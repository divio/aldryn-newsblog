# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os

from django.test import TransactionTestCase
from django.utils.timezone import now
from django.utils.translation import activate

from aldryn_newsblog.models import Article
from cms import api

from . import NewsBlogTestsMixin, TESTS_STATIC_ROOT

FEATURED_IMAGE_PATH = os.path.join(TESTS_STATIC_ROOT, 'featured_image.jpg')


class TestModels(NewsBlogTestsMixin, TransactionTestCase):

    def test_create_article(self):
        article = self.create_article()
        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, article.title)

    def test_delete_article(self):
        article = self.create_article()
        article_pk = article.pk
        article_url = article.get_absolute_url()
        response = self.client.get(article_url)
        self.assertContains(response, article.title)
        Article.objects.get(pk=article_pk).delete()
        response = self.client.get(article_url)
        self.assertEqual(response.status_code, 404)

    def test_auto_slugifies(self):
        activate(self.language)
        title = u'This is a title'
        author = self.create_person()
        article = Article.objects.create(
            title=title, author=author, owner=author.user,
            app_config=self.app_config, publishing_date=now())
        article.save()
        self.assertEquals(article.slug, 'this-is-a-title')
        # Now, let's try another with the same title
        article.id = None
        # Note, it cannot be the exact same title, else we'll fail the unique
        # constraint on the field.
        article.title = title.lower()
        article.save()
        # Note that this should be "incremented" slug here.
        self.assertEquals(article.slug, 'this-is-a-title_1')
        article.id = None
        article.title = title.upper()
        article.save()
        self.assertEquals(article.slug, 'this-is-a-title_2')

    def test_auto_existing_author(self):
        author = self.create_person()
        article = Article.objects.create(
            title=self.rand_str(), owner=author.user,
            app_config=self.app_config, publishing_date=now())
        article.save()
        self.assertEquals(article.author.user, article.owner)

        old = self.app_config.create_authors
        self.app_config.create_authors = False
        self.app_config.save()
        article = Article.objects.create(
            title=self.rand_str(), owner=author.user,
            app_config=self.app_config, publishing_date=now())
        self.app_config.create_authors = old
        self.app_config.save()
        self.assertEquals(article.author, None)

    def test_auto_new_author(self):
        user = self.create_user()
        article = Article.objects.create(
            title=self.rand_str(), owner=user,
            app_config=self.app_config, publishing_date=now())
        article.save()
        self.assertEquals(article.author.name,
                          u' '.join((user.first_name, user.last_name)))

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
