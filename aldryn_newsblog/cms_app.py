from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _


class NewsBlogApp(CMSApp):
    name = _('NewsBlog')
    urls = ['aldryn_newsblog.urls']
    app_name = 'aldryn_newsblog'


apphook_pool.register(NewsBlogApp)
