# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from . import NewsBlogTestCase
from aldryn_newsblog.sitemaps import NewsBlogSitemap
from django.contrib.sites.models import get_current_site

class TestSitemaps(NewsBlogTestCase):

    def test_listening_all_instances(self):
        articles = [self.create_article() for _ in range(11)]
        unpublished_article = articles[0]
        unpublished_article.is_published = False
        unpublished_article.save()
        urls_info = NewsBlogSitemap().get_urls()
        urls = [url_info['location'] for url_info in urls_info]

        host = 'http://' + get_current_site(self.request).domain

        self.assertEqual(len(articles[1:]), len(urls))
        for article in articles[1:]:
            self.assertIn(host + article.get_absolute_url(), urls)
        self.assertNotIn(host + unpublished_article.get_absolute_url(), urls)

    def test_listening_namespace(self):
        articles = [self.create_article() for _ in range(11)]
        unpublished_article = articles[0]
        unpublished_article.is_published = False
        unpublished_article.save()
        urls_info = NewsBlogSitemap(
            namespace=self.app_config.namespace).get_urls()
        urls = [url_info['location'] for url_info in urls_info]

        host = 'http://' + get_current_site(self.request).domain

        self.assertEqual(len(articles[1:]), len(urls))
        for article in articles[1:]:
            self.assertIn(host + article.get_absolute_url(), urls)
        self.assertNotIn(host + unpublished_article.get_absolute_url(), urls)

    def test_listening_unexisting_namespace(self):
        articles = [self.create_article() for _ in range(11)]
        unpublished_article = articles[0]
        unpublished_article.is_published = False
        unpublished_article.save()
        sitemap = NewsBlogSitemap(
            namespace='not exists')
        self.assertFalse(sitemap.items())
