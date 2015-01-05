from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.utils import timezone
from django.utils.translation import get_language, ugettext_lazy as _, override
from django.contrib.auth.models import User

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from parler.models import TranslatableModel, TranslatedFields
from aldryn_people.models import Person


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
