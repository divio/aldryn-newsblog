# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import datetime
import pytz

from django.core.urlresolvers import reverse
from django.test import TransactionTestCase

from aldryn_newsblog.models import NewsBlogConfig
from cms import api

from . import NewsBlogTestsMixin


class TestAppConfigPluginsBase(NewsBlogTestsMixin, TransactionTestCase):
    plugin_to_test = 'TextPlugin'
    plugin_params = {}

    def setUp(self):
        super(TestAppConfigPluginsBase, self).setUp()
        self.page = api.create_page(
            'plugin page', self.template, self.language,
            parent=self.root_page, published=True
        )
        self.placeholder = self.page.placeholders.all()[0]
        api.add_plugin(self.placeholder, self.plugin_to_test, self.language,
            app_config=self.app_config, **self.plugin_params)
        self.plugin = self.placeholder.get_plugins()[0].get_plugin_instance()[0]
        self.plugin.save()
        self.page.publish(self.language)
        self.another_app_config = NewsBlogConfig.objects.create(
            namespace=self.rand_str())


class TestArchivePlugin(TestAppConfigPluginsBase):
    plugin_to_test = 'NewsBlogArchivePlugin'

    def test_archive_plugin(self):
        dates = [
            datetime.datetime(2014, 11, 15, 12, 0, 0, 0, pytz.UTC),
            datetime.datetime(2014, 11, 16, 12, 0, 0, 0, pytz.UTC),
            datetime.datetime(2015, 1, 15, 12, 0, 0, 0, pytz.UTC),
            datetime.datetime(2015, 1, 15, 12, 0, 0, 0, pytz.UTC),
            datetime.datetime(2015, 1, 15, 12, 0, 0, 0, pytz.UTC),
            datetime.datetime(2015, 2, 15, 12, 0, 0, 0, pytz.UTC),
        ]
        articles = []
        for d in dates:
            article = self.create_article(publishing_date=d)
            articles.append(article)

        response = self.client.get(self.page.get_absolute_url())
        needle = '<a href="/en/page/{year}/{month}/"[^>]*>[^<]*<span class="badge">{num}</span>'
        month1 = needle.format(year=2014, month=11, num=2)
        month2 = needle.format(year=2015, month=2, num=1)
        month3 = needle.format(year=2015, month=1, num=3)
        self.assertRegexpMatches(str(response), month1)
        self.assertRegexpMatches(str(response), month2)
        self.assertRegexpMatches(str(response), month3)


class TestArticleSearchPlugin(TestAppConfigPluginsBase):
    """Simply tests that the plugin form renders on the page."""
    # This is a really weak test. To do more, we'll have to submit the form,
    # yadda yadda yadda. Test_views.py should already test the other side of
    # this.
    plugin_to_test = 'NewsBlogArticleSearchPlugin'
    plugin_params = {
        "max_articles": 5,
    }

    def test_article_search_plugin(self):
        needle = '<input type="hidden" name="max_articles" value="{num}">'
        response = self.client.get(self.page.get_absolute_url())
        self.assertContains(response, needle.format(num=5))


class TestAuthorsPlugin(TestAppConfigPluginsBase):
    plugin_to_test = 'NewsBlogAuthorsPlugin'

    def test_authors_plugin(self):
        author1, author2 = self.create_person(), self.create_person()
        # Published, author1 articles in our current namespace
        author1_articles = []
        for _ in range(3):
            article = self.create_article(author=author1)
            author1_articles.append(article)

        # Published, author2 articles in our current namespace
        other_articles = []
        for _ in range(5):
            article = self.create_article(author=author2)
            other_articles.append(article)

        # Unpublished, author1 articles in our current namespace
        for _ in range(7):
            article = self.create_article(
                author=author1,
                is_published=False
            )
            other_articles.append(article)

        # Published, author1 articles in a different namespace
        other_articles.append(self.create_article(
            author=author1,
            app_config=self.another_app_config
        ))

        # REQUIRED DUE TO USE OF RAW QUERIES
        time.sleep(1)

        response = self.client.get(self.page.get_absolute_url())
        pattern = '<p class="author"><a href="{url}"></a>'
        pattern += '</p>\s*<p[^>]*></p>\s*<p class="badge">{num}</p>'
        author1_pattern = pattern.format(
            num=3,
            url=reverse(
                '{0}:article-list-by-author'.format(self.app_config.namespace),
                args=[author1.slug]
            )
        )
        author2_pattern = pattern.format(
            num=5,
            url=reverse(
                '{0}:article-list-by-author'.format(self.app_config.namespace),
                args=[author2.slug]
            )
        )
        self.assertRegexpMatches(str(response), author1_pattern)
        self.assertRegexpMatches(str(response), author2_pattern)


