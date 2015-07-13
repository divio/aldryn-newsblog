# -*- coding: utf-8 -*-
import os
import shutil

from django.conf import settings
from django.utils.timezone import now
from django.utils.translation import activate

from aldryn_newsblog.models import Article
from aldryn_newsblog.search_indexes import ArticleIndex

from . import NewsBlogTestCase


class ArticleIndexingTests(NewsBlogTestCase):

    def get_index(self):
        return ArticleIndex()

    def test_article_is_indexed_using_prepare(self):
        from haystack.constants import DEFAULT_ALIAS

        activate(self.language)

        user = self.create_user()

        lead_in = 'Hello! this text will be searchable.'

        article = Article.objects.create(
            title=self.rand_str(),
            owner=user,
            lead_in=lead_in,
            app_config=self.app_config,
            publishing_date=now()
        )
        article.save()

        index = self.get_index()
        index._backend_alias = DEFAULT_ALIAS

        data = index.prepare(article)

        count = data['text'].count(lead_in)

        self.assertTrue(count != 0, "Couldn't find %s in response" % lead_in)

    def test_translated_article_is_indexed_using_prepare(self):
        from haystack.constants import DEFAULT_ALIAS

        activate(self.language)

        user = self.create_user()

        lead_in = 'Hello! this text will be searchable.'

        # create english article
        article = Article.objects.create(
            title=self.rand_str(),
            owner=user,
            lead_in=lead_in,
            app_config=self.app_config,
            publishing_date=now()
        )
        article.save()

        # create german translation for article
        article.set_current_language('de')
        article.title = '%s [de]' % self.rand_str()
        article.save()

        index = self.get_index()
        index._backend_alias = DEFAULT_ALIAS

        data = index.prepare(article)

        self.assertEquals(data['language'], 'de')
        self.assertEquals(data['url'], article.get_absolute_url('de'))
