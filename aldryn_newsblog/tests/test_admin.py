# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.test import TransactionTestCase

from aldryn_newsblog.cms_appconfig import NewsBlogConfig
from aldryn_newsblog.models import Article
from aldryn_people.models import Person

from . import NewsBlogTestsMixin


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
        option = r'<option value="{}" (selected="selected"|selected)>%s<\/option>'.format(
            user.pk,
        )
        self.assertRegexpMatches(response.rendered_content, option % user.username)
        self.assertRegexpMatches(response.rendered_content, option % user.get_full_name())
