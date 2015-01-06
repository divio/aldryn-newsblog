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


class TranslatableVersionAdapter(VersionAdapter):
    revision_manager = None

    def __init__(self, model):
        super(TranslatableVersionAdapter, self).__init__(model)

        # Register the translation model to be tracked as well
        root_model = model._parler_meta.root_model
        self.revision_manager.register(root_model)

        # Also add the translations to the models to follow
        self.follow = list(self.follow) + [model._parler_meta.root_rel_name]

        # And make sure that when we revert them, we update the translations
        # cache (this is normally done in the translation `save_base` method,
        # but it is not caled when reverting changes).
        post_save.connect(self._update_cache, sender=root_model)

    def _update_cache(self, sender, instance, raw, **kwargs):
        if raw:
            # Raw is set to true only when restoring from fixtures
            cache._cache_translation(instance)


register_translatable = partial(reversion.register,
                                adapter_cls=TranslatableVersionAdapter,
                                revision_manager=reversion)


@register_translatable
class Article(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('Title'), max_length=234),

        content = PlaceholderField(
            'aldryn_newsblog_article_content',
            related_name='aldryn_newsblog_articles'),
    )

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
