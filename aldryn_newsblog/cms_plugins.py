from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from aldryn_newsblog import forms, models


class NewsBlogPlugin(CMSPluginBase):
    module = 'NewsBlog'


class LatestEntriesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/latest_entries.html'
    name = _('Latest Entries')
    cache = False
    model = models.LatestEntriesPlugin
    form = forms.LatestEntriesForm

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(LatestEntriesPlugin)
