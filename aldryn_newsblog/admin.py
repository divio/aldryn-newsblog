from django.contrib import admin
from django.utils.translation import ugettext as _
from cms.admin.placeholderadmin import FrontendEditableAdminMixin
from parler.admin import TranslatableAdmin

from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_people.models import Person
from aldryn_reversion.admin import VersionedPlaceholderAdminMixin

from . import models


def make_featured(modeladmin, request, queryset):
    queryset.update(is_featured=True)
make_featured.short_description = _(
    "Mark selected articles as featured")


def make_not_featured(modeladmin, request, queryset):
    queryset.update(is_featured=False)
make_not_featured.short_description = _(
    "Mark selected articles as not featured")


class ArticleAdmin(VersionedPlaceholderAdminMixin,
                   TranslatableAdmin,
                   FrontendEditableAdminMixin,
                   admin.ModelAdmin):
    list_display = ('title', 'app_config', 'slug', 'is_featured')
    actions = (make_featured, make_not_featured)

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
