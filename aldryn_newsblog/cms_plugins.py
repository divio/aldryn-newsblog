from cms.models.pluginmodel import CMSPlugin
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool


class NewsBlogPlugin(CMSPluginBase):
    module = 'NewsBlog'
    render_plugin=False # TODO


plugin_pool.register_plugin(NewsBlogPlugin)
