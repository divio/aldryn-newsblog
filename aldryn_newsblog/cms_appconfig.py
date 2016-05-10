# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django import forms
from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.utils import setup_config
from aldryn_apphooks_config.models import AppHookConfig
from aldryn_reversion.core import version_controlled_content
from app_data import AppDataForm
from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel
from parler.models import TranslatedFields

PERMALINK_CHOICES = (
    ('s', _('the-eagle-has-landed/', )),
    ('ys', _('1969/the-eagle-has-landed/', )),
    ('yms', _('1969/07/the-eagle-has-landed/', )),
    ('ymds', _('1969/07/16/the-eagle-has-landed/', )),
    ('ymdi', _('1969/07/16/11/', )),
)

NON_PERMALINK_HANDLING = (
    (200, _('Allow')),
    (302, _('Redirect to permalink (default)')),
    (301, _('Permanent redirect to permalink')),
    (404, _('Return 404: Not Found')),
)

# TODO override default if support for Django 1.6 will be dropped
TEMPLATE_PREFIX_CHOICES = getattr(
    settings, 'ALDRYN_NEWSBLOG_TEMPLATE_PREFIXES', [])


@version_controlled_content
class NewsBlogConfig(TranslatableModel, AppHookConfig):
    """Adds some translatable, per-app-instance fields."""
    translations = TranslatedFields(
        app_title=models.CharField(_('application title'), max_length=234),
    )

    permalink_type = models.CharField(_('permalink type'), max_length=8,
        blank=False, default='slug', choices=PERMALINK_CHOICES,
        help_text=_('Choose the style of urls to use from the examples. '
                    '(Note, all types are relative to apphook)'))

    non_permalink_handling = models.SmallIntegerField(
        _('non-permalink handling'),
        blank=False, default=302,
        choices=NON_PERMALINK_HANDLING,
        help_text=_('How to handle non-permalink urls?'))

    paginate_by = models.PositiveIntegerField(
        _('Paginate size'),
        blank=False,
        default=5,
        help_text=_('When paginating list views, how many articles per page?'),
    )
    pagination_pages_start = models.PositiveIntegerField(
        _('Pagination pages start'),
        blank=False,
        default=10,
        help_text=_('When paginating list views, after how many pages '
                    'should we start grouping the page numbers.'),
    )
    pagination_pages_visible = models.PositiveIntegerField(
        _('Pagination pages visible'),
        blank=False,
        default=4,
        help_text=_('When grouping page numbers, this determines how many '
                    'pages are visible on each side of the active page.'),
    )
    exclude_featured = models.PositiveSmallIntegerField(
        _('Excluded featured articles count'),
        blank=True,
        default=0,
        help_text=_(
            'If you are using the Featured Articles plugin on the article list '
            'view, you may prefer to exclude featured articles from the '
            'article list itself to avoid duplicates. To do this, enter the '
            'same number here as in your Featured Articles plugin.'),
    )
    template_prefix = models.CharField(
        max_length=20,
        null=True, blank=True,
        choices=TEMPLATE_PREFIX_CHOICES,
        verbose_name=_("Prefix for template dirs"))

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

    class Meta:
        verbose_name = 'application configuration'
        verbose_name_plural = 'application configurations'


class NewsBlogConfigForm(AppDataForm):
    default_published = forms.BooleanField(
        label=_(u'Post published by default'), required=False,
        initial=getattr(settings, 'ALDRYN_NEWSBLOG_DEFAULT_PUBLISHED', False))
setup_config(NewsBlogConfigForm, NewsBlogConfig)
