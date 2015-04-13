# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.core.urlresolvers import NoReverseMatch
from aldryn_search.utils import get_index_base

from .models import Article


class ArticleIndex(get_index_base()):
    haystack_use_for_indexing = getattr(
        settings, 'ALDRYN_NEWSBLOG_SEARCH', True)

    index_title = True

    def get_title(self, obj):
        language = self.prepared_data['language']
        return obj.safe_translation_getter('title', language_code=language)

    def get_url(self, obj):
        try:
            return obj.get_absolute_url()
        except NoReverseMatch:
            return ''

    def get_description(self, obj):
        language = self.prepared_data['language']
        return obj.safe_translation_getter('lead_in', language_code=language)

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
        return article.safe_translation_getter('search_data', language_code=language)

