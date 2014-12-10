from django.db import models
from django.utils import timezone
from django.utils.translation import get_language, ugettext_lazy as _, override

from cms.models.fields import PlaceholderField
from parler.models import TranslatableModel, TranslatedFields
# from filer.fields.image import FilerImageField


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
    publication_start = models.DateTimeField(
        verbose_name=_('Published Since'), default=timezone.now,
        help_text=_('Used in the URL. If changed, the URL will change.')
    )
    publication_end = models.DateTimeField(
        verbose_name=_('Published Until'), null=True, blank=True)
    # key_visual = FilerImageField(verbose_name=_('Key Visual'), blank=True, null=True)
