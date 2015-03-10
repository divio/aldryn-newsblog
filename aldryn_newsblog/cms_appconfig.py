# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

from aldryn_apphooks_config.utils import setup_config
from aldryn_apphooks_config.models import AppHookConfig
from app_data import AppDataForm
from parler.models import TranslatableModel
from parler.models import TranslatedFields


class NewsBlogConfig(TranslatableModel, AppHookConfig):
    """Adds some translatable, per-app-instance fields."""
    translations = TranslatedFields(
        app_title=models.CharField(_('application title'), max_length=234),
    )

    paginate_by = models.PositiveIntegerField(
        _('Paginate size'),
        blank=False,
        default=5,
        help_text=_('When paginating list views, how many articles per page?')
    )


class NewsBlogConfigForm(AppDataForm):
    pass
setup_config(NewsBlogConfigForm, NewsBlogConfig)
