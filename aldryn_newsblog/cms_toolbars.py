# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import (
    ugettext as _, get_language_from_request, override)

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool

from aldryn_apphooks_config.utils import get_app_instance
from aldryn_translation_tools.utils import get_admin_url
from aldryn_translation_tools.utils import get_object_from_request

from .models import Article
from .cms_appconfig import NewsBlogConfig


@toolbar_pool.register
class NewsBlogToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Article, ]
    supported_apps = ('aldryn_newsblog',)

    def get_on_delete_redirect_url(self, article, language):
        with override(language):
            url = reverse(
                '{0}:article-list'.format(article.app_config.namespace))
        return url

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
        try:
            view_name = self.request.resolver_match.view_name
        except AttributeError:
            view_name = None

        if user and view_name:
            language = get_language_from_request(self.request, check_path=True)

            # FIXME: determine if we're in edit mode and load the draft if
            #        applicable.
            # If we're on an Article detail page, then get the article
            detail_view_names = [
                '{0}:article-detail'.format(config.namespace),
                '{0}:article-detail-draft'.format(config.namespace),
                '{0}:article-detail-draft-create'.format(config.namespace),
                # '{0}:article-detail-draft-publish'.format(config.namespace),
            ]
            if view_name in detail_view_names:
                article = get_object_from_request(Article, self.request)
            else:
                article = None

            menu = self.toolbar.get_or_create_menu('newsblog-app',
                                                   config.get_app_title())

            change_config_perm = user.has_perm(
                'aldryn_newsblog.change_newsblogconfig')
            add_config_perm = user.has_perm(
                'aldryn_newsblog.add_newsblogconfig')
            config_perms = [change_config_perm, add_config_perm]

            change_article_perm = user.has_perm(
                'aldryn_newsblog.change_article')
            delete_article_perm = user.has_perm(
                'aldryn_newsblog.delete_article')
            add_article_perm = user.has_perm('aldryn_newsblog.add_article')
            article_perms = [change_article_perm, add_article_perm,
                             delete_article_perm, ]

            if change_config_perm:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('aldryn_newsblog_newsblogconfig_change',
                                    [config.pk, ], **url_args)
                menu.add_modal_item(_('Configure addon'), url=url)

            if any(config_perms) and any(article_perms):
                menu.add_break()

            if change_article_perm:
                url_args = {}
                if config:
                    url_args = {'app_config__id__exact': config.pk}
                url = get_admin_url('aldryn_newsblog_article_changelist',
                                    **url_args)
                menu.add_sideframe_item(_('Article list'), url=url)

            if add_article_perm:
                url_args = {'app_config': config.pk, 'owner': user.pk, }
                if language:
                    url_args.update({'language': language, })
                url = get_admin_url('aldryn_newsblog_article_add', **url_args)
                menu.add_modal_item(_('Add new article'), url=url)

            if change_article_perm and article:
                url_args = {}
                if language:
                    url_args = {'language': language, }
                url = get_admin_url('aldryn_newsblog_article_change',
                                    [article.pk, ], **url_args)
                menu.add_modal_item(_('Edit this article'), url=url,
                                    active=True)

            if delete_article_perm and article:
                redirect_url = self.get_on_delete_redirect_url(
                    article, language=language)
                url = get_admin_url('aldryn_newsblog_article_delete',
                                    [article.pk, ])
                menu.add_modal_item(_('Delete this article'), url=url,
                                    on_close=redirect_url)

            # PUBLISHER
            if article:
                draft_article = article.publisher_get_draft_version()
                published_article = article.publisher_get_published_version()
                if self.toolbar.edit_mode:
                    if draft_article:
                        # We're in edit mode. There is a draft article.
                        self.toolbar.add_button(
                            name='Publish',
                            url=draft_article.get_publish_url(),
                            side=self.toolbar.RIGHT,
                            extra_classes=[
                                'cms-btn-action',
                            ],
                        )
                        # add_ajax_button(
                        #     toolbar=self.toolbar,
                        #     name='Publish',
                        #     action=draft_article.get_publish_url(),
                        #     side=self.toolbar.RIGHT,
                        #     extra_classes=[
                        #         'cms-btn-action',
                        #     ],
                        # )
                    else:
                        # We're in edit mode but there is no draft yet. Add a
                        # edit button that will create a draft if it does not
                        # exist.
                        self.toolbar.add_button(
                            name='Edit',
                            url=published_article.get_draft_url(),
                            side=self.toolbar.RIGHT,
                            extra_classes=[
                                'cms-btn-action',
                            ],
                        )
                        # add_ajax_button(
                        #     toolbar=self.toolbar,
                        #     name='Edit',
                        #     action=published_article.get_draft_url(),
                        #     side=self.toolbar.RIGHT,
                        #     extra_classes=[
                        #         'cms-btn-action',
                        #     ],
                        # )
                    if self.toolbar.edit_mode and draft_article:
                        menu.add_ajax_item(
                            name=_('Revert to live'),
                            action=draft_article.get_discard_draft_url(),
                            question=_('Are you sure you want to revert to live?'),
                        )
                    elif self.toolbar.edit_mode:
                        menu.add_link_item(
                            name=_('Revert to live'),
                            url='',
                            disabled=True,
                        )

            # /PUBLISHER
