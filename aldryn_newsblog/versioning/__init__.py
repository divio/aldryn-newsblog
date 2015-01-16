"""
Support for django-reversion on models with translatable fields and django-cms
placeholder fields.
"""
from functools import partial

from django.db.models.signals import post_save

from cms.models.pluginmodel import CMSPlugin
import reversion
from reversion.revisions import VersionAdapter
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
