from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib import admin, messages
from django.contrib.admin.util import unquote
from django.db import transaction
from django.shortcuts import get_object_or_404, render_to_response
from django.utils.encoding import force_text
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.utils.translation import ugettext as _
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.admin.placeholderadmin import FrontendEditableAdmin
import reversion
from reversion.models import Version
from parler.admin import TranslatableAdmin

from aldryn_apphooks_config.admin import BaseAppHookConfig
from aldryn_people.models import Person

from .versioning import create_revision_with_placeholders
from . import models


class ArticleAdmin(reversion.VersionAdmin,
                   PlaceholderAdminMixin,
                   TranslatableAdmin,
                   FrontendEditableAdmin):

    revision_confirmation_template = 'reversion/confirm_reversion.html'

    def add_view(self, request, *args, **kwargs):
        data = request.GET.copy()
        try:
            person = Person.objects.get(user=request.user)
            data['author'] = person.pk
            request.GET = data
        except Person.DoesNotExist:
            pass
        return super(ArticleAdmin, self).add_view(request, *args, **kwargs)

    def edit_plugin(self, request, plugin_id):
        with transaction.atomic():
            with reversion.create_revision():
                return super(ArticleAdmin, self).edit_plugin(
                    request, plugin_id)

    def _create_revision(self, plugin, user=None, comment=None):
        objs = plugin.placeholder._get_attached_objects()
        assert len(objs) == 1
        obj = objs[0]
        if user:
            reversion.set_user(user)
        if comment:
            reversion.set_comment(comment)
        create_revision_with_placeholders(obj)

    def post_edit_plugin(self, request, plugin):
        comment = u'Edited plugin #{0.id}: {0!s}'.format(plugin)
        self._create_revision(plugin, request.user, comment)

    def post_move_plugin(self, request, source_placeholder, target_placeholder,
                         plugin):
        comment = u'Moved plugin #{0.id}: {0!s}'.format(plugin)
        self._create_revision(plugin, request.user, comment)

    def post_delete_plugin(self, request, plugin):
        comment = u'Deleted plugin #{0.id}: {0!s}'.format(plugin)
        self._create_revision(plugin, request.user, comment)

    @transaction.atomic
    def revision_view(self, request, object_id, version_id,
                      extra_context=None):
        if not self.has_change_permission(request):
            raise PermissionDenied()

        obj = get_object_or_404(self.model, pk=unquote(object_id))
        version = get_object_or_404(Version, pk=unquote(version_id),
                                    object_id=force_text(obj.pk))
        revision = version.revision

        if request.method == "POST":
            revision.revert()
            opts = self.model._meta
            pk_value = obj._get_pk_val()
            preserved_filters = self.get_preserved_filters(request)

            msg_dict = {
                'name': force_text(opts.verbose_name),
                'obj': force_text(obj)
            }
            msg = _('The %(name)s "%(obj)s" was successfully reverted. '
                    'You may edit it again below.') % msg_dict
            self.message_user(request, msg, messages.SUCCESS)
            redirect_url = reverse('admin:%s_%s_change' %
                                   (opts.app_label, opts.model_name),
                                   args=(pk_value,),
                                   current_app=self.admin_site.name)
            redirect_url = add_preserved_filters({
                'preserved_filters': preserved_filters,
                'opts': opts,
            }, redirect_url)
            return HttpResponseRedirect(redirect_url)
        else:
            context = {
                'object': obj,
                'version': version,
                'revision': revision,
                'revision_date': revision.date_created,
                'versions': revision.version_set.order_by(
                    'content_type__name', 'object_id_int').all,
                'object_name': force_text(self.model._meta.verbose_name),
                'app_label': self.model._meta.app_label,
                'opts': self.model._meta,
                'add': False,
                'change': True,
                'save_as': False,
                'has_add_permission': self.has_add_permission(request),
                'has_change_permission': self.has_change_permission(
                    request, obj),
                'has_delete_permission': self.has_delete_permission(
                    request, obj),
                'has_file_field': True,
                'has_absolute_url': False,
                'original': obj,
            }
            return render_to_response(self.revision_confirmation_template,
                                      context, RequestContext(request))

admin.site.register(models.Article, ArticleAdmin)


class NewsBlogConfigAdmin(BaseAppHookConfig):
    def get_config_fields(self):
        return []

admin.site.register(models.NewsBlogConfig, NewsBlogConfigAdmin)
