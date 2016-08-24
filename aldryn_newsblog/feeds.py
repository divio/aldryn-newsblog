# -*- coding: utf-8 -*-

from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    # Django 1.6
    from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse
from django.utils.translation import get_language_from_request, ugettext as _

from aldryn_apphooks_config.utils import get_app_instance
from aldryn_categories.models import Category
from aldryn_newsblog.models import Article
from aldryn_newsblog.utils.utilities import get_valid_languages


class LatestArticlesFeed(Feed):

    def __call__(self, request, *args, **kwargs):
        self.namespace, self.config = get_app_instance(request)
        language = get_language_from_request(request)
        site_id = getattr(get_current_site(request), 'id', None)
        self.valid_languages = get_valid_languages(
            self.namespace,
            language_code=language,
            site_id=site_id)
        return super(LatestArticlesFeed, self).__call__(
            request, *args, **kwargs)

    def link(self):
        return reverse('{0}:article-list-feed'.format(self.namespace))

    def title(self):
        msgformat = {'site_name': Site.objects.get_current().name}
        return _('Articles on %(site_name)s') % msgformat

    def get_queryset(self):
        qs = Article.objects.published().namespace(self.namespace).translated(
            *self.valid_languages)
        return qs

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
            *self.valid_languages, slug=category).get()

    def items(self, obj):
        return self.get_queryset().filter(categories=obj)[:10]
