from django.contrib import admin

from aldryn_apphooks_config.admin import BaseAppHookConfig

from .models import NewsBlogConfig, MockCategory, MockTag


class MockCategoryAdmin(admin.ModelAdmin):
    pass


class MockTagAdmin(admin.ModelAdmin):
    pass


class NewsBlogConfigAdmin(BaseAppHookConfig):
    def get_config_fields(self):
        return []


admin.site.register(MockTag, MockCategoryAdmin)
admin.site.register(MockCategory, MockTagAdmin)
admin.site.register(NewsBlogConfig, NewsBlogConfigAdmin)
