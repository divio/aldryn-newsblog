# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from aldryn_apphooks_config.utils import get_app_instance
from .models import Article
from .cms_appconfig import NewsBlogConfig


@toolbar_pool.register
class NewsBlogToolbar(CMSToolbar):
    watch_models = (Article, )
    supported_apps = ('aldryn_newsblog',)

    def __get_newsblog_config(self):
        try:
            __, config = get_app_instance(self.request)
            if not isinstance(config, NewsBlogConfig):
                # This is not the app_hook you are looking for.
                return None
        except ImproperlyConfigured:
            # There is no app_hook at all.
            return None

        return config

    def populate(self):
        config = self.__get_newsblog_config()
        if not config:
            # Do nothing if there is no NewsBlog app_config to work with
            return

        user = getattr(self.request, 'user', None)

        menu = self.toolbar.get_or_create_menu('newsblog-app', config.get_app_title())

        if self.request.user.has_perm('aldryn_newsblog.change_newsblogconfig'):
            menu.add_modal_item(
                _('Configure application'),
                url=admin_reverse(
                    'aldryn_newsblog_newsblogconfig_change',
                    args=(config.pk, )
                ),
            )

        if self.request.user.has_perm('aldryn_newsblog.change_article'):
            menu.add_sideframe_item(
                _('Article list'),
                url="{base}?app_config__id__exact={config}".format(
                    base=admin_reverse('aldryn_newsblog_article_changelist'),
                    config=config.pk,
                ),
            )

        if self.request.user.has_perm('aldryn_newsblog.add_article'):
            menu.add_modal_item(
                _('Add new article'),
                url="{base}?app_config={config}&owner={owner}".format(
                    base=admin_reverse('aldryn_newsblog_article_add'),
                    config=config.pk,
                    owner=user.pk,
                ),
            )

        view_name = self.request.resolver_match.view_name
        if (view_name == '{0}:article-detail'.format(config.namespace) and
                self.request.user.has_perm('aldryn_newsblog.change_article')):

            slug = self.request.resolver_match.kwargs['slug']
            articles = Article.objects.translated(slug=slug)
            if articles.count() == 1:
                menu.add_modal_item(_('Edit article'), admin_reverse(
                    'aldryn_newsblog_article_change', args=(
                        articles[0].pk,)), active=True,)
