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


class MockCategory(models.Model):
    name = models.CharField(_('Name'), max_length=123)


class MockTag(models.Model):
    name = models.CharField(_('Name'), max_length=123)


# TODO: The followng classes and registration function shall be extracted in a
# common addon module (as soon as we have one).

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
        # but it is not caled when reverting changes).
        post_save.connect(self._update_cache, sender=root_model)

    def _update_cache(self, sender, instance, raw, **kwargs):
        """Update the translations chache when restoring from a revision."""
        if raw:
            # Raw is set to true (only) when restoring from fixtures or,
            # django-reversion
            cache._cache_translation(instance)


class PlaceholderVersionAdapterMixin(object):
    follow_placeholders = True

    def __init__(self, model):
        super(PlaceholderVersionAdapterMixin, self).__init__(model)

        # Add the to the models to follow.
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


@version_controlled_content
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
    categories = models.ManyToManyField(MockCategory)
    tags = models.ManyToManyField(MockTag)
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

    def copy_relations(self, old_instance):
        self.categories = old_instance.categories.all()
        self.tags = old_instance.tags.all()

    def get_articles(self):
        articles = Article.objects.filter_by_language(self.language)
        return articles[:self.latest_entries]
