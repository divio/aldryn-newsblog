# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TransactionTestCase

from aldryn_newsblog.models import Article
from aldryn_people.models import Person

from . import NewsBlogTestsMixin


class AdminTest(NewsBlogTestsMixin, TransactionTestCase):

    def test_admin_owner_default(self):
        from django.contrib import admin
        admin.autodiscover()

        user = self.create_user()
        user.is_superuser = True
        user.save()

        Person.objects.create(user=user, name=u' '.join(
            (user.first_name, user.last_name)))

        admin_inst = admin.site._registry[Article]
        self.request.user = user
        self.request.META['HTTP_HOST'] = 'example.com'
        response = admin_inst.add_view(self.request)
        option = '<option value="1" selected="selected">%s</option>'
        self.assertContains(response, option % user.username)
        self.assertContains(response, option % user.get_full_name())
