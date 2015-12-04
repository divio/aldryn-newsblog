# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.utils.translation import ugettext_lazy as _

from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from . import models, forms
from .utils import add_prefix_to_path, default_reverse


class TemplatePrefixMixin(object):

    def get_render_template(self, context, instance, placeholder):
        if (hasattr(instance, 'app_config') and
                instance.app_config.template_prefix):
            return add_prefix_to_path(
                self.render_template,
                instance.app_config.template_prefix
            )
        return self.render_template


class NewsBlogPlugin(TemplatePrefixMixin, CMSPluginBase):
    module = 'News & Blog'


@plugin_pool.register_plugin
class NewsBlogArchivePlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/archive.html'
    name = _('Archive')
    cache = False
    model = models.NewsBlogArchivePlugin
    form = forms.NewsBlogArchivePluginForm

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance

        queryset = models.Article.objects

        context['dates'] = queryset.get_months(
            request,
            namespace=instance.app_config.namespace
        )
        return context


@plugin_pool.register_plugin
class NewsBlogArticleSearchPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/article_search.html'
    name = _('Article Search')
    model = models.NewsBlogArticleSearchPlugin
    form = forms.NewsBlogArticleSearchPluginForm

    def render(self, context, instance, placeholder):
        context['instance'] = instance
        context['query_url'] = default_reverse('{0}:article-search'.format(
            instance.app_config.namespace), default=None)
        return context


@plugin_pool.register_plugin
class NewsBlogAuthorsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/authors.html'
    name = _('Authors')
    model = models.NewsBlogAuthorsPlugin
    form = forms.NewsBlogAuthorsPluginForm

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance
        context['authors_list'] = instance.get_authors(request)
        context['article_list_url'] = default_reverse(
            '{0}:article-list'.format(instance.app_config.namespace),
            default=None)

        return context


@plugin_pool.register_plugin
class NewsBlogCategoriesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/categories.html'
    name = _('Categories')
    model = models.NewsBlogCategoriesPlugin
    form = forms.NewsBlogCategoriesPluginForm

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance
        context['categories'] = instance.get_categories(request)
        context['article_list_url'] = default_reverse(
            '{0}:article-list'.format(instance.app_config.namespace),
            default=None)
        return context


@plugin_pool.register_plugin
class NewsBlogFeaturedArticlesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/featured_articles.html'
    name = _('Featured Articles')
    model = models.NewsBlogFeaturedArticlesPlugin
    form = forms.NewsBlogFeaturedArticlesPluginForm

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance
        context['articles_list'] = instance.get_articles(request)
        return context


@plugin_pool.register_plugin
class NewsBlogLatestArticlesPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/latest_articles.html'
    name = _('Latest Articles')
    cache = False
    model = models.NewsBlogLatestArticlesPlugin
    form = forms.NewsBlogLatestArticlesPluginForm

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance
        context['article_list'] = instance.get_articles(request)
        return context


@plugin_pool.register_plugin
class NewsBlogRelatedPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/related_articles.html'
    name = _('Related Articles')
    cache = False
    model = models.NewsBlogRelatedPlugin

    def get_article(self, request):
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
        request = context.get('request')
        context['instance'] = instance
        article = self.get_article(request)
        if article:
            context['article'] = article
            context['article_list'] = instance.get_articles(article, request)
        return context


@plugin_pool.register_plugin
class NewsBlogTagsPlugin(NewsBlogPlugin):
    render_template = 'aldryn_newsblog/plugins/tags.html'
    name = _('Tags')
    model = models.NewsBlogTagsPlugin
    form = forms.NewsBlogTagsPluginForm

    def render(self, context, instance, placeholder):
        request = context.get('request')
        context['instance'] = instance
        context['tags'] = instance.get_tags(request)
        context['article_list_url'] = default_reverse(
            '{0}:article-list'.format(instance.app_config.namespace),
            default=None)
        return context
