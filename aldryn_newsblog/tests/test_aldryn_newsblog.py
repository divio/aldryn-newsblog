# -*- coding: utf-8 -*-

import unittest
import random
import six
import string
from datetime import datetime
from random import randint

from django.conf import settings
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.db import transaction
from django.test import TestCase, TransactionTestCase
from django.utils.translation import activate, override

from cms import api
from cms.utils import get_cms_setting
from parler.utils.context import switch_language

from aldryn_categories.models import Category
from aldryn_categories.tests import CategoryTestCaseMixin

from aldryn_people.models import Person

import reversion

from aldryn_newsblog.models import Article, NewsBlogConfig
from aldryn_newsblog.versioning import create_revision_with_placeholders


def rand_str(prefix='', length=23, chars=string.ascii_letters):
    return prefix + ''.join(random.choice(chars) for _ in range(length))


class NewsBlogTestsMixin(CategoryTestCaseMixin):
    def create_person(self):
        user = User.objects.create(
            username=rand_str(), first_name=rand_str(), last_name=rand_str())
        person = Person.objects.create(user=user, slug=rand_str())
        return person

    def create_article(self, content=None, **kwargs):
        try:
            author = kwargs['author']
        except KeyError:
            author = self.create_person()

        fields = {
            'title': rand_str(),
            'slug': rand_str(),
            'author': author,
            'owner': author.user,
            'namespace': self.ns_newsblog,
            'publishing_date': datetime.now()
        }

        fields.update(kwargs)

        article = Article.objects.create(**fields)

        if content:
            api.add_plugin(article.content, 'TextPlugin',
                           self.language, body=content)

        return article

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
        self.ns_newsblog = NewsBlogConfig.objects.create(namespace='NBNS')
        self.page = api.create_page(
            'page', self.template, self.language, published=True,
            apphook='NewsBlogApp',
            apphook_namespace=self.ns_newsblog.namespace)
        self.page.publish(self.language)
        self.placeholder = self.page.placeholders.all()[0]

        self.setup_categories()

        for language, _ in settings.LANGUAGES[1:]:
            api.create_title(language, 'page', self.page)
            self.page.publish(language)


class TestAldrynNewsBlog(NewsBlogTestsMixin, TestCase):

    def test_create_post(self):
        article = self.create_article()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, article.title)

    def test_delete_post(self):
        article = self.create_article()
        article_url = article.get_absolute_url()
        response = self.client.get(article_url)
        self.assertContains(response, article.title)
        Article.objects.get(slug=article.slug).delete()
        response = self.client.get(article_url)
        self.assertEqual(response.status_code, 404)

    def test_articles_list(self):
        articles = [self.create_article() for _ in range(10)]
        response = self.client.get(
            reverse('aldryn_newsblog:article-list'))
        for article in articles:
            self.assertContains(response, article.title)

    def test_articles_list_pagination(self):
        paginate_by = settings.ALDRYN_NEWSBLOG_PAGINATE_BY
        articles = [
            self.create_article(publishing_date=datetime(
                2000 - i, 1, 1, 1, 1)) for i in range(paginate_by + 5)]

        response = self.client.get(
            reverse('aldryn_newsblog:article-list'))
        for article in articles[:paginate_by]:
            self.assertContains(response, article.title)
        for article in articles[paginate_by:]:
            self.assertNotContains(response, article.title)

        response = self.client.get(
            reverse('aldryn_newsblog:article-list') + '?page=2')
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
                    namespace=self.ns_newsblog,
                    author=author, owner=author.user,
                    publishing_date=datetime.now())
                article.save()
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
                    with switch_language(article, language):
                        self.assertContains(response, article.title)

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
            namespace=self.ns_newsblog, publishing_date=datetime.now())
        article.save()
        api.add_plugin(article.content, 'TextPlugin', self.language)
        plugin = article.content.get_plugins()[0].get_plugin_instance()[0]
        plugin.body = content
        plugin.save()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title)
        self.assertContains(response, content)

    def test_wrong_namespace(self):
        namespace = NewsBlogConfig.objects.create(namespace='another')
        article = self.create_article(namespace=namespace)
        response = self.client.get(article.get_absolute_url())
        self.assertEqual(response.status_code, 404)


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

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1_en)

        with override('de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revision 2a (modify just EN)
        article.set_current_language('en')
        self.create_revision(article, title=title2_en)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_en)

        with override('de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revision 2b (modify just DE)
        article.set_current_language('de')
        self.create_revision(article, title=title2_de)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_en)

        with override('de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title2_de)

        # Revert to revision 2a (EN=2, DE=1)
        self.revert_to(article, 1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_en)

        with override('de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revert to revision 1 (EN=1, DE=1)
        self.revert_to(article, 2)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1_en)

        with override('de'):
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
