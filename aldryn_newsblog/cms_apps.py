# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.apphook_pool import apphook_pool

from aldryn_apphooks_config.app_base import CMSConfigApp

from aldryn_newsblog.cms_appconfig import NewsBlogConfig


@apphook_pool.register
class NewsBlogApp(CMSConfigApp):
    name = _('NewsBlog')
    app_name = 'aldryn_newsblog'
    app_config = NewsBlogConfig

    def get_urls(self, page=None, language=None, **kwargs):
        return ['aldryn_newsblog.urls']

    # NOTE: Please do not add a «menu» here, menu’s should only be added by at
    # the discretion of the operator.
