# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db.models.signals import post_save
from django.dispatch import receiver

from cms.models import CMSPlugin


@receiver(post_save)
def update_seach_index(sender, instance, **kwargs):
    """
    Upon detecting changes in a plugin used in an Article's content
    (PlaceholderField), update the article's search_index so that we can
    perform simple searches even without Haystack, etc.
    """
    if isinstance(instance, CMSPlugin):
        # TODO: Handle cases where the plugin is a child of another plugin, etc.
        if hasattr(instance.placeholder, 'aldryn_newsblog_articles'):
            articles = instance.placeholder.aldryn_newsblog_articles.all()
            if articles.count():
                article = articles[0]
                article.set_current_language(instance.language)
                article.search_data = article.get_search_data(
                    instance.language, None)
                article.save()
