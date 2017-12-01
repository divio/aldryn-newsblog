# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from aldryn_newsblog.tests import NewsBlogTestCase
from aldryn_newsblog.cms_wizards import CreateNewsBlogArticleForm


class CreateNewsBlogArticleFormTestCase(NewsBlogTestCase):
    def get_form(self, has_content, has_permission):
        data = {'title': 'My super title', 'app_config': self.app_config.id}
        if has_content:
            data['content'] = 'My super content'

        form = CreateNewsBlogArticleForm(wizard_language='en', data=data)
        form.user = self.create_user(is_staff=has_permission, is_superuser=has_permission)
        self.assertTrue(form.is_valid())
        return form

    def test_article_is_saved_with_content_user_with_plugin_permission(self):
        form = self.get_form(has_content=True, has_permission=True)

        article = form.save()
        self.assertTrue(article.__class__.objects.filter(id=article.id).exists())
        self.assertEquals(article.content.get_plugins('en').count(), 1)
        plugin = article.content.get_plugins('en').get()
        self.assertEquals(plugin.plugin_type, 'TextPlugin')
        self.assertEquals(plugin.djangocms_text_ckeditor_text.body, 'My super content')

    def test_article_is_saved_without_content_with_plugin_permission(self):
        form = self.get_form(has_content=False, has_permission=True)

        article = form.save()
        self.assertTrue(article.__class__.objects.filter(id=article.id).exists())
        self.assertFalse(article.content.get_plugins('en').exists())

    def test_article_is_saved_with_content_without_plugin_permission(self):
        form = self.get_form(has_content=True, has_permission=False)

        article = form.save()
        self.assertTrue(article.__class__.objects.filter(id=article.id).exists())
        self.assertFalse(article.content.get_plugins('en').exists())

    def test_article_is_saved_without_content_without_plugin_permission(self):
        form = self.get_form(has_content=False, has_permission=False)

        article = form.save()
        self.assertTrue(article.__class__.objects.filter(id=article.id).exists())
        self.assertFalse(article.content.get_plugins('en').exists())
