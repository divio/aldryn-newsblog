# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings

from haystack.constants import DEFAULT_ALIAS

from aldryn_search.utils import get_index_base

from .models import Article


class ArticleIndex(get_index_base()):
    haystack_use_for_indexing = getattr(
        settings, 'ALDRYN_NEWSBLOG_SEARCH', True)

    index_title = True

    def get_language(self, obj):
        return getattr(obj, '_current_language', None)

    def get_title(self, obj):
        return obj.title

    def get_url(self, obj):
        using = getattr(self, '_backend_alias', DEFAULT_ALIAS)
        language = self.get_current_language(using=using, obj=obj)
        return obj.get_absolute_url(language)

    def get_description(self, obj):
        return obj.lead_in

    def get_index_kwargs(self, language):
        """
        This is called to filter the index queryset.
        """
        kwargs = {
            'app_config__search_indexed': True,
            'translations__language_code': language,
        }
        return kwargs

    def get_index_queryset(self, language):
        queryset = super(ArticleIndex, self).get_index_queryset(language)
        return queryset.published().language(language)

    def get_model(self):
        return Article

    def get_search_data(self, article, language, request):
        return article.search_data

    def should_update(self, instance, **kwargs):
        using = getattr(self, '_backend_alias', DEFAULT_ALIAS)
        language = self.get_current_language(using=using, obj=instance)
        translations = instance.get_available_languages()
        return translations.filter(language_code=language).exists()
