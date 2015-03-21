# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models


class NewsBlogPlugin(CMSPluginBase):
    module = 'NewsBlog'


class NewsBlogArchivePlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/archive.html'
    name = _('Archive')
    cache = False
    model = models.NewsBlogArchivePlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['dates'] = models.Article.objects.get_months(
            namespace=instance.app_config.namespace)
        return context

plugin_pool.register_plugin(NewsBlogArchivePlugin)


class NewsBlogArticleSearchPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/article_search.html'
    name = _('Article Search')
    model = models.NewsBlogArticleSearchPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['query_url'] = reverse('{0}:article-search'.format(
            instance.app_config.namespace))
        return context


plugin_pool.register_plugin(NewsBlogArticleSearchPlugin)


class NewsBlogAuthorsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/authors.html'
    name = _('Authors')
    model = models.NewsBlogAuthorsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['article_list_url'] = reverse(
            '{0}:article-list'.format(instance.app_config.namespace))
        return context


plugin_pool.register_plugin(NewsBlogAuthorsPlugin)


class NewsBlogCategoriesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/categories.html'
    name = _('Categories')
    model = models.NewsBlogCategoriesPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['categories'] = instance.get_categories()
        context['article_list_url'] = reverse(
            '{0}:article-list'.format(instance.app_config.namespace))
        return context


plugin_pool.register_plugin(NewsBlogCategoriesPlugin)


class NewsBlogFeaturedArticlesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/featured_articles.html'
    name = _('Featured Articles')
    model = models.NewsBlogFeaturedArticlesPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(NewsBlogFeaturedArticlesPlugin)


class NewsBlogLatestArticlesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/latest_articles.html'
    name = _('Latest Articles')
    cache = False
    model = models.NewsBlogLatestArticlesPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        return context


plugin_pool.register_plugin(NewsBlogLatestArticlesPlugin)


class NewsBlogRelatedPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/related_articles.html'
    name = _('Related Articles')
    cache = False
    model = models.NewsBlogRelatedPlugin

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


plugin_pool.register_plugin(NewsBlogRelatedPlugin)


class NewsBlogTagsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/tags.html'
    name = _('Tags')
    model = models.NewsBlogTagsPlugin

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['tags'] = instance.get_tags()
        context['article_list_url'] = reverse(
            '{0}:article-list'.format(instance.app_config.namespace))
        return context


plugin_pool.register_plugin(NewsBlogTagsPlugin)
