# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from datetime import datetime, date
from operator import itemgetter
from random import randint

from django.conf import settings
from django.core.files import File as DjangoFile
from django.core.urlresolvers import reverse, NoReverseMatch
from django.utils.timezone import now
from django.utils.translation import override

from aldryn_newsblog.models import Article, NewsBlogConfig
from aldryn_newsblog.search_indexes import ArticleIndex
from cms.utils.i18n import get_current_language, force_language
from easy_thumbnails.files import get_thumbnailer
from filer.models.imagemodels import Image
from parler.tests.utils import override_parler_settings
from parler.utils.conf import add_default_language_settings
from parler.utils.context import switch_language, smart_override

from . import NewsBlogTestCase, TESTS_STATIC_ROOT

FEATURED_IMAGE_PATH = os.path.join(TESTS_STATIC_ROOT, 'featured_image.jpg')

PARLER_LANGUAGES_HIDE = {
    1: [
        {
            'code': u'en',
            'fallbacks': [u'de'],
            'hide_untranslated': True
        },
        {
            'code': u'de',
            'fallbacks': [u'en'],
            'hide_untranslated': True
        },
        {
            'code': u'fr',
            'fallbacks': [u'en'],
            'hide_untranslated': True
        },
    ],
    'default': {
        'hide_untranslated': True,
        'fallbacks': [],
    }
}

PARLER_LANGUAGES_SHOW = {
    1: [
        {
            'code': u'en',
            'fallbacks': [u'de'],
            'hide_untranslated': False
        },
        {
            'code': u'de',
            'fallbacks': [u'en'],
            'hide_untranslated': False
        },
        {
            'code': u'fr',
            'fallbacks': [u'en'],
            'hide_untranslated': False
        },
    ],
    'default': {
        'hide_untranslated': False,
        'fallbacks': [],
    }
}


class TestViews(NewsBlogTestCase):

    def test_articles_list(self):
        namespace = self.app_config.namespace
        articles = [self.create_article() for _ in range(11)]
        unpublished_article = articles[0]
        unpublished_article.is_published = False
        unpublished_article.save()
        response = self.client.get(
            reverse('{0}:article-list'.format(namespace)))
        for article in articles[1:]:
            self.assertContains(response, article.title)
        self.assertNotContains(response, unpublished_article.title)

    def test_articles_list_exclude_featured(self):
        namespace = self.app_config.namespace
        # configure app config
        exclude_count = 2
        self.app_config.exclude_featured = exclude_count
        self.app_config.paginate_by = 2
        self.app_config.save()
        # set up articles
        articles = []
        featured_articles = []
        for idx in range(6):
            if idx % 2:
                featured_articles.append(self.create_article(is_featured=True))
            else:
                articles.append(self.create_article())
        # imitate ordering by publish date DESC
        articles.reverse()
        featured_articles.reverse()
        # prepare urls
        list_base_url = reverse('{0}:article-list'.format(namespace))
        page_url_template = '{0}?page={1}'
        response_page_1 = self.client.get(list_base_url)
        response_page_2 = self.client.get(
            page_url_template.format(list_base_url, 2))

        # page 1
        # ensure that first two not featured articles are present on first page
        for article in articles[:2]:
            self.assertContains(response_page_1, article.title)
        # Ensure no featured articles are present on first page.
        for featured_article in featured_articles[:2]:
            self.assertNotContains(response_page_1, featured_article.title)

        # page 2
        # check that not excluded featured article is present on second page
        for featured_article in featured_articles[2:]:
            self.assertContains(response_page_2, featured_article.title)
        # ensure that third not featured article is present in the response
        for article in articles[2:]:
            self.assertContains(response_page_2, article.title)

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
                self.create_article(author=author) for _ in range(11)]
            response = self.client.get(reverse(
                'aldryn_newsblog:article-list-by-author',
                kwargs={'author': author.slug}))
            for article in articles:
                self.assertContains(response, article.title)

    def test_articles_by_unknown_author(self):
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-author',
            kwargs={'author': 'unknown'}))
        self.assertEqual(response.status_code, 404)

    def test_articles_by_category(self):
        """
        Tests that we can find articles by their categories, in ANY of the
        languages they are translated to.
        """
        LANGUAGES = add_default_language_settings(PARLER_LANGUAGES_HIDE)
        with override_parler_settings(PARLER_LANGUAGES=LANGUAGES):
            author = self.create_person()
            for category in (self.category1, self.category2):
                articles = []
                code = "{0}-".format(self.language)
                for _ in range(11):
                    article = Article.objects.create(
                        title=self.rand_str(),
                        slug=self.rand_str(prefix=code),
                        app_config=self.app_config,
                        author=author,
                        owner=author.user,
                        publishing_date=now(),
                        is_published=True,
                    )
                    # Make sure there are translations in place for the
                    # articles.
                    for language, _ in settings.LANGUAGES[1:]:
                        with switch_language(article, language):
                            code = "{0}-".format(language)
                            article.title = self.rand_str(prefix=code)
                            article.save()

                    article.categories.add(category)
                    articles.append(article)

                for language, _ in settings.LANGUAGES:
                    with switch_language(category, language):
                        url = reverse(
                            'aldryn_newsblog:article-list-by-category',
                            kwargs={'category': category.slug})
                        response = self.client.get(url)
                    for article in articles:
                        if language in article.get_available_languages():
                            article.set_current_language(language)
                            self.assertContains(response, article.title)
                        else:
                            article.set_current_language(language)
                            self.assertNotContains(response, article.title)

    def test_articles_by_unknown_category(self):
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-category',
            kwargs={'category': 'unknown'}))
        self.assertEqual(response.status_code, 404)


