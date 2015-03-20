# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import forms, models


class NewsBlogPlugin(CMSPluginBase):
    module = 'NewsBlog'


# TODO: rename plugins to have a full app prefix
#       (e.g NewsBlogLatestEntriesPlugin)
#       https://github.com/divio/django-cms/issues/2562


class BlogArchivePlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/archive.html'
    name = _('Archive')
    cache = False
    model = models.ArchivePlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['dates'] = models.Article.objects.get_months(
            namespace=instance.app_config.namespace)
        return context

plugin_pool.register_plugin(BlogArchivePlugin)


class LatestEntriesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/latest_entries.html'
    name = _('Latest Entries')
    cache = False
    model = models.LatestEntriesPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(LatestEntriesPlugin)


class BlogCategoriesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/categories.html'
    name = _('Categories')
    model = models.CategoriesPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['categories'] = instance.get_categories()
        context['article_list_url'] = reverse(
            '{0}:article-list'.format(instance.app_config.namespace))
        return context


plugin_pool.register_plugin(BlogCategoriesPlugin)


class BlogTagsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/tags.html'
    name = _('Tags')
    model = models.TagsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['tags'] = instance.get_tags()
        context['article_list_url'] = reverse(
            '{0}:article-list'.format(instance.app_config.namespace))
        return context


plugin_pool.register_plugin(BlogTagsPlugin)


class AuthorsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/authors.html'
    name = _('Blog Authors')
    model = models.AuthorsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['article_list_url'] = reverse(
            '{0}:article-list'.format(instance.app_config.namespace))
        return context


plugin_pool.register_plugin(AuthorsPlugin)


class RelatedPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/related_articles.html'
    name = _('Related Articles')
    cache = False
    model = models.RelatedPlugin

    def get_article(self, context):
        request = context.get('request', None)
        if request and request.resolver_match:
            view_name = request.resolver_match.view_name
            namespace = request.resolver_match.namespace
            if view_name == '{0}:article-detail'.format(namespace):
                article = models.Article.objects.active_translations(
                    slug=request.resolver_match.kwargs['slug'])
                if article.count() == 1:
                    return article[0]
        return None

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        article = self.get_article(context)
        if article:
            context['article'] = article
            context['related'] = article.related.all()
        return context


plugin_pool.register_plugin(RelatedPlugin)


class NewsBlogFeaturedArticlesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/featured_articles.html'
    name = _('Featured Articles')
    cache = False
    model = models.FeaturedArticlesPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        # article = self.get_article(context)
        return context


plugin_pool.register_plugin(NewsBlogFeaturedArticlesPlugin)
