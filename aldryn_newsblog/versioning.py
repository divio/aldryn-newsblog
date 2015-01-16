"""
Support for django-reversion on models with translatable fields and django-cms
placeholder fields.
"""
from functools import partial

from django.core.exceptions import PermissionDenied
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.admin.util import unquote
from django.contrib.admin.templatetags.admin_urls import add_preserved_filters
from django.db.models.signals import post_save
from django.db import transaction
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render_to_response
from django.template import RequestContext
from django.utils.encoding import force_text
from django.utils.translation import ugettext as _

from cms.admin.placeholderadmin import PlaceholderAdminMixin
from cms.models.pluginmodel import CMSPlugin
import reversion
from reversion.revisions import VersionAdapter
from reversion.models import Version
from parler import cache


# TODO: The following classes and registration function shall be extracted in a
# common add-on module (as soon as we have one).


def create_revision_with_placeholders(instance, revision_manager=None,
                                      rev_ctx=None):
    if revision_manager is None:
        revision_manager = reversion.default_revision_manager

    if rev_ctx is None:
        rev_ctx = revision_manager._revision_context_manager

    def add_to_context(obj):
        adapter = revision_manager.get_adapter(obj.__class__)
        version_data = adapter.get_version_data(obj)
        rev_ctx.add_to_context(revision_manager, obj, version_data)

    if rev_ctx.is_active() and not rev_ctx.is_managing_manually():
        # Add the instance to the revision
        add_to_context(instance)

        # Add the placeholder to the revision
        for name in instance._meta.placeholder_field_names:
            add_to_context(getattr(instance, name))

        # Add all plugins to the revision
        ph_ids = [getattr(instance, '{0}_id'.format(name))
                  for name in instance._meta.placeholder_field_names]

        for plugin in CMSPlugin.objects.filter(placeholder_id__in=ph_ids):
            plugin_instance, _ = plugin.get_plugin_instance()
            if plugin_instance:
                add_to_context(plugin_instance)
            add_to_context(plugin)


class TranslatableVersionAdapterMixin(object):
    revision_manager = None

    def __init__(self, model):
        super(TranslatableVersionAdapterMixin, self).__init__(model)

        # Register the translation model to be tracked as well, by following
        # all placeholder fields, if any.
        root_model = model._parler_meta.root_model
        self.revision_manager.register(root_model)

        # Also add the translations to the models to follow.
        self.follow = list(self.follow) + [model._parler_meta.root_rel_name]

        # And make sure that when we revert them, we update the translations
        # cache (this is normally done in the translation `save_base` method,
        # but it is not called when reverting changes).
        post_save.connect(self._update_cache, sender=root_model)

    def _update_cache(self, sender, instance, raw, **kwargs):
        """Update the translations cache when restoring from a revision."""
        if raw:
            # Raw is set to true (only) when restoring from fixtures or,
            # django-reversion
            cache._cache_translation(instance)


class PlaceholderVersionAdapterMixin(object):
    follow_placeholders = True

    def __init__(self, model):
        super(PlaceholderVersionAdapterMixin, self).__init__(model)

        # Add cms placeholders the to the models to follow.
        placeholders = getattr(model._meta, 'placeholder_field_names', None)
        if self.follow_placeholders and placeholders:
            self.follow = list(self.follow) + placeholders
            post_save.connect(self._add_plugins_to_revision, sender=model)

    def _add_plugins_to_revision(self, sender, instance, **kwargs):
        """Manually add plugins to the revision.

        This method is an updated and adapter version of
        https://github.com/divio/django-cms/blob/develop/cms/utils/helpers.py#L34
        but instead of working on pages, works on models with placeholder
        fields.
        """
        rev_ctx = self.revision_manager._revision_context_manager

        def add_to_context(obj):
            adapter = self.revision_manager.get_adapter(obj.__class__)
            version_data = adapter.get_version_data(obj)
            rev_ctx.add_to_context(self.revision_manager, obj, version_data)

        if rev_ctx.is_active() and not rev_ctx.is_managing_manually():
            ph_ids = [getattr(instance, '{0}_id'.format(name))
                      for name in instance._meta.placeholder_field_names]

            # Add all plugins to the revision
            for plugin in CMSPlugin.objects.filter(placeholder_id__in=ph_ids):
                plugin_instance, _ = plugin.get_plugin_instance()
                if plugin_instance:
                    add_to_context(plugin_instance)
                add_to_context(plugin)


class ContentEnabledVersionAdapter(TranslatableVersionAdapterMixin,
                                   PlaceholderVersionAdapterMixin,
                                   VersionAdapter):
    pass


version_controlled_content = partial(
    reversion.register, adapter_cls=ContentEnabledVersionAdapter,
    revision_manager=reversion.default_revision_manager)


class VersionedPlaceholderAdminMixin(reversion.VersionAdmin,
                                     PlaceholderAdminMixin):
    revision_confirmation_template = 'reversion/confirm_reversion.html'

    def edit_plugin(self, request, plugin_id):
        with transaction.atomic():
            with reversion.create_revision():
                return super(VersionedPlaceholderAdminMixin, self).edit_plugin(
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
        super(VersionedPlaceholderAdminMixin, self).post_edit_plugin(
            request, plugin)
        comment = u'Edited plugin #{0.id}: {0!s}'.format(plugin)
        self._create_revision(plugin, request.user, comment)

    def post_move_plugin(self, request, source_placeholder, target_placeholder,
                         plugin):
        super(VersionedPlaceholderAdminMixin, self).post_move_plugin(
            request, plugin)
        comment = u'Moved plugin #{0.id}: {0!s}'.format(plugin)
        self._create_revision(plugin, request.user, comment)

    def post_delete_plugin(self, request, plugin):
        super(VersionedPlaceholderAdminMixin, self).post_delete_plugin(
            request, plugin)
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
