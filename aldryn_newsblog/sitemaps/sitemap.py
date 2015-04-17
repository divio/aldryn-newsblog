# -*- coding: utf-8 -*-
from django.contrib.sitemaps import Sitemap

from ..models import Article


class NewsBlogSitemap(Sitemap):

    changefreq = "never"
    priority = 0.5

    def __init__(self, *args, **kwargs):
        self.namespace = kwargs.pop('namespace', None)
        super(NewsBlogSitemap, self).__init__(*args, **kwargs)

    def items(self):
        qs = Article.objects.published()
        if self.namespace is not None:
            qs = qs.filter(app_config__namespace=self.namespace)
        return qs

    def lastmod(self, obj):
        return obj.publishing_date
