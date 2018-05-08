# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import filer.fields.image
import django.db.models.deletion
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0016_auto_20180329_1417'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='publisher_deletion_requested',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='article',
            name='publisher_is_published_version',
            field=models.BooleanField(default=False, editable=False),
        ),
        migrations.AddField(
            model_name='article',
            name='publisher_published_at',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
        migrations.AddField(
            model_name='article',
            name='publisher_published_version',
            field=models.OneToOneField(related_name='publisher_draft_version', null=True, default=None, editable=False, to='aldryn_newsblog.Article', blank=True),
        ),
        migrations.AlterField(
            model_name='article',
            name='featured_image',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, verbose_name='featured image', blank=True, to=settings.FILER_IMAGE_MODEL, null=True),
        ),
        migrations.AlterField(
            model_name='newsblogconfig',
            name='namespace',
            field=models.CharField(default=None, unique=True, max_length=100, verbose_name='Instance namespace'),
        ),
        migrations.AlterField(
            model_name='newsblogconfig',
            name='type',
            field=models.CharField(max_length=100, verbose_name='Type'),
        ),
    ]
