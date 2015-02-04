# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.template import RequestContext

from aldryn_search.utils import get_index_base, strip_tags

from aldryn_newsblog.models import Article


class ArticleIndex(get_index_base()):
    haystack_use_for_indexing = getattr(settings, "ALDRYN_NEWSBLOG_SEARCH", True)

    INDEX_TITLE = True

    def get_title(self, obj):
        return obj.safe_translation_getter('title')

    def get_description(self, obj):
        return obj.safe_translation_getter('lead_in')

    def get_index_kwargs(self, language):
        return {'translations__language_code': language}

    def get_index_queryset(self, language):
        return self.get_model().objects.active_translations(
            language_code=language)

    def get_model(self):
        return Article

    def get_search_data(self, obj, language, request):
        description = self.get_description(obj)
        text_bits = [strip_tags(description)]
        if obj.content:
                plugins = obj.content.cmsplugin_set.filter(language=language)
                for base_plugin in plugins:
                    instance, plugin_type = base_plugin.get_plugin_instance()
                    if instance is not None:
                        content = strip_tags(instance.render_plugin(context=RequestContext(request)))
                        text_bits.append(content)
        return ' '.join(text_bits)