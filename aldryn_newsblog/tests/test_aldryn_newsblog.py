# -*- coding: utf-8 -*-

import os
import random
import reversion
import six
import string
import unittest

from datetime import datetime, date
from easy_thumbnails.files import get_thumbnailer
from operator import itemgetter
from random import randint

from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import transaction
from django.test import TransactionTestCase
from django.utils.translation import activate, override, get_language
from aldryn_newsblog.search_indexes import ArticleIndex

from cms import api
from cms.utils import get_cms_setting
from filer.models.imagemodels import Image
from parler.tests.utils import override_parler_settings
from parler.utils.conf import add_default_language_settings
from parler.utils.context import switch_language, smart_override


from aldryn_categories.models import Category
from aldryn_categories.tests import CategoryTestCaseMixin

from aldryn_people.models import Person

from aldryn_search.helpers import get_request

from aldryn_newsblog.models import Article, NewsBlogConfig
from aldryn_reversion.core import create_revision_with_placeholders

from . import TESTS_STATIC_ROOT

FEATURED_IMAGE_PATH = os.path.join(TESTS_STATIC_ROOT, 'featured_image.jpg')


def rand_str(prefix=u'', length=23, chars=string.ascii_letters):
    return prefix + u''.join(random.choice(chars) for _ in range(length))


class NewsBlogTestsMixin(CategoryTestCaseMixin):

    @staticmethod
    def create_user():
        return User.objects.create(username=rand_str(), first_name=rand_str(),
                                   last_name=rand_str())

    def create_person(self):
        return Person.objects.create(user=self.create_user(), slug=rand_str())

    def create_article(self, content=None, **kwargs):
        try:
            author = kwargs['author']
        except KeyError:
            author = self.create_person()
        try:
            owner = kwargs['owner']
        except KeyError:
            owner = author.user

        fields = {
            'title': rand_str(),
            'slug': rand_str(),
            'author': author,
            'owner': owner,
            'app_config': self.app_config,
            'publishing_date': datetime.now(),
            'is_published': True,
        }

        fields.update(kwargs)

        article = Article.objects.create(**fields)

        if content:
            api.add_plugin(article.content, 'TextPlugin',
                           self.language, body=content)

        return article

    def create_tagged_articles(self, num_articles=3, tags=('tag1', 'tag2')):
        """Create num_articles Articles for each tag"""
        articles = {}
        for tag_name in tags:
            tagged_articles = []
            for _ in range(num_articles):
                article = self.create_article()
                article.save()
                article.tags.add(tag_name)
                tagged_articles.append(article)
            tag_slug = tagged_articles[0].tags.slugs()[0]
            articles[tag_slug] = tagged_articles
        return articles

    def setup_categories(self):
        """Sets-up i18n categories (self.category_root, self.category1 and
        self.category2) for use in tests"""
        if not self.language:
            self.language = settings.LANGUAGES[0][0]

        categories = []
        # Set the default language, create the objects
        with override(self.language):
            code = "{0}-".format(self.language)
            self.category_root = Category.add_root(
                name=rand_str(prefix=code, length=8))
            categories.append(self.category_root)
            self.category1 = self.category_root.add_child(
                name=rand_str(prefix=code, length=8))
            categories.append(self.category1)
            self.category2 = self.category_root.add_child(
                name=rand_str(prefix=code, length=8))
            categories.append(self.category2)

        # We should reload category_root, since we modified its children.
        self.category_root = self.reload(self.category_root)

        # Setup the other language(s) translations for the categories
        for language, _ in settings.LANGUAGES[1:]:
            for category in categories:
                with switch_language(category, language):
                    code = "{0}-".format(language)
                    category.name = rand_str(prefix=code, length=8)
                    category.save()

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.root_page = api.create_page(
            'root page', self.template, self.language, published=True)
        self.app_config = NewsBlogConfig.objects.create(
            namespace='NBNS', paginate_by=10)
        self.page = api.create_page(
            'page', self.template, self.language, published=True,
            parent=self.root_page,
            apphook='NewsBlogApp',
            apphook_namespace=self.app_config.namespace)
        self.placeholder = self.page.placeholders.all()[0]
        self.request = get_request('en')

        self.setup_categories()

        for page in self.root_page, self.page:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, page.get_slug(), page)
                page.publish(language)


