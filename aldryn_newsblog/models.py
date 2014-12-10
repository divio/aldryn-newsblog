from django.db import models
from django.utils import timezone
from django.utils.translation import get_language, ugettext_lazy as _, override

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from parler.models import TranslatableModel, TranslatedFields
# from filer.fields.image import FilerImageField


class Article(TranslatableModel):
    CLONE_FIELDS = ['title', ]
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

    published = models.BooleanField(default=False)

    def publish(self):
        """Publish this article.

        If the instance is a draft, find the corresponding published instance
        and update it. If a published instance doesn't exist, create one."""
        # TODO : find existing object
        published_instance = self.__class__()
        # TODO : copy values from draft to published instance
        # TODO : clone translated instances
        published_instance.published = True
        published_instance.save()

    @property
    def published(self):
        return self.objects.filter(published=True)

    @property
    def drafts(self):
        return self.objects.filter(published=False)
