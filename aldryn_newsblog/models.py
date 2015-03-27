# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import datetime

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils.encoding import python_2_unicode_compatible
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode
from django.utils.text import slugify as default_slugify
from django.utils.translation import get_language, ugettext_lazy as _
from django.contrib.auth.models import User
from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.image import FilerImageField

from aldryn_categories.fields import CategoryManyToManyField
from aldryn_categories.models import Category
from aldryn_people.models import Person
from aldryn_reversion.core import version_controlled_content
from parler.models import TranslatableModel, TranslatedFields
from taggit.managers import TaggableManager
from sortedm2m.fields import SortedManyToManyField

from .cms_appconfig import NewsBlogConfig
from .managers import RelatedManager
from .utils import strip_tags, get_plugin_index_data, get_request

import django.core.validators

if settings.LANGUAGES:
    LANGUAGE_CODES = [language[0] for language in settings.LANGUAGES]
elif settings.LANGUAGE:
    LANGUAGE_CODES = [settings.LANGUAGE]
else:
    raise ImproperlyConfigured(
        'Neither LANGUAGES nor LANGUAGE was found in settings.')


@python_2_unicode_compatible
@version_controlled_content
class Article(TranslatableModel):
    translations = TranslatedFields(
        title=models.CharField(_('title'), max_length=234),
        slug=models.SlugField(
            verbose_name=_('slug'),
            max_length=255,
            db_index=True,
            blank=True,
            help_text=_(
                'Used in the URL. If changed, the URL will change. '
                'Clear it to have it re-created automatically.'),
        ),
        lead_in=HTMLField(
            verbose_name=_('Optional lead-in'), default='',
            help_text=_('Will be displayed in lists, and at the start of the '
                        'detail page (in bold)'),
            blank=True,
        ),
        meta_title=models.CharField(
            max_length=255, verbose_name=_('meta title'),
            blank=True, default=''),
        meta_description=models.TextField(
            verbose_name=_('meta description'), blank=True, default=''),
        meta_keywords=models.TextField(
            verbose_name=_('meta keywords'), blank=True, default=''),
        meta={'unique_together': (('language_code', 'slug', ), )},

        search_data=models.TextField(blank=True, editable=False)
    )

    content = PlaceholderField('newsblog_article_content',
                               related_name='newsblog_article_content')
    author = models.ForeignKey(Person, null=True, blank=True,
                               verbose_name=_('author'))
    owner = models.ForeignKey(User, verbose_name=_('owner'))
    app_config = models.ForeignKey(NewsBlogConfig,
                                   verbose_name=_('app. config'))
    categories = CategoryManyToManyField('aldryn_categories.Category',
                                         verbose_name=_('categories'),
                                         blank=True)
    publishing_date = models.DateTimeField(_('publishing date'),
                                           default=datetime.datetime.now)
    is_published = models.BooleanField(_('is published'), default=True,
                                       db_index=True)
    is_featured = models.BooleanField(_('is featured'), default=False,
                                      db_index=True)
    featured_image = FilerImageField(null=True, blank=True)

    tags = TaggableManager(blank=True)

    related = SortedManyToManyField('self',
        verbose_name=_('related articles'), blank=True)

    objects = RelatedManager()

    class Meta:
        ordering = ['-publishing_date']

    def __str__(self):
        return self.safe_translation_getter('title', any_language=True)

    def get_absolute_url(self):
        #
        # NB: It is important that this is safe to run even when the user has
        # not created the apphook yet, as some user work-flows involve creating
        # articles before the page exists.
        #
        try:
            return reverse(
                '{namespace}:article-detail'.format(
                    namespace=self.app_config.namespace
                ), kwargs={
                    'slug': self.safe_translation_getter('slug', any_language=True)
                }
            )
        except:
            return ''  # Note NOT None here

    def slugify(self, source_text, i=None):
        slug = default_slugify(source_text)
        if i is not None:
            slug += "_%d" % i
        return slug

    def get_search_data(self, language=None, request=None):
        """
        Provides an index for use with Haystack, or, for populating
        Article.translations.search_data.
        """
        if not self.pk:
            return ''
        if language is None:
            language = get_language()
        if request is None:
            request = get_request(language=language)
        description = self.safe_translation_getter('lead_in')
        text_bits = [strip_tags(description)]
        for category in self.categories.all():
            text_bits.append(
                force_unicode(category.safe_translation_getter('name')))
        for tag in self.tags.all():
            text_bits.append(force_unicode(tag.name))
        if self.content:
            plugins = self.content.cmsplugin_set.filter(language=language)
            for base_plugin in plugins:
                plugin_text_content = ' '.join(
                    get_plugin_index_data(base_plugin, request))
                text_bits.append(plugin_text_content)
        return ' '.join(text_bits)

    def save(self, *args, **kwargs):
        # Update the search index
        self.search_data = self.get_search_data()

        # Ensure there is an owner.
        if self.app_config.create_authors and self.author is None:
            self.author = Person.objects.get_or_create(
                user=self.owner,
                defaults={
                    'name': u' '.join((self.owner.first_name,
                                       self.owner.last_name))
                })[0]

        # Start with a naïve approach, if none provided.
        if not self.slug:
            self.slug = default_slugify(self.title)

        # Ensure we aren't colliding with an existing slug *for this language*.
        if Article.objects.translated(
                slug=self.slug).exclude(id=self.id).count() == 0:
            return super(Article, self).save(*args, **kwargs)

        for lang in LANGUAGE_CODES:
            #
            # We'd much rather just do something like:
            # Article.objects.translated(lang,
            # slug__startswith=self.slug)
            # But sadly, this isn't supported by Parler/Django, see:
            # http://django-parler.readthedocs.org/en/latest/api/\
            # parler.managers.html#the-translatablequeryset-class
            #
            slugs = []
            all_slugs = Article.objects.language(lang).exclude(
                id=self.id).values_list('translations__slug', flat=True)
            for slug in all_slugs:
                if slug and slug.startswith(self.slug):
                    slugs.append(slug)
            i = 1
            while True:
                slug = self.slugify(self.title, i)
                if slug not in slugs:
                    self.slug = slug
                    return super(Article, self).save(*args, **kwargs)
                i += 1


