# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from django.core.urlresolvers import reverse

from reversion.revisions import default_revision_manager
try:
    from reversion import create_revision
except ImportError:
    # django-reversion >=1.9
    from reversion.revisions import create_revision

import six

from django.db import transaction

from aldryn_reversion.core import create_revision as aldryn_create_revision

from parler.utils.context import switch_language

from . import NewsBlogTestCase
from aldryn_newsblog.cms_appconfig import NewsBlogConfig


class TestVersioning(NewsBlogTestCase):
    def create_revision(self, article, content=None, language=None, **kwargs):
        with transaction.atomic():
            with create_revision():
                for k, v in six.iteritems(kwargs):
                    setattr(article, k, v)
                if content:
                    plugins = article.content.get_plugins()
                    plugin = plugins[0].get_plugin_instance()[0]
                    plugin.body = content
                    plugin.save()
                # TODO: Cover both cases (plugin modification/recreation)
                # if content:
                #     article.content.get_plugins().delete()
                #     api.add_plugin(article.content, 'TextPlugin',
                #                    self.language, body=content)
                article.save()

    def revert_to(self, article, revision):
        (default_revision_manager.get_for_object(article)[revision]
                                 .revision.revert())

    def test_revert_revision(self):
        title1 = self.rand_str(prefix='title1_')
        title2 = self.rand_str(prefix='title2_')

        content0 = self.rand_str(prefix='content0_')
        content1 = self.rand_str(prefix='content1_')
        content2 = self.rand_str(prefix='content2_')

        article = self.create_article(content=content0)

        # Revision 1
        self.create_revision(article, title=title1, content=content1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1)
        self.assertContains(response, content1)
        self.assertNotContains(response, content0)

        # Revision 2
        self.create_revision(article, title=title2, content=content2)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2)
        self.assertContains(response, content2)
        self.assertNotContains(response, content1)

        # Revert to revision 1
        self.revert_to(article, 1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title1)
        self.assertContains(response, content1)
        self.assertNotContains(response, content0)
        self.assertNotContains(response, content2)

    def test_revert_translated_revision(self):
        title1_en = self.rand_str(prefix='title1_en_')
        title1_de = self.rand_str(prefix='title1_de_')
        title2_en = self.rand_str(prefix='title2_en_')
        title2_de = self.rand_str(prefix='title2_de_')

        article = self.create_article()

        # Revision 1
        article.set_current_language('en')
        self.create_revision(article, title=title1_en)

        article.set_current_language('de')
        self.create_revision(article, title=title1_de)

        with switch_language(article, 'en'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revision 2a (modify just EN)
        article.set_current_language('en')
        self.create_revision(article, title=title2_en)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, title2_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revision 2b (modify just DE)
        article.set_current_language('de')
        self.create_revision(article, title=title2_de)

        with switch_language(article, 'en'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title2_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title2_de)

        # Revert to revision 2a (EN=2, DE=1)
        self.revert_to(article, 1)

        with switch_language(article, 'en'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title2_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

        # Revert to revision 1 (EN=1, DE=1)
        self.revert_to(article, 2)

        with switch_language(article, 'en'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_en)

        with switch_language(article, 'de'):
            response = self.client.get(article.get_absolute_url())
            self.assertContains(response, title1_de)

    def test_edit_plugin_directly(self):
        content0 = self.rand_str(prefix='content0_')
        content1 = self.rand_str(prefix='content1_')
        content2 = self.rand_str(prefix='content2_')

        article = self.create_article(content=content0)

        # Revision 1
        self.create_revision(article, content=content1)

        self.assertEqual(
            len(default_revision_manager.get_for_object(article)), 1)

        # Revision 2
        with transaction.atomic():
            plugins = article.content.get_plugins()
            plugin = plugins[0].get_plugin_instance()[0]
            plugin.body = content2
            plugin.save()
            aldryn_create_revision(article)

        self.assertEqual(
            len(default_revision_manager.get_for_object(article)), 2)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, content2)
        self.assertNotContains(response, content1)

        # Revert to revision 1
        self.revert_to(article, 1)

        response = self.client.get(article.get_absolute_url())
        self.assertContains(response, content1)
        self.assertNotContains(response, content2)

    def test_blog_config_recovery_accessible(self):
        with transaction.atomic():
            with create_revision():
                new_conf = NewsBlogConfig(
                    namespace='test_revocery_admin_url', paginate_by=15)
                new_conf.save()
        new_config_version = (default_revision_manager
                              .get_for_object(new_conf)[0])
        new_config_pk = new_conf.pk
        self.assertEqual(NewsBlogConfig.objects.filter(
            pk=new_config_pk).count(), 1)
        new_conf.delete()
        self.assertEqual(NewsBlogConfig.objects.filter(
            pk=new_config_pk).count(), 0)

        # check that there is a a way to access recovery view
        obj = new_config_version.object_version.object
        opts = obj._meta
        url = reverse(
            'admin:{0}_{1}_{2}'.format(
                opts.app_label,
                obj._meta.model_name,
                'recover'),
            args=[new_config_version.pk])
        # ust in case check the length, but at this step either a
        # NoReverseMatch should occur or other error,
        # if no exception is raised, it is a good sign
        self.assertGreater(len(url), 4)
