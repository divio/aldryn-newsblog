from django import forms
from app_data import AppDataForm

from aldryn_apphooks_config.utils import setup_config

from .models import NewsBlogConfig


class LatestEntriesForm(forms.ModelForm):
    pass


class NewsBlogConfigForm(AppDataForm):
    pass


setup_config(NewsBlogConfigForm, NewsBlogConfig)
