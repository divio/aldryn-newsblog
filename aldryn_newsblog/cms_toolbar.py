# -*- coding: utf-8 -*-

from __future__ import unicode_literals

try:
    from urllib import urlencode
except ImportError:
    from urllib.parse import urlencode

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext as _, get_language_from_request

from cms.toolbar_base import CMSToolbar
from cms.toolbar_pool import toolbar_pool
from cms.utils.urlutils import admin_reverse

from aldryn_apphooks_config.utils import get_app_instance
from parler.models import TranslatableModel

from .models import Article
from .cms_appconfig import NewsBlogConfig


def get_obj_from_request(model, request,
                         pk_url_kwarg='pk',
                         slug_url_kwarg='slug',
                         slug_field='slug'):
    """
    Given a model and the request, try to extract and return an object
    from an available 'pk' or 'slug', or return None.

    Note that no checking is done that the view's kwargs really are for objects
    matching the provided model (how would it?) so use only where appropriate.
    """
    language = get_language_from_request(request, check_path=True)
    kwargs = request.resolver_match.kwargs
    mgr = model.objects
    if pk_url_kwarg in kwargs:
        return mgr.filter(pk=kwargs[pk_url_kwarg]).first()
    elif slug_url_kwarg in kwargs:
        # If the model is translatable, and the given slug is a translated
        # field, then find it the Parler way.
        filter_kwargs = {slug_field: kwargs[slug_url_kwarg]}
        translated_fields = model._parler_meta.get_translated_fields()
        if (issubclass(model, TranslatableModel) and
                slug_url_kwarg in translated_fields):
            return mgr.active_translations(language, **filter_kwargs).first()
        else:
            # OK, do it the normal way.
            return mgr.filter(**filter_kwargs).first()
    else:
        return None


def get_admin_url(action, action_args=[], **url_args):
    """
    Convenience method for constructing admin-urls with GET parameters.

    :param action:      The admin url key for use in reverse. E.g.,
                        'aldryn_newsblog_edit_article'
    :param action_args: The url args for the reverse. E.g., [article.pk, ]
    :param url_args:    A dict of key/value pairs for GET parameters. E.g.,
                        {'language': 'en', }.
    :return: The complete admin url
    """
    base_url = admin_reverse(action, args=action_args)
    # Converts [{key: value}, …] => ["key=value", …]
    params = urlencode(url_args)
    if params:
        return "?".join([base_url, params])
    else:
        return base_url


@toolbar_pool.register
class NewsBlogToolbar(CMSToolbar):
    # watch_models must be a list, not a tuple
    # see https://github.com/divio/django-cms/issues/4135
    watch_models = [Article, ]
    supported_apps = ('aldryn_newsblog',)

    def get_on_delete_redirect_url(self, article):
        url = reverse('{0}:article-list'.format(article.app_config.namespace))
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

            # If we're on an Article detail page, then get the article
            if view_name == '{0}:article-detail'.format(config.namespace):
                article = get_obj_from_request(Article, self.request)
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
                redirect_url = self.get_on_delete_redirect_url(article)
                url = get_admin_url('aldryn_newsblog_article_delete',
                                    [article.pk, ])
                menu.add_modal_item(_('Delete this article'), url=url,
                                    on_close=redirect_url)
