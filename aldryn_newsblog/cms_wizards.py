# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _
from django import forms

from cms.wizards.wizard_pool import wizard_pool
from cms.wizards.wizard_base import Wizard

from parler.forms import TranslatableModelForm

from .models import Article


class NewsBlogArticleWizard(Wizard):

    def user_has_add_permission(self, user, **kwargs):
        """
        Return True if the current user has permission to add an article.
        :param user: The current user
        :param kwargs: Ignored here
        :return: True if user has add permission, else False
        """
        if user.is_superuser or user.has_perm("aldryn_newsblog.add_article"):
            return True
        return False


class CreateNewsBlogArticleForm(TranslatableModelForm):
    model = Article
    fields = ['title', 'app_config', 'is_featured', 'is_published', 'lead_in',
              'content', ]



newsblog_article_wizard = NewsBlogArticleWizard(
    title=_(u"New article"),
    weight=200,
    form=CreateNewsBlogArticleForm,
    description=_(u"Create a new article.")
)

wizard_pool.register(newsblog_article_wizard)
