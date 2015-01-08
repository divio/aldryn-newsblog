from aldryn_apphooks_config.app_base import CMSConfigApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

from .models import NewsBlogConfig


class NewsBlogApp(CMSConfigApp):
    name = _('NewsBlog')
    urls = ['aldryn_newsblog.urls']
    app_name = 'aldryn_newsblog'
    app_config = NewsBlogConfig


apphook_pool.register(NewsBlogApp)
