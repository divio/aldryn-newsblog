# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import filer.fields.image
import django.db.models.deletion
import app_data.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0007_default_newsblog_config'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='featured_image',
            field=filer.fields.image.FilerImageField(on_delete=django.db.models.deletion.SET_NULL, blank=True, to='filer.Image', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='newsblogconfig',
            name='app_data',
            field=app_data.fields.AppDataField(default=b'{}', editable=False),
            preserve_default=True,
        ),
    ]