class TestAldrynNewsBlog(NewsBlogTestsMixin, TransactionTestCase):

    def test_create_article(self):
        article = self.create_article()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, article.title)

    def test_delete_article(self):
        article = self.create_article()
        article_pk = article.pk
        article_url = article.get_absolute_url()
        response = self.client.get(article_url)
        self.assertContains(response, article.title)
        Article.objects.get(pk=article_pk).delete()
        response = self.client.get(article_url)
        self.assertEqual(response.status_code, 404)

    def test_published_articles_filtering(self):
        for i in range(5):
            self.create_article()
        unpublised_article = Article.objects.first()
        unpublised_article.is_published = False
        unpublised_article.save()
        self.assertEqual(Article.objects.published().count(), 4)
        self.assertNotIn(unpublised_article, Article.objects.published())

    def test_view_article_not_published(self):
        article = self.create_article(is_published=False)
        response = self.client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 404)

    def test_articles_list(self):
        articles = [self.create_article() for _ in range(10)]
        unpublished_article = articles[0]
        unpublished_article.is_published = False
        unpublished_article.save()
        response = self.client.get(
            reverse('aldryn_newsblog:article-list'))
        for article in articles[1:]:
            self.assertContains(response, article.title)
        self.assertNotContains(response, unpublished_article.title)

    def test_articles_list_pagination(self):
        namespace = self.app_config.namespace
        paginate_by = self.app_config.paginate_by
        articles = [self.create_article(
            app_config=self.app_config,
            publishing_date=datetime(2000 - i, 1, 1, 1, 1)
        ) for i in range(paginate_by + 5)]

        response = self.client.get(
            reverse('{0}:article-list'.format(namespace)))
        for article in articles[:paginate_by]:
            self.assertContains(response, article.title)
        for article in articles[paginate_by:]:
            self.assertNotContains(response, article.title)

        response = self.client.get(
            reverse('{0}:article-list'.format(namespace)) + '?page=2')
        for article in articles[:paginate_by]:
            self.assertNotContains(response, article.title)
        for article in articles[paginate_by:]:
            self.assertContains(response, article.title)

    def test_articles_by_author(self):
        author1, author2 = self.create_person(), self.create_person()
        for author in (author1, author2):
            articles = [
                self.create_article(author=author) for _ in range(10)]
            response = self.client.get(reverse(
                'aldryn_newsblog:article-list-by-author',
                kwargs={'author': author.slug}))
            for article in articles:
                self.assertContains(response, article.title)

    def test_articles_by_category(self):
        """Tests that we can find articles by their categories, in ANY of the
        languages they are translated to"""
        author = self.create_person()
        for category in (self.category1, self.category2):
            articles = []
            code = "{0}-".format(self.language)
            for _ in range(10):
                article = Article.objects.create(
                    title=rand_str(), slug=rand_str(prefix=code),
                    app_config=self.app_config,
                    author=author, owner=author.user,
                    publishing_date=datetime.now())
                # Make sure there are translations in place for the articles.
                for language, _ in settings.LANGUAGES[1:]:
                    with switch_language(article, language):
                        code = "{0}-".format(language)
                        article.title = rand_str(prefix=code)
                        article.save()

                article.categories.add(category)
                articles.append(article)

            for language, _ in settings.LANGUAGES:
                with switch_language(category, language):
                    url = reverse('aldryn_newsblog:article-list-by-category',
                                  kwargs={'category': category.slug})
                response = self.client.get(url)
                for article in articles:
                    if language in article.get_available_languages():
                        article.set_current_language(language)
                        self.assertContains(response, article.title)
                    else:
                        article.set_current_language(language)
                        self.assertNotContains(response, article.title)

    def test_article_detail_not_translated_fallback(self):
        """
        If the fallback is configured, article is available in any (configured) language
        """
        author = self.create_person()
        code = "{0}-".format(self.language)
        article = Article.objects.create(
            title=rand_str(), slug=rand_str(prefix=code),
            app_config=self.app_config,
            author=author, owner=author.user,
            publishing_date=datetime.now())
        article.save()
        article.categories.add(self.category1)

        # current language - it still exists
        article = Article.objects.get(pk=article.pk)
        language = settings.LANGUAGES[0][0]
        with switch_language(self.category1, language):
            url = reverse('aldryn_newsblog:article-detail',
                          kwargs={'slug': article.slug})
            response = self.client.get(url)
            self.assertContains(response, article.title)

        # non existing language - it still exists
        language = settings.LANGUAGES[1][0]
        with switch_language(self.category1, language):
            url = reverse('aldryn_newsblog:article-detail',
                          kwargs={'slug': article.slug})
            response = self.client.get(url)
            self.assertContains(response, article.title)

    def test_article_detail_not_translated_no_fallback(self):
        """
        If the fallback is disabled, article is available only in the
        language in which is translated
        """
        author = self.create_person()
        code = "{0}-".format(self.language)
        article = Article.objects.create(
            title=rand_str(), slug=rand_str(prefix=code),
            app_config=self.app_config,
            author=author, owner=author.user,
            publishing_date=datetime.now())
        article.save()
        article.categories.add(self.category1)

        PARLER_LANGUAGES = {
            1: (
                {'code': 'de'},
                {'code': 'fr'},
                {'code': 'en'},
            ),
            'default': {
                'hide_untranslated': True,
            }
        }
        LANGUAGES = add_default_language_settings(PARLER_LANGUAGES)
        with override_parler_settings(PARLER_LANGUAGES=LANGUAGES):

            # current language - it still exists
            article = Article.objects.get(pk=article.pk)
            language = settings.LANGUAGES[0][0]
            with switch_language(self.category1, language):
                url = reverse('aldryn_newsblog:article-detail',
                              kwargs={'slug': article.slug})
                response = self.client.get(url)
                self.assertContains(response, article.title)

            # non existing language - it still exists
            language = settings.LANGUAGES[1][0]
            with switch_language(self.category1, language):
                url = reverse('aldryn_newsblog:article-detail',
                              kwargs={'slug': article.slug})
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)

    def test_article_detail_show_featured_image(self):
        author = self.create_person()
        with open(FEATURED_IMAGE_PATH, 'rb') as f:
            file_obj = DjangoFile(f, name='featured_image.jpg')
            image = Image.objects.create(owner=author.user,
                                         original_filename='featured_image.jpg',
                                         file=file_obj,
                                         subject_location='fooobar')
        article = self.create_article(author=author, featured_image=image)
        response = self.client.get(article.get_absolute_url())
        image_url = get_thumbnailer(article.featured_image).get_thumbnail({
            'size': (800, 450),
            'crop': True,
            'subject_location': article.featured_image.subject_location
        }).url
        self.assertContains(response, image_url)

    def test_articles_by_tag(self):
        """
        Tests that TagArticleList view properly filters articles by their tags.

        This uses ANY of the languages articles are translated to.
        """

        untagged_articles = []
        for _ in range(5):
            article = self.create_article()
            untagged_articles.append(article)

        articles = self.create_tagged_articles(
            3, tags=(rand_str(), rand_str()))

        # tags are created in previous loop on demand, we need their slugs
        tag_slug1, tag_slug2 = articles.keys()
        url = reverse('aldryn_newsblog:article-list-by-tag',
                      kwargs={'tag': tag_slug2})
        response = self.client.get(url)
        for article in articles[tag_slug2]:
            self.assertContains(response, article.title)
        for article in articles[tag_slug1]:
            self.assertNotContains(response, article.title)
        for article in untagged_articles:
            self.assertNotContains(response, article.title)

    def test_articles_count_by_month(self):
        months = [
            {'date': date(1914, 7, 3), 'num_articles': 1},
            {'date': date(1914, 8, 3), 'num_articles': 3},
            {'date': date(1945, 9, 3), 'num_articles': 5},
        ]
        for month in months:
            for _ in range(month['num_articles']):
                self.create_article(publishing_date=month['date'])
        self.assertEquals(
            sorted(
                Article.objects.get_months(
                    namespace=self.app_config.namespace),
                key=itemgetter('num_articles')),
            months)

    def test_articles_count_by_author(self):
        authors = []
        for num_articles in [1, 3, 5]:
            person = self.create_person()
            person.num_articles = num_articles
            authors.append((person, num_articles))

        for i, data in enumerate(authors):
            for _ in range(data[1]):
                self.create_article(author=data[0])
            # replace author with it's pk, as we need it to easily compare
            authors[i] = (data[0].pk, data[1])

        self.assertEquals(
            sorted(
                Article.objects.get_authors(
                    namespace=self.app_config.namespace).values_list(
                        'pk', 'num_articles'),
                key=itemgetter(1)),
            authors)

    def test_articles_count_by_tags(self):
        untagged_articles = []
        for _ in range(5):
            article = self.create_article()
            untagged_articles.append(article)
        # Tag objects are created on attaching tag name to Article,
        # so this looks not very DRY
        tag_names = ('tag foo', 'tag bar', 'tag buzz')
        tag_slug1 = self.create_tagged_articles(
            1, tags=(tag_names[0],)).keys()[0]
        tag_slug2 = self.create_tagged_articles(
            3, tags=(tag_names[1],)).keys()[0]
        tag_slug3 = self.create_tagged_articles(
            5, tags=(tag_names[2],)).keys()[0]
        tags_expected = [
            (tag_slug3, 5),
            (tag_slug2, 3),
            (tag_slug1, 1),
        ]
        tags = Article.objects.get_tags(namespace=self.app_config.namespace)
        tags = map(lambda x: (x.slug, x.num_articles), tags)
        self.assertEquals(tags, tags_expected)

    def test_articles_by_date(self):
        in_articles = [
            self.create_article(
                publishing_date=datetime(
                    1914, 7, 28, randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        out_articles = [
            self.create_article(
                publishing_date=datetime(
                    1939, 9, 1, randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-day',
            kwargs={'year': '1914', 'month': '07', 'day': '28'}))
        for article in out_articles:
            self.assertNotContains(response, article.title)
        for article in in_articles:
            self.assertContains(response, article.title)

    def test_articles_by_month(self):
        in_articles = [
            self.create_article(
                publishing_date=datetime(
                    1914, 7, randint(1, 31), randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        out_articles = [
            self.create_article(
                publishing_date=datetime(
                    1939, 9, 1, randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-month',
            kwargs={'year': '1914', 'month': '07'}))
        for article in out_articles:
            self.assertNotContains(response, article.title)
        for article in in_articles:
            self.assertContains(response, article.title)

    def test_articles_by_year(self):
        in_articles = [
            self.create_article(
                publishing_date=datetime(
                    1914, randint(1, 12), randint(1, 28),
                    randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        out_articles = [
            self.create_article(
                publishing_date=datetime(
                    1939, randint(1, 12), randint(1, 28),
                    randint(0, 23), randint(0, 59)))
            for _ in range(10)]
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-year', kwargs={'year': '1914'}))
        for article in out_articles:
            self.assertNotContains(response, article.title)
        for article in in_articles:
            self.assertContains(response, article.title)

    def test_has_content(self):
        # Just make sure we have a known language
        activate(self.language)
        title = rand_str()
        content = rand_str()
        author = self.create_person()
        article = Article.objects.create(
            title=title, slug=rand_str(), author=author, owner=author.user,
            app_config=self.app_config, publishing_date=datetime.now())
        article.save()
        api.add_plugin(article.content, 'TextPlugin', self.language)
        plugin = article.content.get_plugins()[0].get_plugin_instance()[0]
        plugin.body = content
        plugin.save()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title)
        self.assertContains(response, content)

    def test_unattached_namespace(self):
        # create a new namespace that has no corresponding blog app page
        app_config = NewsBlogConfig.objects.create(namespace='another')
        articles = [self.create_article(app_config=app_config)
                    for _ in range(10)]
        with self.assertRaises(NoReverseMatch):
            response = self.client.get(articles[0].get_absolute_url())
        response = self.client.get(
            reverse('aldryn_newsblog:article-list'))
        for article in articles:
            self.assertNotContains(response, article.title)

    def test_auto_slugifies(self):
        activate(self.language)
        title = u'This is a title'
        author = self.create_person()
        article = Article.objects.create(
            title=title, author=author, owner=author.user,
            app_config=self.app_config, publishing_date=datetime.now())
        article.save()
        self.assertEquals(article.slug, 'this-is-a-title')
        # Now, let's try another with the same title
        article.id = None
        # Note, it cannot be the exact same title, else we'll fail the unique
        # constraint on the field.
        article.title = title.lower()
        article.save()
        # Note that this should be "incremented" slug here.
        self.assertEquals(article.slug, 'this-is-a-title_1')
        article.id = None
        article.title = title.upper()
        article.save()
        self.assertEquals(article.slug, 'this-is-a-title_2')

    def test_auto_existing_author(self):
        author = self.create_person()
        article = Article.objects.create(
            title=rand_str(), owner=author.user,
            app_config=self.app_config, publishing_date=datetime.now())
        article.save()
        self.assertEquals(article.author.user, article.owner)

        old = self.app_config.create_authors
        self.app_config.create_authors = False
        self.app_config.save()
        article = Article.objects.create(
            title=rand_str(), owner=author.user,
            app_config=self.app_config, publishing_date=datetime.now())
        self.app_config.create_authors = old
        self.app_config.save()
        self.assertEquals(article.author, None)

    def test_auto_new_author(self):
        user = self.create_user()
        article = Article.objects.create(
            title=rand_str(), owner=user,
            app_config=self.app_config, publishing_date=datetime.now())
        article.save()
        self.assertEquals(article.author.name,
                          u' '.join((user.first_name, user.last_name)))

    def test_latest_articles_plugin(self):
        page = api.create_page(
            'plugin page', self.template, self.language,
            parent=self.root_page, published=True)
        placeholder = page.placeholders.all()[0]
        api.add_plugin(placeholder, 'NewsBlogLatestArticlesPlugin',
                       self.language, app_config=self.app_config,
                       latest_articles=7)
        plugin = placeholder.get_plugins()[0].get_plugin_instance()[0]
        plugin.save()
        page.publish(self.language)
        articles = [self.create_article() for _ in range(7)]
        another_app_config = NewsBlogConfig.objects.create(namespace='another')
        another_articles = [self.create_article(app_config=another_app_config)
                            for _ in range(3)]
        response = self.client.get(page.get_absolute_url())
        for article in articles:
            self.assertContains(response, article.title)
        for article in another_articles:
            self.assertNotContains(response, article.title)

    def test_index_simple(self):
        self.index = ArticleIndex()
        content0 = rand_str(prefix='content0_')
        self.setup_categories()

        article = self.create_article(content=content0, lead_in='lead in text',
                                      title='a title')
        article.categories.add()
        for tag_name in ('tag 1', 'tag2'):
            article.tags.add(tag_name)
        for category in (self.category1, self.category2):
            article.categories.add(category)

        self.assertEqual(self.index.get_title(article), 'a title')
        self.assertEqual(self.index.get_description(article), 'lead in text')
        self.assertTrue('lead in text' in self.index.get_search_data(article, 'en', self.request))
        self.assertTrue(content0 in self.index.get_search_data(article, 'en', self.request))
        self.assertTrue('tag 1' in self.index.get_search_data(article, 'en', self.request))
        self.assertTrue(self.category1.name in self.index.get_search_data(article, 'en', self.request))

    def test_index_multilingual(self):
        self.index = ArticleIndex()
        content0 = rand_str(prefix='content0_')
        self.setup_categories()

        article_1 = self.create_article(content=content0, lead_in=u'lead in text',
                                        title=u'a title')
        article_2 = self.create_article(content=content0, lead_in=u'lead in text',
                                        title=u'second title')
        for article in (article_1, article_2):
            for tag_name in ('tag 1', 'tag2'):
                article.tags.add(tag_name)
            for category in (self.category1, self.category2):
                article.categories.add(category)
        with switch_language(article_2, 'de'):
            article_2.title = u'de title'
            article_2.lead_in = u'de lead in'
            article_2.save()

        PARLER_LANGUAGES = {
            1: (
                {'code': 'de', },
                {'code': 'fr', },
                {'code': 'en', },
            ),
            'default': {
                'hide_untranslated': True,
            }
        }
        LANGUAGES = add_default_language_settings(PARLER_LANGUAGES)
        with override_parler_settings(PARLER_LANGUAGES=LANGUAGES):
            with smart_override('de'):
                language = get_language()
                # english-only article is excluded
                qs = self.index.index_queryset(language)
                self.assertEqual(qs.count(), 1)
                self.assertEqual(qs.translated(language, title__icontains='title').count(), 1)
                # the language is correctly setup
                for article_de in qs:
                    self.assertEqual(self.index.get_title(article_de), 'de title')
                    self.assertEqual(self.index.get_description(article_de), 'de lead in')


class AdminTest(NewsBlogTestsMixin, TransactionTestCase):

    def test_admin_owner_default(self):
        from django.contrib import admin
        admin.autodiscover()

        user = self.create_user()
        user.is_superuser = True
        user.save()

        Person.objects.create(user=user, name= u' '.join((user.first_name, user.last_name)))

        admin_inst = admin.site._registry[Article]
        self.request.user = user
        self.request.META['HTTP_HOST'] = 'example.com'
        response = admin_inst.add_view(self.request)
        self.assertContains(response, '<option value="1" selected="selected">%s</option>' % user.username)
        self.assertContains(response, '<option value="1" selected="selected">%s</option>' % user.get_full_name())


class TestVersioning(NewsBlogTestsMixin, TransactionTestCase):
    def create_revision(self, article, content=None, language=None, **kwargs):
        with transaction.atomic():
            with reversion.create_revision():
                for k, v in six.iteritems(kwargs):
                    setattr(article, k, v)
                if content:
                    plugins = article.content.get_plugins()
                    plugin = plugins[0].get_plugin_instance()[0]
                    plugin.body = content
                    plugin.save()
                # TODO: Cover both cases (plugin modification/recreation)
                # if content:
                #     article.content.get_plugins().delete()
                #     api.add_plugin(article.content, 'TextPlugin',
                #                    self.language, body=content)
                article.save()

    def revert_to(self, article, revision):
        reversion.get_for_object(article)[revision].revision.revert()

    def test_revert_revision(self):
        title1 = rand_str(prefix='title1_')
        title2 = rand_str(prefix='title2_')

        content0 = rand_str(prefix='content0_')
        content1 = rand_str(prefix='content1_')
        content2 = rand_str(prefix='content2_')

        article = self.create_article(content=content0)

        # Revision 1
        self.create_revision(article, title=title1, content=content1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1)
        self.assertContains(response, content1)
        self.assertNotContains(response, content0)

        # Revision 2
        self.create_revision(article, title=title2, content=content2)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2)
        self.assertContains(response, content2)
        self.assertNotContains(response, content1)

        # Revert to revision 1
        self.revert_to(article, 1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1)
        self.assertContains(response, content1)
        self.assertNotContains(response, content0)
        self.assertNotContains(response, content2)

    def test_revert_translated_revision(self):
        title1_en = rand_str(prefix='title1_en_')
        title1_de = rand_str(prefix='title1_de_')
        title2_en = rand_str(prefix='title2_en_')
        title2_de = rand_str(prefix='title2_de_')

        article = self.create_article()

        # Revision 1
        article.set_current_language('en')
        self.create_revision(article, title=title1_en)

        article.set_current_language('de')
        self.create_revision(article, title=title1_de)

        with switch_language(article, 'en'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revision 2a (modify just EN)
        article.set_current_language('en')
        self.create_revision(article, title=title2_en)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revision 2b (modify just DE)
        article.set_current_language('de')
        self.create_revision(article, title=title2_de)

        with switch_language(article, 'en'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title2_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title2_de)

        # Revert to revision 2a (EN=2, DE=1)
        self.revert_to(article, 1)

        with switch_language(article, 'en'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title2_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revert to revision 1 (EN=1, DE=1)
        self.revert_to(article, 2)

        with switch_language(article, 'en'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

    def test_edit_plugin_directly(self):
        content0 = rand_str(prefix='content0_')
        content1 = rand_str(prefix='content1_')
        content2 = rand_str(prefix='content2_')

        article = self.create_article(content=content0)

        # Revision 1
        self.create_revision(article, content=content1)

        self.assertEqual(
            len(reversion.get_for_object(article)), 1)

        # Revision 2
        with transaction.atomic():
            with reversion.create_revision():
                plugins = article.content.get_plugins()
                plugin = plugins[0].get_plugin_instance()[0]
                plugin.body = content2
                plugin.save()
                create_revision_with_placeholders(article)

        self.assertEqual(
            len(reversion.get_for_object(article)), 2)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, content2)
        self.assertNotContains(response, content1)

        # Revert to revision 1
        self.revert_to(article, 1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, content1)
        self.assertNotContains(response, content2)


if __name__ == '__main__':
    unittest.main()
