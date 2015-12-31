# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers
import aldryn_categories.fields
import aldryn_newsblog.models
import filer.fields.image
from django.conf import settings
import sortedm2m.fields
import django.utils.timezone
import djangocms_text_ckeditor.fields
import cms.models.fields
import app_data.fields
import aldryn_apphooks_config.fields
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('cms', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aldryn_people', '0001_initial'),
        ('filer', '0001_initial'),
        ('aldryn_categories', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publishing_date', models.DateTimeField(default=django.utils.timezone.now, verbose_name='publishing date')),
                ('is_published', models.BooleanField(default=True, db_index=True, verbose_name='is published')),
                ('is_featured', models.BooleanField(default=False, db_index=True, verbose_name='is featured')),
            ],
            options={
                'ordering': ['-publishing_date'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ArticleTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('title', models.CharField(max_length=234, verbose_name='title')),
                ('slug', models.SlugField(help_text='Used in the URL. If changed, the URL will change. Clear it to have it re-created automatically.', max_length=255, verbose_name='slug', blank=True)),
                ('lead_in', djangocms_text_ckeditor.fields.HTMLField(default='', help_text='Will be displayed in lists, and at the start of the detail page (in bold)', verbose_name='Optional lead-in', blank=True)),
                ('meta_title', models.CharField(default='', max_length=255, verbose_name='meta title', blank=True)),
                ('meta_description', models.TextField(default='', verbose_name='meta description', blank=True)),
                ('meta_keywords', models.TextField(default='', verbose_name='meta keywords', blank=True)),
                ('search_data', models.TextField(editable=False, blank=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_newsblog.Article', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'aldryn_newsblog_article_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'article Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsBlogArchivePlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_newsblog.models.PluginEditModeMixin, 'cms.cmsplugin'),
        ),
        migrations.CreateModel(
            name='NewsBlogArticleSearchPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('max_articles', models.PositiveIntegerField(default=10, help_text='The maximum number of found articles display.', verbose_name='max articles', validators=[django.core.validators.MinValueValidator(1)])),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='NewsBlogAuthorsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_newsblog.models.PluginEditModeMixin, 'cms.cmsplugin'),
        ),
        migrations.CreateModel(
            name='NewsBlogCategoriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_newsblog.models.PluginEditModeMixin, 'cms.cmsplugin'),
        ),
        migrations.CreateModel(
            name='NewsBlogConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='type')),
                ('namespace', models.CharField(default=None, unique=True, max_length=100, verbose_name='instance namespace')),
                ('app_data', app_data.fields.AppDataField(default=dict, editable=False)),
                ('permalink_type', models.CharField(default='slug', help_text='Choose the style of urls to use from the examples. (Note, all types are relative to apphook)', max_length=8, verbose_name='permalink type', choices=[('s', 'the-eagle-has-landed/'), ('ys', '1969/the-eagle-has-landed/'), ('yms', '1969/07/the-eagle-has-landed/'), ('ymds', '1969/07/16/the-eagle-has-landed/'), ('ymdi', '1969/07/16/11/')])),
                ('non_permalink_handling', models.SmallIntegerField(default=302, help_text='How to handle non-permalink urls?', verbose_name='non-permalink handling', choices=[(200, 'Allow'), (302, 'Redirect to permalink (default)'), (301, 'Permanent redirect to permalink'), (404, 'Return 404: Not Found')])),
                ('paginate_by', models.PositiveIntegerField(default=5, help_text='When paginating list views, how many articles per page?', verbose_name='Paginate size')),
                ('create_authors', models.BooleanField(default=True, help_text='Automatically create authors from logged-in user?', verbose_name='Auto-create authors?')),
                ('search_indexed', models.BooleanField(default=True, help_text='Include articles in search indexes?', verbose_name='Include in search index?')),
                ('placeholder_base_sidebar', cms.models.fields.PlaceholderField(related_name='aldryn_newsblog_base_sidebar', slotname='newsblog_base_sidebar', editable=False, to='cms.Placeholder', null=True)),
                ('placeholder_base_top', cms.models.fields.PlaceholderField(related_name='aldryn_newsblog_base_top', slotname='newsblog_base_top', editable=False, to='cms.Placeholder', null=True)),
                ('placeholder_detail_bottom', cms.models.fields.PlaceholderField(related_name='aldryn_newsblog_detail_bottom', slotname='newsblog_detail_bottom', editable=False, to='cms.Placeholder', null=True)),
                ('placeholder_detail_footer', cms.models.fields.PlaceholderField(related_name='aldryn_newsblog_detail_footer', slotname='newsblog_detail_footer', editable=False, to='cms.Placeholder', null=True)),
                ('placeholder_detail_top', cms.models.fields.PlaceholderField(related_name='aldryn_newsblog_detail_top', slotname='newsblog_detail_top', editable=False, to='cms.Placeholder', null=True)),
                ('placeholder_list_footer', cms.models.fields.PlaceholderField(related_name='aldryn_newsblog_list_footer', slotname='newsblog_list_footer', editable=False, to='cms.Placeholder', null=True)),
                ('placeholder_list_top', cms.models.fields.PlaceholderField(related_name='aldryn_newsblog_list_top', slotname='newsblog_list_top', editable=False, to='cms.Placeholder', null=True)),
            ],
            options={
                'abstract': False,
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsBlogConfigTranslation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('language_code', models.CharField(max_length=15, verbose_name='Language', db_index=True)),
                ('app_title', models.CharField(max_length=234, verbose_name='application title')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_newsblog.NewsBlogConfig', null=True)),
            ],
            options={
                'managed': True,
                'db_table': 'aldryn_newsblog_newsblogconfig_translation',
                'db_tablespace': '',
                'default_permissions': (),
                'verbose_name': 'news blog config Translation',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='NewsBlogFeaturedArticlesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('article_count', models.PositiveIntegerField(default=1, help_text='The maximum number of featured articles display.', validators=[django.core.validators.MinValueValidator(1)])),
                ('app_config', models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig')),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_newsblog.models.PluginEditModeMixin, 'cms.cmsplugin'),
        ),
        migrations.CreateModel(
            name='NewsBlogLatestArticlesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('latest_articles', models.IntegerField(default=5, help_text='The maximum number of latest articles to display.')),
                ('app_config', models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig')),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_newsblog.models.PluginEditModeMixin, 'cms.cmsplugin'),
        ),
        migrations.CreateModel(
            name='NewsBlogRelatedPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_newsblog.models.PluginEditModeMixin, 'cms.cmsplugin'),
        ),
        migrations.CreateModel(
            name='NewsBlogTagsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, related_name='+', primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('app_config', models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig')),
            ],
            options={
                'abstract': False,
            },
            bases=(aldryn_newsblog.models.PluginEditModeMixin, 'cms.cmsplugin'),
        ),
        migrations.AlterUniqueTogether(
            name='newsblogconfigtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AddField(
            model_name='newsblogcategoriesplugin',
            name='app_config',
            field=models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newsblogauthorsplugin',
            name='app_config',
            field=models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newsblogarticlesearchplugin',
            name='app_config',
            field=models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newsblogarchiveplugin',
            name='app_config',
            field=models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig'),
            preserve_default=True,
        ),
        migrations.AlterUniqueTogether(
            name='articletranslation',
            unique_together=set([('language_code', 'master'), ('language_code', 'slug')]),
        ),
        migrations.AddField(
            model_name='article',
            name='app_config',
            field=aldryn_apphooks_config.fields.AppHookConfigField(verbose_name='app. config', to='aldryn_newsblog.NewsBlogConfig', help_text='When selecting a value, the form is reloaded to get the updated default'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='author',
            field=models.ForeignKey(verbose_name='author', blank=True, to='aldryn_people.Person', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='categories',
            field=aldryn_categories.fields.CategoryManyToManyField(to='aldryn_categories.Category', verbose_name='categories', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='content',
            field=cms.models.fields.PlaceholderField(related_name='newsblog_article_content', slotname='newsblog_article_content', editable=False, to='cms.Placeholder', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='featured_image',
            field=filer.fields.image.FilerImageField(blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='owner',
            field=models.ForeignKey(verbose_name='owner', to=settings.AUTH_USER_MODEL),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='related',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, related_name='related_rel_+', verbose_name='related articles', to='aldryn_newsblog.Article', blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='article',
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
