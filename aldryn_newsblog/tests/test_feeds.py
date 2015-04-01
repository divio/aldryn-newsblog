# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from datetime import timedelta

from django.core.urlresolvers import reverse
from django.test import TransactionTestCase
from django.utils.timezone import now
from django.utils.translation import override

from aldryn_newsblog.feeds import LatestArticlesFeed, TagFeed, CategoryFeed

from . import NewsBlogTestsMixin


class TestFeeds(NewsBlogTestsMixin, TransactionTestCase):

    def test_latest_feeds(self):
        article = self.create_article()
        future_article = self.create_article(
            publishing_date=now() + timedelta(days=3))
        self.request.current_page = self.page
        self.request.path = reverse(
            '{0}:article-list-feed'.format(self.app_config.namespace)
        )
        feed = LatestArticlesFeed()(self.request)

        self.assertContains(feed, article.title)
        self.assertNotContains(feed, future_article.title)

    def test_tag_feed(self):
        articles = self.create_tagged_articles()
        self.request.current_page = self.page
        self.request.path = reverse(
            '{0}:article-list-by-tag-feed'.format(self.app_config.namespace),
            args=['tag1']
        )
        feed = TagFeed()(self.request, 'tag1')

        for article in articles['tag1']:
            self.assertContains(feed, article.title)
        for different_tag_article in articles['tag2']:
            self.assertNotContains(feed, different_tag_article.title)

    def test_category_feed(self):
        with override(self.category1.get_current_language()):
            article = self.create_article()
            article.categories.add(self.category1)
            different_category_article = self.create_article()
            different_category_article.categories.add(self.category2)

            self.request.current_page = self.page
            self.request.path = reverse(
                '{0}:article-list-by-category-feed'.format(
                    self.app_config.namespace),
                args=[self.category1.slug]
            )

            feed = CategoryFeed()(self.request, self.category1.slug)

            self.assertContains(feed, article.title)
            self.assertNotContains(feed, different_category_article.title)
