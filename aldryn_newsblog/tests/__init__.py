# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import os
import random
import string
import sys

from django.conf import settings
from django.contrib.auth.models import AnonymousUser, User
from django.core.urlresolvers import clear_url_caches
from django.core.cache import cache
from django.test import RequestFactory
from django.utils.timezone import now
from django.utils.translation import override
from aldryn_categories.models import Category
from aldryn_newsblog.cms_apps import NewsBlogApp
from aldryn_newsblog.models import Article, NewsBlogConfig
from aldryn_people.models import Person
from cms import api
from cms.apphook_pool import apphook_pool
from cms.appresolver import clear_app_resolvers
from cms.exceptions import AppAlreadyRegistered
from cms.test_utils.testcases import CMSTestCase, TransactionCMSTestCase
from cms.utils import get_cms_setting

from cms.toolbar.toolbar import CMSToolbar


from parler.utils.context import switch_language

TESTS_ROOT = os.path.abspath(os.path.dirname(__file__))
TESTS_STATIC_ROOT = os.path.abspath(os.path.join(TESTS_ROOT, 'static'))


class NewsBlogTestsMixin(object):

    NO_REDIRECT_CMS_SETTINGS = {
        1: [
            {
                'code': 'de',
                'name': 'Deutsche',
                'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'fr' HERE
            },
            {
                'code': 'fr',
                'name': 'Française',
                'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'de' HERE
            },
            {
                'code': 'en',
                'name': 'English',
                'fallbacks': ['de', 'fr', ]
            },
            {
                'code': 'it',
                'name': 'Italiano',
                'fallbacks': ['fr', ]  # FOR TESTING, LEAVE AS ONLY 'fr'
            },
        ],
        'default': {
            'redirect_on_fallback': False,
        }
    }

    @staticmethod
    def reload(node):
        """NOTE: django-treebeard requires nodes to be reloaded via the Django
        ORM once its sub-tree is modified for the API to work properly.

        See:: https://tabo.pe/projects/django-treebeard/docs/2.0/caveats.html

        This is a simple helper-method to do that."""
        return node.__class__.objects.get(id=node.id)

    @classmethod
    def rand_str(cls, prefix=u'', length=23, chars=string.ascii_letters):
        return prefix + u''.join(random.choice(chars) for _ in range(length))

    @classmethod
    def create_user(cls):
        return User.objects.create(
            username=cls.rand_str(), first_name=cls.rand_str(),
            last_name=cls.rand_str())

    def create_person(self):
        return Person.objects.create(
            user=self.create_user(), slug=self.rand_str())

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
        # save again to calculate article search_data.
        article.save()

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

    @staticmethod
    def get_request(language=None, url="/"):
        """
        Returns a Request instance populated with cms specific attributes.
        """
        request_factory = RequestFactory(HTTP_HOST=settings.ALLOWED_HOSTS[0])
        request = request_factory.get(url)
        request.session = {}
        request.LANGUAGE_CODE = language or settings.LANGUAGE_CODE
        # Needed for plugin rendering.
        request.current_page = None
        request.user = AnonymousUser()
        request.toolbar = CMSToolbar(request)
        return request

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
        self.plugin_page = api.create_page(
            title="plugin_page", template=self.template, language=self.language,
            parent=self.root_page, published=True)
        self.placeholder = self.page.placeholders.all()[0]

        self.setup_categories()

        for page in self.root_page, self.page:
            for language, _ in settings.LANGUAGES[1:]:
                api.create_title(language, page.get_slug(), page)
                page.publish(language)


class CleanUpMixin(object):
    apphook_object = None

    def tearDown(self):
        """
        Do a proper cleanup, delete everything what is preventing us from
        clean environment for tests.
        :return: None
        """
        self.app_config.delete()
        self.reset_all()
        cache.clear()
        super(CleanUpMixin, self).tearDown()

    def get_apphook_object(self):
        return self.apphook_object

    def reset_apphook_cmsapp(self, apphook_object=None):
        """
        For tests that should not be polluted by previous setup we need to
        ensure that app hooks are reloaded properly. One of the steps is to
        reset the relation between EventListAppHook and EventsConfig
        """
        if apphook_object is None:
            apphook_object = self.get_apphook_object()
        app_config = getattr(apphook_object, 'app_config', None)
        if (app_config and
                getattr(app_config, 'cmsapp', None)):
            delattr(apphook_object.app_config, 'cmsapp')
        if getattr(app_config, 'cmsapp', None):
            delattr(app_config, 'cmsapp')

    def reset_all(self):
        """
        Reset all that could leak from previous test to current/next test.
        :return: None
        """
        apphook_object = self.get_apphook_object()
        self.delete_app_module(apphook_object.__module__)
        self.reload_urls(apphook_object)
        self.apphook_clear()

    def delete_app_module(self, app_module=None):
        """
        Remove APP_MODULE from sys.modules. Taken from cms.
        :return: None
        """
        if app_module is None:
            apphook_object = self.get_apphook_object()
            app_module = apphook_object.__module__
        if app_module in sys.modules:
            del sys.modules[app_module]

    def apphook_clear(self):
        """
        Clean up apphook_pool and sys.modules. Taken from cms with slight
        adjustments and fixes.
        :return: None
        """
        try:
            apphooks = apphook_pool.get_apphooks()
        except AppAlreadyRegistered:
            # there is an issue with discover apps, or i'm using it wrong.
            # setting discovered to True solves it. Maybe that is due to import
            # from aldryn_events.cms_apps which registers EventListAppHook
            apphook_pool.discovered = True
            apphooks = apphook_pool.get_apphooks()

        for name, label in list(apphooks):
            if apphook_pool.apps[name].__class__.__module__ in sys.modules:
                del sys.modules[apphook_pool.apps[name].__class__.__module__]
        apphook_pool.clear()
        self.reset_apphook_cmsapp()

    def reload_urls(self, apphook_object=None):
        """
        Clean up url related things (caches, app resolvers, modules).
        Taken from cms.
        :return: None
        """
        if apphook_object is None:
            apphook_object = self.get_apphook_object()
        app_module = apphook_object.__module__
        package = app_module.split('.')[0]
        clear_app_resolvers()
        clear_url_caches()
        url_modules = [
            'cms.urls',
            '{0}.urls'.format(package),
            settings.ROOT_URLCONF
        ]

        for module in url_modules:
            if module in sys.modules:
                del sys.modules[module]


class NewsBlogTestCase(CleanUpMixin, NewsBlogTestsMixin, CMSTestCase):
    apphook_object = NewsBlogApp
    pass


class NewsBlogTransactionTestCase(CleanUpMixin,
                                  NewsBlogTestsMixin,
                                  TransactionCMSTestCase):
    apphook_object = NewsBlogApp
    pass
