# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from aldryn_newsblog.models import Article

from . import NewsBlogTestCase


class TestManagers(NewsBlogTestCase):

    def test_published_articles_filtering(self):
        for i in range(5):
            self.create_article()
        unpublised_article = Article.objects.first()
        unpublised_article.is_published = False
        unpublised_article.save()
        self.assertEqual(Article.objects.published().count(), 4)
        self.assertNotIn(unpublised_article, Article.objects.published())

    # TODO: Should also test for publishing_date
    def test_view_article_not_published(self):
        article = self.create_article(is_published=False)
        article_url = article.get_absolute_url()
        response = self.client.get(article_url)
        self.assertEqual(response.status_code, 404)