class TestTemplatePrefixes(NewsBlogTestCase):

    def setUp(self):
        super(TestTemplatePrefixes, self).setUp()
        self.app_config.template_prefix = 'dummy'
        self.app_config.save()

    def test_articles_list(self):
        namespace = self.app_config.namespace
        response = self.client.get(
            reverse('{0}:article-list'.format(namespace)))
        self.assertContains(response, 'This is dummy article list page')

    def test_article_detail(self):
        article = self.create_article(app_config=self.app_config)
        namespace = self.app_config.namespace
        response = self.client.get(
            reverse(
                '{0}:article-detail'.format(namespace),
                kwargs={'slug': article.slug}
            ))
        self.assertContains(response, 'This is dummy article detail page')


class TestTranslationFallbacks(NewsBlogTestCase):
    def test_article_detail_not_translated_fallback(self):
        """
        If the fallback is configured, article is available in any
        (configured) language
        """
        author = self.create_person()
        code = "{0}-".format(self.language)

        with override(settings.LANGUAGES[0][0]):
            article = Article.objects.create(
                title=self.rand_str(),
                slug=self.rand_str(prefix=code),
                app_config=self.app_config,
                author=author, owner=author.user,
                publishing_date=now(),
                is_published=True,
            )
            article.save()
            article.categories.add(self.category1)
            url_one = reverse(
                'aldryn_newsblog:article-detail',
                kwargs={'slug': article.slug}
            )
        # Parler settings should be same as cms settings and vice versa
        # ensure that if hide_untranslated = True we don't have a fallback
        # redirect.
        LANGUAGES = add_default_language_settings(PARLER_LANGUAGES_HIDE)
        with override_parler_settings(PARLER_LANGUAGES=LANGUAGES):
            language = settings.LANGUAGES[1][0]
            with switch_language(article, language):
                slug = article.safe_translation_getter('slug', None,
                    language_code=language, any_language=True)
                url = reverse(
                    'aldryn_newsblog:article-detail',
                    kwargs={'slug': slug}
                )
                self.assertNotEquals(url, url_one)
                response = self.client.get(url)
                self.assertEquals(response.status_code, 404)

            # Test again with redirect_on_fallback = False
            with self.settings(CMS_LANGUAGES=self.NO_REDIRECT_CMS_SETTINGS):
                language = settings.LANGUAGES[1][0]
                with switch_language(article, language):
                    slug = article.safe_translation_getter('slug', None)
                    url = reverse(
                        'aldryn_newsblog:article-detail',
                        kwargs={'slug': slug, }
                    )
                    self.assertNotEquals(url, url_one)
                    response = self.client.get(url)
                    self.assertEquals(response.status_code, 404)

    def test_article_detail_not_translated_no_fallback(self):
        """
        If the fallback is disabled, article is available only in the
        language in which is translated
        """
        author = self.create_person()
        code = "{0}-".format(self.language)
        article = Article.objects.create(
            title=self.rand_str(), slug=self.rand_str(prefix=code),
            app_config=self.app_config,
            author=author, owner=author.user,
            publishing_date=now(),
            is_published=True,
        )
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

            # non existing language - it does NOT exists
            language = settings.LANGUAGES[1][0]
            with switch_language(self.category1, language):
                url = reverse('aldryn_newsblog:article-detail',
                              kwargs={'slug': article.slug})
                response = self.client.get(url)
                self.assertEqual(response.status_code, 404)


