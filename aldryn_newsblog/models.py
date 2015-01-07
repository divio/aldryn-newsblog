from functools import partial

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.db.models.signals import post_save

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from aldryn_people.models import Person
import reversion
from reversion.revisions import VersionAdapter
from parler.models import TranslatableModel, TranslatedFields
from parler import cache


# TODO: The followng class and registration function shall be extracted in a
# command addon module (as soon as we have one).

class TranslatableVersionAdapter(VersionAdapter):
    revision_manager = None
    follow_placeholders = True

    def __init__(self, model):
        super(TranslatableVersionAdapter, self).__init__(model)

        # Register the translation model to be tracked as well, by following
        # all placeholder fields, if any.
        root_model = model._parler_meta.root_model
        self.revision_manager.register(root_model)

        # Also add the translations to the models to follow.
        self.follow = list(self.follow) + [model._parler_meta.root_rel_name]

        # ...and the placeholders
        if self.follow_placeholders:
            self.follow += model._meta.placeholder_field_names
            post_save.connect(self._add_plugins_to_revision, sender=model)

        # And make sure that when we revert them, we update the translations
        # cache (this is normally done in the translation `save_base` method,
        # but it is not caled when reverting changes).
        post_save.connect(self._update_cache, sender=root_model)

    def _update_cache(self, sender, instance, raw, **kwargs):
        """Update the translations chache when restoring from a revision."""
        if raw:
            # Raw is set to true (only) when restoring from fixtures or,
            # django-reversion
            cache._cache_translation(instance)

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
            ph_ids = [getattr(instance, '{}_id'.format(name))
                      for name in instance._meta.placeholder_field_names]

            # Add all plugins to the revision
            for plugin in CMSPlugin.objects.filter(placeholder_id__in=ph_ids):
                plugin_instance, _ = plugin.get_plugin_instance()
                if plugin_instance:
                    add_to_context(plugin_instance)
                add_to_context(plugin)


register_translatable = partial(
    reversion.register, adapter_cls=TranslatableVersionAdapter,
    revision_manager=reversion.default_revision_manager)


@register_translatable
class Article(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('Title'), max_length=234),
    )

    content = PlaceholderField('aldryn_newsblog_article_content',
                               related_name='aldryn_newsblog_articles')

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
        blank=True,
        help_text=_(
            'Used in the URL. If changed, the URL will change. '
            'Clean it to have it re-created.'),
    )

    author = models.ForeignKey(Person)
    owner = models.ForeignKey(User)
    namespace = models.CharField(max_length=123, blank=True, default='')
    category = models.CharField(max_length=123, blank=True, default='')
    publishing_date = models.DateTimeField()

    def get_absolute_url(self):
        return reverse(
            'aldryn_newsblog:article-detail', kwargs={'slug': self.slug})


class LatestEntriesPlugin(CMSPlugin):

    latest_entries = models.IntegerField(
        default=5,
        help_text=_('The number of latests entries to be displayed.')
    )

    def __unicode__(self):
        return str(self.latest_entries).decode('utf8')

    def copy_relations(self, oldinstance):
        self.tags = oldinstance.tags.all()

    def get_articles(self):
        articles = Article.objects.filter_by_language(self.language)
        return articles[:self.latest_entries]
