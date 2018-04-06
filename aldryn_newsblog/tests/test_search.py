# -*- coding: utf-8 -*-
from django.utils.translation import activate

from aldryn_newsblog.search_indexes import ArticleIndex

from . import NewsBlogTestCase


class ArticleIndexingTests(NewsBlogTestCase):

    def get_index(self):
        from haystack.constants import DEFAULT_ALIAS

        index = ArticleIndex()
        index._backend_alias = DEFAULT_ALIAS
        return index

    def test_article_is_indexed_using_prepare(self):
        activate(self.language)

        lead_in = 'Hello! this text will be searchable.'

        article = self.create_article(lead_in=lead_in)
        # If set ALDRYN_NEWSBLOG_UPDATE_SEARCH_DATA_ON_SAVE this will do
        # automatically
        article.search_data = article.get_search_data()

        index = self.get_index()

        data = index.prepare(article)

        count = data['text'].count(lead_in)

        self.assertTrue(count != 0, "Couldn't find %s in text" % lead_in)

    def test_translated_article_is_indexed_using_prepare(self):
        activate(self.language)

        lead_in = 'Hello! this text will be searchable.'

        # create english article
        article = self.create_article(lead_in=lead_in)

        # create german translation for article
        article.set_current_language('de')
        article.title = '%s [de]' % self.rand_str()
        article.save()

        index = self.get_index()

        data = index.prepare(article)

        self.assertEquals(data['language'], 'de')
        self.assertEquals(data['url'], article.get_absolute_url('de'))

    def test_article_not_indexed_if_no_translation(self):
        index = self.get_index()
        # create english article
        article = self.create_article()

        # should the index be updated for this object? (yes)
        should_update = index.should_update(article)
        self.assertEquals(should_update, True)

        # remove all translations for article
        article.translations.all().delete()

        # should the index be updated for this object? (no)
        should_update = index.should_update(article)
        self.assertEquals(should_update, False)
