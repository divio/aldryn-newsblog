from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .models import NewsBlogConfig
from .menu import NewsBlogMenu


class NewsBlogApp(CMSConfigApp):
    app_config = NewsBlogConfig
    app_name = 'aldryn_newsblog'
    menus = [NewsBlogMenu, ]
    name = _('NewsBlog')
    urls = ['aldryn_newsblog.urls']


apphook_pool.register(NewsBlogApp)
