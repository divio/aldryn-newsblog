# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from aldryn_search.utils import get_index_base

from .models import Article


class ArticleIndex(get_index_base()):
    haystack_use_for_indexing = getattr(
        settings, 'ALDRYN_NEWSBLOG_SEARCH', True)

    index_title = True

    def get_title(self, obj):
        return obj.safe_translation_getter('title')

    def get_description(self, obj):
        return obj.safe_translation_getter('lead_in')

    def index_queryset(self, using=None):
        self._get_backend(using)
        language = self.get_current_language(using)
        filter_kwargs = self.get_index_kwargs(language)
        qs = self.get_index_queryset(language)
        if filter_kwargs:
            return qs.translated(language, **filter_kwargs)
        return qs

    def get_index_queryset(self, language):
        return self.get_model().objects.published().active_translations(
            language_code=language).filter(app_config__search_indexed=True)

    def get_model(self):
        return Article

    def get_search_data(self, article, language, request):
        if not article.search_data:
            article.search_data = article.get_search_data(language, request)
            article.save()
        return article.search_data
