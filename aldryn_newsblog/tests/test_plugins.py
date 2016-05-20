# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import time
import datetime
import pytz

from django.core.cache import cache
from django.core.urlresolvers import reverse
from django.utils.translation import force_text, override

from aldryn_newsblog.models import NewsBlogConfig
from cms import api
from cms.models import StaticPlaceholder

from . import NewsBlogTestCase


class TestAppConfigPluginsBase(NewsBlogTestCase):
    plugin_to_test = 'TextPlugin'
    plugin_params = {}

    def setUp(self):
        super(TestAppConfigPluginsBase, self).setUp()
        self.placeholder = self.plugin_page.placeholders.all()[0]
        api.add_plugin(
            self.placeholder, self.plugin_to_test, self.language,
            app_config=self.app_config, **self.plugin_params)
        self.plugin = self.placeholder.get_plugins()[0].get_plugin_instance()[0]
        self.plugin.save()
        self.plugin_page.publish(self.language)
        self.another_app_config = NewsBlogConfig.objects.create(
            namespace=self.rand_str())


class TestPluginLanguageHelperMixin(object):
    def _test_plugin_languages_with_article(self, article):
        """Set up conditions to test plugin languages edge cases"""
        # Add 'de' translation to one of the articles
        title_de = 'title-de'
        title_en = article.title
        article.set_current_language('de')
        article.title = title_de
        article.save()

        # Unpublish page with newsblog apphook
        self.page.unpublish('en')
        cache.clear()
        response = self.client.get(self.plugin_page.get_absolute_url())

        # This article should not be visible on 'en' page/plugin
        self.assertNotContains(response, title_en)


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
        response = self.client.get(self.plugin_page.get_absolute_url())
        response_content = force_text(response.content)
        needle = '<a href="/en/page/{year}/{month}/"[^>]*>'
        '[^<]*<span class="badge">{num}</span>'
        month1 = needle.format(year=2014, month=11, num=2)
        month2 = needle.format(year=2015, month=2, num=1)
        month3 = needle.format(year=2015, month=1, num=3)
        self.assertRegexpMatches(response_content, month1)
        self.assertRegexpMatches(response_content, month2)
        self.assertRegexpMatches(response_content, month3)


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
        response = self.client.get(self.plugin_page.get_absolute_url())
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

        response = self.client.get(self.plugin_page.get_absolute_url())
        response_content = force_text(response.content)
        # This pattern tries to accommodate all the templates from all the
        # versions of this package.
        pattern = '<a href="{url}">\s*</a>'
        author1_pattern = pattern.format(
            url=reverse(
                '{0}:article-list-by-author'.format(self.app_config.namespace),
                args=[author1.slug]
            )
        )
        author2_pattern = pattern.format(
            url=reverse(
                '{0}:article-list-by-author'.format(self.app_config.namespace),
                args=[author2.slug]
            )
        )
        self.assertRegexpMatches(response_content, author1_pattern)
        self.assertRegexpMatches(response_content, author2_pattern)


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

        response = self.client.get(self.plugin_page.get_absolute_url())
        response_content = force_text(response.content)
        # We use two different patterns in alternation because different
        # versions of newsblog have different templates
        pattern = '<span[^>]*>{num}</span>\s*<a href=[^>]*>{name}</a>'
        pattern += '|<a href=[^>]*>{name}</a>\s*<span[^>]*>{num}</span>'
        needle1 = pattern.format(num=3, name=self.category1.name)
        needle2 = pattern.format(num=5, name=self.category2.name)
        self.assertRegexpMatches(response_content, needle1)
        self.assertRegexpMatches(response_content, needle2)


class TestFeaturedArticlesPlugin(TestPluginLanguageHelperMixin,
                                 TestAppConfigPluginsBase):
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

        response = self.client.get(self.plugin_page.get_absolute_url())
        for article in featured_articles:
            self.assertContains(response, article.title)
        for article in other_articles:
            self.assertNotContains(response, article.title)

    def test_featured_articles_plugin_unpublished_app_page(self):
        with override('de'):
            articles = [self.create_article(is_featured=True)
                        for _ in range(3)]

        response = self.client.get(self.plugin_page.get_absolute_url())
        for article in articles:
            self.assertContains(response, article.title)

        self.page.unpublish('de')
        cache.clear()
        response = self.client.get(self.plugin_page.get_absolute_url())
        for article in articles:
            self.assertNotContains(response, article.title)

    def test_featured_articles_plugin_language(self):
        article = self.create_article(is_featured=True)
        self._test_plugin_languages_with_article(article)


