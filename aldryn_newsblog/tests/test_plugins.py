# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TransactionTestCase
from django.utils.timezone import now
from django.utils.translation import activate

from aldryn_newsblog.models import Article, NewsBlogConfig
# from aldryn_newsblog.search_indexes import ArticleIndex
# from aldryn_people.models import Person
# from aldryn_reversion.core import create_revision_with_placeholders
# from aldryn_search.helpers import get_request
from cms import api
# from cms.utils import get_cms_setting
# from easy_thumbnails.files import get_thumbnailer
# from filer.models.imagemodels import Image
# from parler.tests.utils import override_parler_settings
# from parler.utils.conf import add_default_language_settings
# from parler.utils.context import switch_language, smart_override

from . import NewsBlogTestsMixin


class TestPlugins(NewsBlogTestsMixin, TransactionTestCase):

    def test_latest_articles_plugin(self):
        page = api.create_page(
            'plugin page', self.template, self.language,
            parent=self.root_page, published=True)
        placeholder = page.placeholders.all()[0]
        api.add_plugin(placeholder, 'NewsBlogLatestArticlesPlugin',
                       self.language, app_config=self.app_config,
                       latest_articles=7)
        plugin = placeholder.get_plugins()[0].get_plugin_instance()[0]
        plugin.save()
        page.publish(self.language)
        articles = [self.create_article() for _ in range(7)]
        another_app_config = NewsBlogConfig.objects.create(namespace='another')
        another_articles = [self.create_article(app_config=another_app_config)
                            for _ in range(3)]
        response = self.client.get(page.get_absolute_url())
        for article in articles:
            self.assertContains(response, article.title)
        for article in another_articles:
            self.assertNotContains(response, article.title)

    def test_has_content(self):
        # Just make sure we have a known language
        activate(self.language)
        title = self.rand_str()
        content = self.rand_str()
        author = self.create_person()
        article = Article.objects.create(
            title=title, slug=self.rand_str(), author=author, owner=author.user,
            app_config=self.app_config, publishing_date=now())
        article.save()
        api.add_plugin(article.content, 'TextPlugin', self.language)
        plugin = article.content.get_plugins()[0].get_plugin_instance()[0]
        plugin.body = content
        plugin.save()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title)
        self.assertContains(response, content)

