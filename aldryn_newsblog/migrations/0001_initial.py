# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import app_data.fields
import djangocms_text_ckeditor.fields
import aldryn_categories.fields
from django.conf import settings
import filer.fields.image
import cms.models.fields
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('taggit', '0001_initial'),
        ('aldryn_people', '0002_auto_20150128_1411'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('cms', '0003_auto_20140926_2347'),
        ('aldryn_categories', '0003_auto_20150128_1359'),
        ('filer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Article',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('publishing_date', models.DateTimeField(verbose_name='publishing data')),
                ('author', models.ForeignKey(verbose_name='author', blank=True, to='aldryn_people.Person', null=True)),
                ('categories', aldryn_categories.fields.CategoryManyToManyField(to='aldryn_categories.Category', verbose_name='categories', blank=True)),
                ('content', cms.models.fields.PlaceholderField(related_name='aldryn_newsblog_articles', null=True, slotname='aldryn_newsblog_article_content', editable=False, to='cms.Placeholder', unique=True)),
                ('featured_image', filer.fields.image.FilerImageField(blank=True, to='filer.Image', null=True)),
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
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('title', models.CharField(max_length=234, verbose_name='title')),
                ('slug', models.SlugField(help_text='Used in the URL. If changed, the URL will change. Clear it to have it re-created automatically.', max_length=255, verbose_name='slug', blank=True)),
                ('lead_in', djangocms_text_ckeditor.fields.HTMLField(default='', help_text='Will be displayed in lists, and at the start of the detail page (in bold)', verbose_name='lead-in')),
                ('meta_title', models.CharField(default='', max_length=255, verbose_name='meta title', blank=True)),
                ('meta_description', models.TextField(default='', verbose_name='meta description', blank=True)),
                ('meta_keywords', models.TextField(default='', verbose_name='meta keywords', blank=True)),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_newsblog.Article', null=True)),
            ],
            options={
                'db_table': 'aldryn_newsblog_article_translation',
                'verbose_name': 'article Translation',
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='LatestEntriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('latest_entries', models.IntegerField(default=5, help_text='The number of latest entries to be displayed.')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='NewsBlogConfig',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('type', models.CharField(max_length=100, verbose_name='type')),
                ('namespace', models.CharField(default=None, max_length=100, verbose_name='instance namespace')),
                ('app_data', app_data.fields.AppDataField(default=b'{}', editable=False)),
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
                ('language_code', models.CharField(db_index=True, max_length=15, verbose_name='Language')),
                ('app_title', models.CharField(max_length=234, verbose_name='application title')),
                ('master', models.ForeignKey(related_name='translations', editable=False, to='aldryn_newsblog.NewsBlogConfig', null=True)),
            ],
            options={
                'db_table': 'aldryn_newsblog_newsblogconfig_translation',
                'verbose_name': 'news blog config Translation',
                'default_permissions': (),
            },
            bases=(models.Model,),
        ),
        migrations.AlterUniqueTogether(
            name='newsblogconfigtranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.AlterUniqueTogether(
            name='articletranslation',
            unique_together=set([('language_code', 'master'), ('language_code', 'slug')]),
        ),
        migrations.AddField(
            model_name='article',
            name='namespace',
            field=models.ForeignKey(verbose_name='namespace', to='aldryn_newsblog.NewsBlogConfig'),
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
            name='tags',
            field=taggit.managers.TaggableManager(to='taggit.Tag', through='taggit.TaggedItem', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
