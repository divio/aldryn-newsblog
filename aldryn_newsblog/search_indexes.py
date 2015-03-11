# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.utils.encoding import force_text

from aldryn_search.helpers import get_plugin_index_data
from aldryn_search.utils import get_index_base, strip_tags

from .models import Article


class ArticleIndex(get_index_base()):
    haystack_use_for_indexing = True

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

    def get_search_data(self, obj, language, request):
        description = self.get_description(obj)
        text_bits = [strip_tags(description)]
        for category in obj.categories.all():
            text_bits.append(force_text(category.safe_translation_getter('name')))
        for tag in obj.tags.all():
            text_bits.append(force_text(tag.name))
        if obj.content:
            for base_plugin in obj.content.cmsplugin_set.filter(language=language):
                plugin_text_content = ' '.join(get_plugin_index_data(base_plugin, request))
                text_bits.append(plugin_text_content)
        return ' '.join(text_bits)