class TestLatestArticlesPlugin(TestPluginLanguageHelperMixin,
                               TestAppConfigPluginsBase):
    plugin_to_test = 'NewsBlogLatestArticlesPlugin'
    plugin_params = {
        "latest_articles": 7,
    }

    def test_latest_articles_plugin(self):
        articles = [self.create_article() for _ in range(7)]
        another_app_config = NewsBlogConfig.objects.create(namespace='another')
        another_articles = [self.create_article(app_config=another_app_config)
                            for _ in range(3)]
        response = self.client.get(self.plugin_page.get_absolute_url())
        for article in articles:
            self.assertContains(response, article.title)
        for article in another_articles:
            self.assertNotContains(response, article.title)

    def _test_latest_articles_plugin_exclude_count(self, exclude_count=0):
        self.plugin.exclude_featured = exclude_count
        self.plugin.save()
        self.plugin_page.publish(self.plugin.language)
        articles = []
        featured_articles = []
        for idx in range(7):
            if idx % 2:
                featured_articles.append(self.create_article(is_featured=True))
            else:
                articles.append(self.create_article())
        response = self.client.get(self.plugin_page.get_absolute_url())
        for article in articles:
            self.assertContains(response, article.title)
        # check that configured among of featured articles is excluded
        for featured_article in featured_articles[:exclude_count]:
            self.assertNotContains(response, featured_article.title)
        # ensure that other articles featured articles are present
        for featured_article in featured_articles[exclude_count:]:
            self.assertContains(response, featured_article.title)

    def test_latest_articles_plugin_exclude_featured(self):
        self._test_latest_articles_plugin_exclude_count(3)

    def test_latest_articles_plugin_no_excluded_featured(self):
        self._test_latest_articles_plugin_exclude_count()

    def test_latest_articles_plugin_unpublished_app_page(self):
        with override('de'):
            articles = [self.create_article() for _ in range(3)]

        response = self.client.get(self.plugin_page.get_absolute_url())
        for article in articles:
            self.assertContains(response, article.title)

        self.page.unpublish('de')
        cache.clear()
        response = self.client.get(self.plugin_page.get_absolute_url())
        for article in articles:
            self.assertNotContains(response, article.title)

    def test_latest_articles_plugin_language(self):
        article = self.create_article()
        self._test_plugin_languages_with_article(article)


class TestPrefixedLatestArticlesPlugin(TestAppConfigPluginsBase):
    plugin_to_test = 'NewsBlogLatestArticlesPlugin'
    plugin_params = {
        "latest_articles": 7,
    }

    def setUp(self):
        super(TestPrefixedLatestArticlesPlugin, self).setUp()
        self.app_config.template_prefix = 'dummy'
        self.app_config.save()

    def test_latest_articles_plugin(self):
        response = self.client.get(self.plugin_page.get_absolute_url())
        self.assertContains(response, 'This is dummy latest articles plugin')


class TestRelatedArticlesPlugin(TestPluginLanguageHelperMixin,
                                NewsBlogTestCase):

    def test_related_articles_plugin(self):
        main_article = self.create_article(app_config=self.app_config)
        static_placeholder = StaticPlaceholder.objects.get_or_create(
            code='newsblog_social',
            site__isnull=True,
        )[0]
        placeholder = static_placeholder.draft
        api.add_plugin(placeholder, 'NewsBlogRelatedPlugin', self.language)

        static_placeholder.publish(None, language=self.language, force=True)

        plugin = placeholder.get_plugins()[0].get_plugin_instance()[0]
        plugin.save()

        self.plugin_page.publish(self.language)

        main_article.save()
        for _ in range(3):
            a = self.create_article()
            a.save()
            main_article.related.add(a)

        another_language_articles = []
        with override('de'):
            for _ in range(4):
                a = self.create_article()
                main_article.related.add(a)
                another_language_articles.append(a)

        self.assertEquals(main_article.related.count(), 7)
        unrelated = []
        for _ in range(5):
            unrelated.append(self.create_article())

        response = self.client.get(main_article.get_absolute_url())
        for article in main_article.related.all():
            self.assertContains(response, article.title)
        for article in unrelated:
            self.assertNotContains(response, article.title)

        self.page.unpublish('de')
        cache.clear()
        response = self.client.get(main_article.get_absolute_url())
        for article in another_language_articles:
            self.assertNotContains(response, article.title)

    def test_latest_articles_plugin_language(self):
        main_article, related_article = [
            self.create_article() for _ in range(2)]
        main_article.related.add(related_article)
        self._test_plugin_languages_with_article(related_article)


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

        response = self.client.get(self.plugin_page.get_absolute_url())
        response_content = force_text(response.content)
        self.assertRegexpMatches(response_content, 'tag1\s*<span[^>]*>3</span>')
        self.assertRegexpMatches(response_content, 'tag2\s*<span[^>]*>5</span>')