class TestImages(NewsBlogTestCase):
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


class TestVariousViews(NewsBlogTestCase):
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
            3, tags=(self.rand_str(), self.rand_str()))

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

    def test_articles_by_unknown_tag(self):
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-tag',
            kwargs={'tag': 'unknown'}))
        self.assertEqual(response.status_code, 404)

    def test_articles_count_by_month(self):
        months = [
            {'date': date(1914, 7, 3), 'num_articles': 1},
            {'date': date(1914, 8, 3), 'num_articles': 3},
            {'date': date(1945, 9, 3), 'num_articles': 5},
        ]
        for month in months:
            for _ in range(month['num_articles']):
                article = self.create_article(publishing_date=month['date'])

        # unpublish one specific article to test that it is not counted
        article.is_published = False
        article.save()
        months[-1]['num_articles'] -= 1

        self.assertEquals(
            sorted(
                Article.objects.get_months(
                    request=None, namespace=self.app_config.namespace
                ), key=itemgetter('num_articles')), months)

    def test_articles_count_by_author(self):
        authors = []
        for num_articles in [1, 3, 5]:
            person = self.create_person()
            person.num_articles = num_articles
            authors.append((person, num_articles))

        for i, data in enumerate(authors):
            for _ in range(data[1]):
                article = self.create_article(author=data[0])
            # replace author with it's pk, as we need it to easily compare
            authors[i] = (data[0].pk, data[1])

        # unpublish one specific article to test that it is not counted
        article.is_published = False
        article.save()
        authors[-1] = (authors[-1][0], authors[-1][1] - 1)

        self.assertEquals(
            sorted(
                Article.objects.get_authors(
                    namespace=self.app_config.namespace).values_list(
                        'pk', 'num_articles'),
                key=itemgetter(1)),
            authors)

    def test_articles_count_by_tags(self):
        tags = Article.objects.get_tags(
            request=None, namespace=self.app_config.namespace)
        self.assertEquals(tags, [])

        untagged_articles = []
        for _ in range(5):
            article = self.create_article()
            untagged_articles.append(article)

        # Tag objects are created on attaching tag name to Article,
        # so this looks not very DRY
        tag_names = ('tag foo', 'tag bar', 'tag buzz')
        # create unpublished article to test that it is not counted
        self.create_tagged_articles(
            1, tags=(tag_names[0],), is_published=False)
        tag_slug2 = list(self.create_tagged_articles(
            3, tags=(tag_names[1],)).keys())[0]
        tag_slug3 = list(self.create_tagged_articles(
            5, tags=(tag_names[2],)).keys())[0]
        tags_expected = [
            (tag_slug3, 5),
            (tag_slug2, 3),
        ]
        tags = Article.objects.get_tags(
            request=None, namespace=self.app_config.namespace)
        tags = [(tag.slug, tag.num_articles) for tag in tags]
        self.assertEquals(tags, tags_expected)

    def test_articles_by_date(self):
        in_articles = [
            self.create_article(
                publishing_date=datetime(
                    1914, 7, 28, randint(0, 23), randint(0, 59)))
            for _ in range(11)]
        out_articles = [
            self.create_article(
                publishing_date=datetime(
                    1939, 9, 1, randint(0, 23), randint(0, 59)))
            for _ in range(11)]
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
            for _ in range(11)]
        out_articles = [
            self.create_article(
                publishing_date=datetime(
                    1939, 9, 1, randint(0, 23), randint(0, 59)))
            for _ in range(11)]
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
                    1914, randint(1, 11), randint(1, 28),
                    randint(0, 23), randint(0, 59)))
            for _ in range(11)]
        out_articles = [
            self.create_article(
                publishing_date=datetime(
                    1939, randint(1, 12), randint(1, 28),
                    randint(0, 23), randint(0, 59)))
            for _ in range(11)]
        response = self.client.get(reverse(
            'aldryn_newsblog:article-list-by-year', kwargs={'year': '1914'}))
        for article in out_articles:
            self.assertNotContains(response, article.title)
        for article in in_articles:
            self.assertContains(response, article.title)

    def test_unattached_namespace(self):
        # create a new namespace that has no corresponding blog app page
        app_config = NewsBlogConfig.objects.create(namespace='another')
        articles = [self.create_article(app_config=app_config)
                    for _ in range(11)]
        with self.assertRaises(NoReverseMatch):
            self.client.get(articles[0].get_absolute_url())


