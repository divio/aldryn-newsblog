from django.contrib import admin

from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_people.models import Person
from cms.admin.placeholderadmin import PlaceholderAdmin, FrontendEditableAdmin
from parler.admin import TranslatableAdmin

from .models import Article, MockCategory, MockTag, NewsBlogConfig


class ArticleAdmin(TranslatableAdmin, PlaceholderAdmin, FrontendEditableAdmin):

    # TODO: make possible to edit placeholder

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        try:
            person = Person.objects.get(user=request.user)
            data['author'] = person.pk
            request.GET = data
        except Person.DoesNotExist:
            pass
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
