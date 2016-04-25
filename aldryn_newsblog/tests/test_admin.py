# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.test import TransactionTestCase
from django.test.utils import override_settings
from djangocms_helper.utils import create_user
from cms.utils.urlutils import admin_reverse

from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from aldryn_newsblog.models import Article
from aldryn_people.models import Person

from . import NewsBlogTestsMixin, NewsBlogTransactionTestCase


class AdminTest(NewsBlogTestsMixin, TransactionTestCase):

    def test_admin_owner_default(self):
        from django.contrib import admin
        admin.autodiscover()
        # since we now have data migration to create the default
        # NewsBlogConfig (if migrations were not faked, django >1.7)
        # we need to delete one of configs to be sure that it is pre selected
        # in the admin view.
        if NewsBlogConfig.objects.count() > 1:
            # delete the app config that was created during test set up.
            NewsBlogConfig.objects.filter(namespace='NBNS').delete()
        user = self.create_user()
        user.is_superuser = True
        user.save()

        Person.objects.create(user=user, name=u' '.join(
            (user.first_name, user.last_name)))

        admin_inst = admin.site._registry[Article]
        self.request = self.get_request('en')
        self.request.user = user
        self.request.META['HTTP_HOST'] = 'example.com'
        response = admin_inst.add_view(self.request)
        option = '<option value="1" selected="selected">%s</option>'
        self.assertContains(response, option % user.username)
        self.assertContains(response, option % user.get_full_name())


# session engine is hardcoded in djangocms-helper (atm v0.9.4), so override
# per test case
@override_settings(SESSION_ENGINE='django.contrib.sessions.backends.cached_db')
class AdminViewsTestCase(NewsBlogTransactionTestCase):
    tag_html = '<p>no html</p>'
    escaped_tag_html = '&lt;p&gt;no html&lt;/p&gt;'
    change_view = 'aldryn_newsblog_article_change'
    change_list_view = 'aldryn_newsblog_article_changelist'

    def setUp(self):
        super(AdminViewsTestCase, self).setUp()
        username = 'admin_user'
        password = 'test'
        self.admin_user = create_user(
            username=username,
            email='test@example.com',
            password=password,
            is_superuser=True,
        )
        self.client.login(username=username, password=password)

    def get_object(self):
        return self.create_article()

    def add_tag_with_html(self, obj):
        obj.tags.add(self.tag_html)

    def _test_admin_view(self, view_name, args=None):
        view_url = admin_reverse(view_name, args=args)
        response = self.client.get(view_url)
        # ensure that html was escaped
        self.assertNotContains(response, self.tag_html)

    def test_admin_change_veiw(self):
        article = self.get_object()
        self.add_tag_with_html(article)
        self._test_admin_view(
            view_name=self.change_view,
            args=[article.pk])

    def test_admin_changelist_veiw(self):
        article = self.get_object()
        self.add_tag_with_html(article)
        self._test_admin_view(view_name=self.change_list_view)