class TestIndex(NewsBlogTestCase):
    def test_index_simple(self):
        self.request = self.get_request('en')
        self.index = ArticleIndex()
        content0 = self.rand_str(prefix='content0_')
        self.setup_categories()

        article = self.create_article(content=content0, lead_in='lead in text',
                                      title='a title')
        article.categories.add()
        for tag_name in ('tag 1', 'tag2'):
            article.tags.add(tag_name)
        for category in (self.category1, self.category2):
            article.categories.add(category)
        article.update_search_on_save = True
        article.save()

        self.assertEqual(self.index.get_title(article), 'a title')
        self.assertEqual(self.index.get_description(article), 'lead in text')
        self.assertTrue('lead in text' in self.index.get_search_data(
            article, 'en', self.request))
        self.assertTrue(content0 in self.index.get_search_data(
            article, 'en', self.request))
        self.assertTrue('tag 1' in self.index.get_search_data(
            article, 'en', self.request))
        self.assertTrue(self.category1.name in self.index.get_search_data(
            article, 'en', self.request))

    def test_index_multilingual(self):
        self.index = ArticleIndex()
        content0 = self.rand_str(prefix='content0_')
        self.setup_categories()

        article_1 = self.create_article(
            content=content0, lead_in=u'lead in text', title=u'a title')
        article_2 = self.create_article(
            content=content0, lead_in=u'lead in text', title=u'second title')
        for article in (article_1, article_2):
            for tag_name in ('tag 1', 'tag2'):
                article.tags.add(tag_name)
            for category in (self.category1, self.category2):
                article.categories.add(category)
        with switch_language(article_2, 'de'):
            article_2.title = u'de title'
            article_2.lead_in = u'de lead in'
            article_2.save()

        LANGUAGES = add_default_language_settings(PARLER_LANGUAGES_HIDE)
        with override_parler_settings(PARLER_LANGUAGES=LANGUAGES):
            with smart_override('de'):
                language = get_current_language()
                # english-only article is excluded
                qs = self.index.index_queryset(language)
                self.assertEqual(qs.count(), 1)
                self.assertEqual(
                    qs.translated(language, title__icontains='title').count(),
                    1
                )
                # the language is correctly setup
                for article_de in qs:
                    self.assertEqual(
                        self.index.get_title(article_de), 'de title')
                    self.assertEqual(
                        self.index.get_description(article_de), 'de lead in')


