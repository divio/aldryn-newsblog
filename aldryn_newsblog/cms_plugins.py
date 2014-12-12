from django.utils.translation import ugettext_lazy as _

from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_newsblog import models


class NewsBlogPlugin(CMSPluginBase):
    module = 'NewsBlog'
    render_template = 'aldryn_newsblog/plugins/newsblog_articles.html'


plugin_pool.register_plugin(NewsBlogPlugin)
