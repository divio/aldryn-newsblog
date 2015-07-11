# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.management import call_command
from django.utils.translation import activate

from aldryn_newsblog.models import Article

from . import NewsBlogTestCase


class TestCommands(NewsBlogTestCase):

    def test_rebuild_search_data_command(self):
        # Just make sure we have a known language
        activate(self.language)

        article = self.create_article()

        search_data = article.get_search_data(language=self.language)

        # make sure the search_data is empty
        # we avoid any handler that automatically sets the search_data
        article.translations.filter(
            language_code=self.language).update(search_data='')

        # get fresh article from db
        article = Article.objects.language(self.language).get(pk=article.pk)

        # make sure search data is empty
        self.assertEqual(article.search_data, '')
        # now run the command
        call_command('rebuild_article_search_data', languages=[self.language])
        # now verify the article's search_data has been updated.
        self.assertEqual(article.search_data, search_data)
