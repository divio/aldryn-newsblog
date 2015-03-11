# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import datetime
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0008_article_is_featured'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='app_config',
            field=models.ForeignKey(verbose_name='app. config', to='aldryn_newsblog.NewsBlogConfig'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='publishing_date',
            field=models.DateTimeField(default=datetime.datetime.now, verbose_name='publishing date'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='articletranslation',
            name='lead_in',
            field=djangocms_text_ckeditor.fields.HTMLField(default='', help_text='Will be displayed in lists, and at the start of the detail page (in bold)', verbose_name='Optional lead-in', blank=True),
            preserve_default=True,
        ),
    ]