class TestCategoriesPlugin(TestAppConfigPluginsBase):
    plugin_to_test = 'NewsBlogCategoriesPlugin'

    def test_categories_plugin(self):
        # Published, category1 articles in our current namespace
        cat1_articles = []
        for _ in range(3):
            article = self.create_article()
            article.categories.add(self.category1)
            cat1_articles.append(article)

        # Published category2 articles in our namespace
        other_articles = []
        for _ in range(5):
            article = self.create_article()
            article.categories.add(self.category2)
            other_articles.append(article)

        # Some tag1, but unpublished articles
        for _ in range(7):
            article = self.create_article(is_published=False)
            article.categories.add(self.category1)
            other_articles.append(article)

        # Some tag1 articles in another namespace
        for _ in range(1):
            article = self.create_article(app_config=self.another_app_config)
            article.categories.add(self.category1)
            other_articles.append(article)

        # REQUIRED DUE TO USE OF RAW QUERIES
        time.sleep(1)

        response = self.client.get(self.page.get_absolute_url())
        pattern = '<span[^>]*>{num}</span>\s*<a href=[^>]*>{name}</a>'
        needle1 = pattern.format(num=3, name=self.category1.name)
        needle2 = pattern.format(num=5, name=self.category2.name)
        self.assertRegexpMatches(str(response), needle1)
        self.assertRegexpMatches(str(response), needle2)


class TestFeaturedArticlesPlugin(TestAppConfigPluginsBase):
    plugin_to_test = 'NewsBlogFeaturedArticlesPlugin'
    plugin_params = {
        "article_count": 5,
    }

    def test_featured_articles_plugin(self):
        featured_articles = [self.create_article(
            is_featured=True,
            is_published=True
        ) for _ in range(3)]
        # Some featured articles but unpublished articles
        other_articles = [self.create_article(
            is_featured=True,
            is_published=False
        ) for _ in range(3)]
        # Some non-featured articles in the same namespace
        other_articles += [self.create_article() for _ in range(3)]
        # Some featured articles in another namespace
        other_articles += [self.create_article(
            is_featured=True,
            app_config=self.another_app_config
        ) for _ in range(3)]

        response = self.client.get(self.page.get_absolute_url())
        for article in featured_articles:
            self.assertContains(response, article.title)
        for article in other_articles:
            self.assertNotContains(response, article.title)


class TestLatestArticlesPlugin(TestAppConfigPluginsBase):
    plugin_to_test = 'NewsBlogLatestArticlesPlugin'
    plugin_params = {
        "latest_articles": 7,
    }

    def test_latest_articles_plugin(self):
        articles = [self.create_article() for _ in range(7)]
        another_app_config = NewsBlogConfig.objects.create(namespace='another')
        another_articles = [self.create_article(app_config=another_app_config)
                            for _ in range(3)]
        response = self.client.get(self.page.get_absolute_url())
        for article in articles:
            self.assertContains(response, article.title)
        for article in another_articles:
            self.assertNotContains(response, article.title)


class TestRelatedArticlesPlugin(NewsBlogTestsMixin, TransactionTestCase):

    def test_related_articles_plugin(self):
        main_article = self.create_article(app_config=self.app_config)
        self.placeholder = self.app_config.placeholder_detail_top
        api.add_plugin(self.placeholder, 'NewsBlogRelatedPlugin', self.language)
        self.plugin = self.placeholder.get_plugins()[0].get_plugin_instance()[0]
        self.plugin.save()
        self.page.publish(self.language)

        main_article.save()
        for _ in range(3):
            a = self.create_article()
            a.save()
            main_article.related.add(a)
        self.assertEquals(main_article.related.count(), 3)
        unrelated = []
        for _ in range(5):
            unrelated.append(self.create_article())

        response = self.client.get(main_article.get_absolute_url())
        for article in main_article.related.all():
            self.assertContains(response, article.title)
        for article in unrelated:
            self.assertNotContains(response, article.title)


class TestTagsPlugin(TestAppConfigPluginsBase):
    plugin_to_test = 'NewsBlogTagsPlugin'

    def test_tags_plugin(self):
        # Published, tag1-tagged articles in our current namespace
        self.create_tagged_articles(3, tags=['tag1'])['tag1']
        other_articles = self.create_tagged_articles(5, tags=['tag2'])['tag2']
        # Some tag1, but unpublished articles
        other_articles += self.create_tagged_articles(
            7, tags=['tag1'], is_published=False)['tag1']
        # Some tag1 articles in another namespace
        other_articles += self.create_tagged_articles(
            1, tags=['tag1'], app_config=self.another_app_config)['tag1']

        # REQUIRED DUE TO USE OF RAW QUERIES
        time.sleep(1)

        response = self.client.get(self.page.get_absolute_url())
        self.assertRegexpMatches(str(response), 'tag1\s*<span[^>]*>3</span>')
        self.assertRegexpMatches(str(response), 'tag2\s*<span[^>]*>5</span>')
