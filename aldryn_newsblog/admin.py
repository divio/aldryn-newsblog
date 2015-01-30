from django.contrib import admin
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from parler.admin import TranslatableAdmin

from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_people.models import Person

from .versioning.admin import VersionedPlaceholderAdminMixin
from . import models


class ArticleAdmin(VersionedPlaceholderAdminMixin,
                   TranslatableAdmin,
                   FrontendEditableAdminMixin,
                   admin.ModelAdmin):
    list_display = ('title', 'namespace', 'slug')

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        try:
            person = Person.objects.get(user=request.user)
            data['author'] = person.pk
            request.GET = data
        except Person.DoesNotExist:
            pass
        return super(ArticleAdmin, self).add_view(request, *args, **kwargs)

admin.site.register(models.Article, ArticleAdmin)


class NewsBlogConfigAdmin(TranslatableAdmin, BaseAppHookConfig):
    def get_config_fields(self):
        return ('app_title', )

admin.site.register(models.NewsBlogConfig, NewsBlogConfigAdmin)
