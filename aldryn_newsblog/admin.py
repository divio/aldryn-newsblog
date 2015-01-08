from django.contrib import admin

from aldryn_apphooks_config.admin import BaseAppHookConfig

from .models import NewsBlogConfig


class NewsBlogConfigAdmin(BaseAppHookConfig):
    def get_config_fields(self):
        return []


admin.site.register(NewsBlogConfig, NewsBlogConfigAdmin)
