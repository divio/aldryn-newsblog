# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
from django.core.urlresolvers import reverse
from django.utils.translation import (
    get_language, get_language_from_request, ugettext as _)

from aldryn_apphooks_config.utils import get_app_instance
from aldryn_categories.models import Category
from aldryn_newsblog.models import Article


class LatestArticlesFeed(Feed):

    def __call__(self, request, *args, **kwargs):
        self.namespace, self.config = get_app_instance(request)
        return super(LatestArticlesFeed, self).__call__(
            request, *args, **kwargs)

    def link(self):
        return reverse('{0}:article-list-feed'.format(self.namespace))

    def title(self):
        return _('Articles on {0}').format(Site.objects.get_current().name)

    def get_queryset(self):
        language = get_language()
        return Article.objects.published().active_translations(
            language
        ).namespace(self.namespace)

    def items(self, obj):
        qs = self.get_queryset()
        return qs.order_by('-publishing_date')[:10]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.lead_in

    def item_pubdate(self, item):
        return item.publishing_date


class TagFeed(LatestArticlesFeed):

    def get_object(self, request, tag):
        return tag

    def items(self, obj):
        return self.get_queryset().filter(tags__slug=obj)[:10]


class CategoryFeed(LatestArticlesFeed):

    def get_object(self, request, category):
        language = get_language_from_request(request, check_path=True)
        return Category.objects.language(language).translated(
            slug=category).get()

    def items(self, obj):
        return self.get_queryset().filter(categories=obj)[:10]
