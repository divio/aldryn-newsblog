# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.utils import setup_config
from aldryn_apphooks_config.models import AppHookConfig
from app_data import AppDataForm
from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel
from parler.models import TranslatedFields


class NewsBlogConfig(TranslatableModel, AppHookConfig):
    """Adds some translatable, per-app-instance fields."""
    translations = TranslatedFields(
        app_title=models.CharField(_('application title'), max_length=234),
    )

    # ALDRYN_NEWSBLOG_PAGINATE_BY
    paginate_by = models.PositiveIntegerField(
        _('Paginate size'),
        blank=False,
        default=5,
        help_text=_('When paginating list views, how many articles per page?'),
    )

    # ALDRYN_NEWSBLOG_CREATE_AUTHOR
    create_authors = models.BooleanField(
        _('Auto-create authors?'),
        default=True,
        help_text=_('Automatically create authors from logged-in user?'),
    )

    # ALDRYN_NEWSBLOG_SEARCH
    search_indexed = models.BooleanField(
        _('Include in search index?'),
        default=True,
        help_text=_('Include articles in search indexes?'),
    )

    placeholder_base_top = PlaceholderField(
        'newsblog_base_top',
        related_name='aldryn_newsblog_base_top',
    )

    placeholder_base_sidebar = PlaceholderField(
        'newsblog_base_sidebar',
        related_name='aldryn_newsblog_base_sidebar',
    )

    placeholder_list_top = PlaceholderField(
        'newsblog_list_top',
        related_name='aldryn_newsblog_list_top',
    )

    placeholder_list_footer = PlaceholderField(
        'newsblog_list_footer',
        related_name='aldryn_newsblog_list_footer',
    )

    placeholder_detail_top = PlaceholderField(
        'newsblog_detail_top',
        related_name='aldryn_newsblog_detail_top',
    )

    placeholder_detail_bottom = PlaceholderField(
        'newsblog_detail_bottom',
        related_name='aldryn_newsblog_detail_bottom',
    )

    placeholder_detail_footer = PlaceholderField(
        'newsblog_detail_footer',
        related_name='aldryn_newsblog_detail_footer',
    )

    def get_app_title(self):
        return getattr(self, 'app_title', _('untitled'))


class NewsBlogConfigForm(AppDataForm):
    pass
setup_config(NewsBlogConfigForm, NewsBlogConfig)
