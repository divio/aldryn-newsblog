from django.db import models
from django.utils import timezone
from django.utils.translation import get_language, ugettext_lazy as _, override

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from parler.models import TranslatableModel, TranslatedFields
# from filer.fields.image import FilerImageField


class PublishedManager(models.Manager):
    def __init__(self, is_published=True):
        super(PublishedManager, self).__init__()
        self.is_published = is_published

    def get_query_set(self):
        return super(PublishedManager, self).get_query_set().filter(
            is_published=self.is_published)


class Article(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('Title'), max_length=234),

        content = PlaceholderField(
            'aldryn_newsblog_article_content',
            related_name='aldryn_newsblog_articles'),

        slug = models.SlugField(
            verbose_name=_('Slug'),
            max_length=255,
            unique=True,
            blank=True,
            help_text=_(
                'Used in the URL. If changed, the URL will change. '
                'Clean it to have it re-created.'),
        )
    )

    is_published = models.BooleanField(default=False)

    def publish(self):
        """Publish this article.

        If the instance is a draft, find the corresponding published instance
        and update it. If a published instance doesn't exist, create one."""
        # TODO : find existing object
        published_instance = self.__class__.objects.create(**dict([
            (fld.name, getattr(self, fld.name)) for fld
            in self._meta.fields
            if fld.name != self._meta.pk.name]))
        # TODO : clone translated instances
        published_instance.is_published = True
        published_instance.save()
        return published_instance

    published_objects = PublishedManager(is_published=True)
    draft_objects = PublishedManager(is_published=False)
