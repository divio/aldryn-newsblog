from django.utils.translation import ugettext_lazy as _
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import forms, models


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


class BlogCategoriesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/categories.html'
    name = _('Categories')
    model = models.CategoriesPlugin

    def render(self, context, instance, placeholder):
        context['categories'] = instance.get_categories()
        return context


plugin_pool.register_plugin(BlogCategoriesPlugin)


class AuthorsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/authors.html'
    name = _('Blog Authors')
    model = models.AuthorsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(AuthorsPlugin)