class ViewLanguageFallbackMixin(object):
    view_name = None
    view_kwargs = {}

    def get_view_kwargs(self):
        """
        Prepare and return kwargs to resolve view
        :return: dict
        """
        return {}.update(self.view_kwargs)

    def create_authors(self):
        self.author = self.create_person()
        self.owner = self.author.user
        return self.author, self.owner

    def create_de_article(self, author=None, owner=None, app_config=None,
                          categories=None):
        if author is None:
            author = self.author
        if owner is None:
            owner = self.owner
        if app_config is None:
            app_config = self.app_config

        with force_language('de'):
            de_article = Article.objects.create(
                title='a DE title',
                slug='a-de-title',
                lead_in='DE lead in text',
                author=author,
                owner=owner,
                app_config=app_config,
                publishing_date=now(),
                is_published=True,
            )
        if categories:
            de_article.categories = categories
        de_article.tags.add('tag1')
        de_article.save()
        return de_article

    def create_en_articles(self, author=None, owner=None, app_config=None,
                           amount=3, categories=None):
        if author is None:
            author = self.author
        if owner is None:
            owner = self.owner
        if app_config is None:
            app_config = self.app_config

        with force_language('en'):
            articles = []
            for _ in range(amount):
                article = self.create_article(author=author,
                                              owner=owner,
                                              app_config=app_config)
                if categories:
                    article.categories = categories
                article.tags.add('tag1')
                article.save()
                articles.append(article)
        return articles

    def test_a0_en_only(self):
        namespace = self.app_config.namespace
        self.page.unpublish('de')
        author, owner = self.create_authors()
        author.translations.create(
            slug='{0}-de'.format(author.slug),
            language_code='de')
        de_article = self.create_de_article(
            author=author,
            owner=owner,
            categories=[self.category1],
        )
        articles = self.create_en_articles(categories=[self.category1])
        with force_language('en'):
            response = self.client.get(
                reverse(
                    '{0}:{1}'.format(namespace, self.view_name),
                    kwargs=self.get_view_kwargs()
                )
            )
        for article in articles:
            self.assertContains(response, article.title)
        self.assertNotContains(response, de_article.title)

    def test_a1_en_de(self):
        namespace = self.app_config.namespace
        author, owner = self.create_authors()
        author.translations.create(
            slug='{0}-de'.format(author.slug),
            language_code='de')
        de_article = self.create_de_article(
            author=author,
            owner=owner,
            categories=[self.category1]
        )
        articles = self.create_en_articles(categories=[self.category1])
        with force_language('en'):
            response = self.client.get(
                reverse(
                    '{0}:{1}'.format(namespace, self.view_name),
                    kwargs=self.get_view_kwargs()
                )
            )
        for article in articles:
            self.assertContains(response, article.title)
        self.assertContains(response, de_article.title)


class ArticleListViewLanguageFallback(ViewLanguageFallbackMixin,
                                      NewsBlogTestCase):
    view_name = 'article-list'


class LatestArticlesFeedLanguageFallback(ViewLanguageFallbackMixin,
                                         NewsBlogTestCase):
    view_name = 'article-list-feed'


class YearArticleListLanguageFallback(ViewLanguageFallbackMixin,
                                      NewsBlogTestCase):
    view_name = 'article-list-by-year'

    def get_view_kwargs(self):
        return {'year': now().year}


class MonthArticleListLanguageFallback(ViewLanguageFallbackMixin,
                                       NewsBlogTestCase):
    view_name = 'article-list-by-month'

    def get_view_kwargs(self):
        kwargs = {
            'year': now().year,
            'month': now().month,
        }
        return kwargs


class DayArticleListLanguageFallback(ViewLanguageFallbackMixin,
                                     NewsBlogTestCase):
    view_name = 'article-list-by-day'

    def get_view_kwargs(self):
        kwargs = {
            'year': now().year,
            'month': now().month,
            'day': now().day,
        }
        return kwargs


# class AuthorArticleListLanguageFallback(ViewLanguageFallbackMixin,
#                                         NewsBlogTestCase):
#     view_name = 'article-list-by-author'
#
#     def get_view_kwargs(self):
#         kwargs = {
#             'author': self.author.slug
#         }
#         return kwargs


class CategoryArticleListLanguageFallback(ViewLanguageFallbackMixin,
                                          NewsBlogTestCase):
    view_name = 'article-list-by-category'

    def get_view_kwargs(self):
        kwargs = {
            'category': self.category1.slug
        }
        return kwargs


class CategoryFeedListLanguageFallback(ViewLanguageFallbackMixin,
                                       NewsBlogTestCase):
    view_name = 'article-list-by-category-feed'

    def get_view_kwargs(self):
        kwargs = {
            'category': self.category1.slug
        }
        return kwargs


class TagArticleListLanguageFallback(ViewLanguageFallbackMixin,
                                     NewsBlogTestCase):
    view_name = 'article-list-by-tag'

    def get_view_kwargs(self):
        kwargs = {
            'tag': 'tag1'
        }
        return kwargs


class TagFeedLanguageFallback(ViewLanguageFallbackMixin,
                              NewsBlogTestCase):
    view_name = 'article-list-by-tag-feed'

    def get_view_kwargs(self):
        kwargs = {
            'tag': 'tag1'
        }
        return kwargs