class NewsBlogCMSPlugin(CMSPlugin):
    """AppHookConfig aware abstract CMSPlugin class for Aldryn Newsblog"""
    # avoid reverse relation name clashes by not adding a related_name
    # to the parent plugin
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='+', parent_link=True)

    app_config = models.ForeignKey(NewsBlogConfig)

    def copy_relations(self, old_instance):
        self.app_config = old_instance.app_config

    class Meta:
        abstract = True


@python_2_unicode_compatible
class NewsBlogArchivePlugin(NewsBlogCMSPlugin):
    def __str__(self):
        return _('%s archive') % (self.app_config.get_app_title(), )


class NewsBlogArticleSearchPlugin(NewsBlogCMSPlugin):
    max_articles = models.PositiveIntegerField(_('max articles'), default=10,
        validators=[django.core.validators.MinValueValidator(1)],
        help_text=_('The maximum number of found articles display.')
    )

    def __str__(self):
        return _('%s archive') % (self.app_config.get_app_title(), )


@python_2_unicode_compatible
class NewsBlogAuthorsPlugin(NewsBlogCMSPlugin):
    def __str__(self):
        return _('%s authors') % (self.app_config.get_app_title(), )

    def get_authors(self):
        author_list = Article.objects.published().filter(
            app_config=self.app_config).values_list('author',
                                                    flat=True).distinct()
        author_list = list(author_list)
        qs = Person.objects.filter(
            id__in=author_list, article__app_config=self.app_config
        ).annotate(count=models.Count('article'))
        return qs


@python_2_unicode_compatible
class NewsBlogCategoriesPlugin(NewsBlogCMSPlugin):
    def __str__(self):
        return _('%s categories') % (self.app_config.get_app_title(), )

    def get_categories(self):
        category_list = Article.objects.published().filter(
            app_config=self.app_config).values_list('categories',
                                                    flat=True).distinct()
        category_list = list(category_list)
        qs = Category.objects.filter(
            id__in=category_list,
            article__app_config=self.app_config,
        ).annotate(count=models.Count('article')).order_by('-count')
        return qs


@python_2_unicode_compatible
class NewsBlogFeaturedArticlesPlugin(NewsBlogCMSPlugin):
    article_count = models.PositiveIntegerField(
        default=1,
        validators=[django.core.validators.MinValueValidator(1)],
        help_text=_('The maximum number of featured articles display.')
    )

    def get_articles(self):
        if not self.article_count:
            return Article.objects.none()
        articles = Article.objects.published().active_translations(
            get_language()
        ).filter(
            app_config=self.app_config,
            is_featured=True
        )
        return articles[:self.article_count]

    def __str__(self):
        if not self.pk:
            return 'featured articles'
        prefix = self.app_config.get_app_title()
        if self.article_count == 1:
            title = _('featured article')
        else:
            title = _('featured articles: %(count)s') % {
                'count': self.article_count,
            }
        return '{0} {1}'.format(prefix, title)


@python_2_unicode_compatible
class NewsBlogLatestArticlesPlugin(NewsBlogCMSPlugin):
    latest_articles = models.IntegerField(
        default=5,
        help_text=_('The maximum number of latest articles to display.')
    )

    def __str__(self):
        return _('%s latest articles: %s') % (
            self.app_config.get_app_title(), self.latest_articles, )

    def get_articles(self):
        articles = Article.objects.published().active_translations(
            get_language()).filter(app_config=self.app_config)
        return articles[:self.latest_articles]


@python_2_unicode_compatible
class NewsBlogRelatedPlugin(CMSPlugin):
    # NOTE: This one does NOT subclass NewsBlogCMSPlugin
    cmsplugin_ptr = models.OneToOneField(
        CMSPlugin, related_name='+', parent_link=True)

    def __str__(self):
        return _('Related articles')


@python_2_unicode_compatible
class NewsBlogTagsPlugin(NewsBlogCMSPlugin):
    def __str__(self):
        return _('%s tags') % (self.app_config.get_app_title(), )

    def get_tags(self):
        tags = {}
        articles = Article.objects.published().filter(
            app_config=self.app_config)
        for article in articles:
            for tag in article.tags.all():
                if tag.id in tags:
                    tags[tag.id].count += 1
                else:
                    tag.count = 1
                    tags[tag.id] = tag
        # Return most frequently used tags first
        return sorted(tags.values(), key=lambda x: x.count, reverse=True)


@receiver(post_save)
def update_seach_index(sender, instance, **kwargs):
    """
    Upon detecting changes in a plugin used in an Article's content
    (PlaceholderField), update the article's search_index so that we can
    perform simple searches even without Haystack, etc.
    """
    if issubclass(instance.__class__, CMSPlugin):
        placeholder = instance._placeholder_cache
        if hasattr(placeholder, '_attached_model_cache'):
            if placeholder._attached_model_cache == Article:
                article = placeholder._attached_model_cache.objects.get(content=placeholder.id)
                article.search_data = article.get_search_data(instance.language)
                article.save()
