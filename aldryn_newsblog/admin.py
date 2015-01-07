from django.contrib import admin

from aldryn_apphooks_config.admin import BaseAppHookConfig
from parler.admin import TranslatableAdmin

from .models import Article, MockCategory, MockTag, NewsBlogConfig


class ArticleAdmin(TranslatableAdmin):

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        data['author'] = request.user.id  # default author is logged-in user
        request.GET = data
        return super(ArticleAdmin, self).add_view(request, *args, **kwargs)


class MockCategoryAdmin(admin.ModelAdmin):
    pass


class MockTagAdmin(admin.ModelAdmin):
    pass


class NewsBlogConfigAdmin(BaseAppHookConfig):
    def get_config_fields(self):
        return []


admin.site.register(Article, ArticleAdmin)
admin.site.register(MockTag, MockCategoryAdmin)
admin.site.register(MockCategory, MockTagAdmin)
admin.site.register(NewsBlogConfig, NewsBlogConfigAdmin)
