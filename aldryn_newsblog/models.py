from __future__ import unicode_literals

from django.core.urlresolvers import reverse
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.text import slugify
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from aldryn_people.models import Person
from parler.models import TranslatableModel, TranslatedFields
from aldryn_apphooks_config.models import AppHookConfig
from aldryn_categories.fields import CategoryManyToManyField
from taggit.managers import TaggableManager
from djangocms_text_ckeditor.fields import HTMLField

from .versioning import version_controlled_content


class NewsBlogConfig(AppHookConfig):
    pass


@python_2_unicode_compatible
@version_controlled_content
class Article(TranslatableModel):
    translations = TranslatedFields(
        title = models.CharField(_('Title'), max_length=234),

        lead_in = HTMLField(
            verbose_name=_('Lead-in'), default='',
            help_text=_('Will be displayed in lists, and at the start of the '
                        'detail page (in bold)')),

        meta_title=models.CharField(
            max_length=255, verbose_name=_('meta title'),
            blank=True, default=''),
        meta_description=models.TextField(
            verbose_name=_('meta description'), blank=True, default=''),
        meta_keywords=models.TextField(
            verbose_name=_('meta keywords'), blank=True, default='')
    )

    content = PlaceholderField('aldryn_newsblog_article_content',
                               related_name='aldryn_newsblog_articles',
                               unique=True)

    slug = models.SlugField(
        verbose_name=_('Slug'),
        max_length=255,
        unique=True,
        blank=True,
        help_text=_(
            'Used in the URL. If changed, the URL will change. '
            'Clean it to have it re-created.'),
    )

    author = models.ForeignKey(Person, null=True, blank=True)
    owner = models.ForeignKey(User)
    namespace = models.ForeignKey(NewsBlogConfig)
    categories = CategoryManyToManyField('aldryn_categories.Category',
                                         blank=True)
    tags = TaggableManager(blank=True)
    publishing_date = models.DateTimeField()

    class Meta:
        ordering = ['-publishing_date']

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    def get_absolute_url(self):
        return reverse('aldryn_newsblog:article-detail',
                       kwargs={'slug': self.slug},
                       current_app=self.namespace.namespace)

    def save(self, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.author is None:
            self.author, _ = Person.objects.get_or_create(
                user=self.owner,
                defaults={
                    'name': u' '.join((self.owner.first_name,
                                       self.owner.last_name))
                })
        return super(Article, self).save(**kwargs)


@python_2_unicode_compatible
class LatestEntriesPlugin(CMSPlugin):

    latest_entries = models.IntegerField(
        default=5,
        help_text=_('The number of latest entries to be displayed.')
    )

    # TODO: make sure not to forget this if we add m2m/fk fields for
    # _this_plugin_ later:
    # def copy_relations(self, old_instance):
    #     self.categories = old_instance.categories.all()
    #     self.tags = old_instance.tags.all()

    def __str__(self):
        return u'Latest entries: {0}'.format(self.latest_entries)

    def get_articles(self):
        articles = Article.objects.active_translations()
        return articles[:self.latest_entries]
