# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import random
import string

from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.utils.translation import override

from aldryn_categories.models import Category
from aldryn_categories.tests import CategoryTestCaseMixin
from aldryn_newsblog.models import Article, NewsBlogConfig
from aldryn_people.models import Person
from aldryn_search.helpers import get_request
from cms import api
from cms.utils import get_cms_setting
from parler.utils.context import switch_language

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
TESTS_STATIC_ROOT = os.path.abspath(os.path.join(TESTS_ROOT, 'static'))


class NewsBlogTestsMixin(CategoryTestCaseMixin):

    @classmethod
    def rand_str(cls, prefix=u'', length=23, chars=string.ascii_letters):
        return prefix + u''.join(random.choice(chars) for _ in range(length))

    @classmethod
    def create_user(cls):
        return User.objects.create(username=cls.rand_str(), first_name=cls.rand_str(),
                                   last_name=cls.rand_str())

    def create_person(self):
        return Person.objects.create(user=self.create_user(), slug=self.rand_str())

    def create_article(self, content=None, **kwargs):
        try:
            author = kwargs['author']
        except KeyError:
            author = self.create_person()
        try:
            owner = kwargs['owner']
        except KeyError:
            owner = author.user

        fields = {
            'title': self.rand_str(),
            'slug': self.rand_str(),
            'author': author,
            'owner': owner,
            'app_config': self.app_config,
            'publishing_date': now(),
            'is_published': True,
        }

        fields.update(kwargs)

        article = Article.objects.create(**fields)

        if content:
            api.add_plugin(article.content, 'TextPlugin',
                           self.language, body=content)
        return article

    def create_tagged_articles(self, num_articles=3, tags=('tag1', 'tag2'),
                               **kwargs):
        """Create num_articles Articles for each tag"""
        articles = {}
        for tag_name in tags:
            tagged_articles = []
            for _ in range(num_articles):
                article = self.create_article(**kwargs)
                article.save()
                article.tags.add(tag_name)
                tagged_articles.append(article)
            tag_slug = tagged_articles[0].tags.slugs()[0]
            articles[tag_slug] = tagged_articles
        return articles

    def setup_categories(self):
        """
        Sets-up i18n categories (self.category_root, self.category1 and
        self.category2) for use in tests
        """
        self.language = settings.LANGUAGES[0][0]

        categories = []
        # Set the default language, create the objects
        with override(self.language):
            code = "{0}-".format(self.language)
            self.category_root = Category.add_root(
                name=self.rand_str(prefix=code, length=8))
            categories.append(self.category_root)
            self.category1 = self.category_root.add_child(
                name=self.rand_str(prefix=code, length=8))
            categories.append(self.category1)
            self.category2 = self.category_root.add_child(
                name=self.rand_str(prefix=code, length=8))
            categories.append(self.category2)

        # We should reload category_root, since we modified its children.
        self.category_root = self.reload(self.category_root)

        # Setup the other language(s) translations for the categories
        for language, _ in settings.LANGUAGES[1:]:
            for category in categories:
                with switch_language(category, language):
                    code = "{0}-".format(language)
                    category.name = self.rand_str(prefix=code, length=8)
                    category.save()

    def setUp(self):
        self.template = get_cms_setting('TEMPLATES')[0][0]
        self.language = settings.LANGUAGES[0][0]
        self.root_page = api.create_page(
            'root page', self.template, self.language, published=True)
        self.app_config = NewsBlogConfig.objects.create(
            namespace='NBNS', paginate_by=15)
        self.page = api.create_page(
            'page', self.template, self.language, published=True,
            parent=self.root_page,
            apphook='NewsBlogApp',
            apphook_namespace=self.app_config.namespace)
        self.placeholder = self.page.placeholders.all()[0]
        self.request = get_request('en')

        self.setup_categories()

        for page in self.root_page, self.page:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, page.get_slug(), page)
                page.publish(language)
