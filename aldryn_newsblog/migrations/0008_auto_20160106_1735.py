# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import django.db.models.deletion
from django.db import migrations, models

import app_data.fields
import filer.fields.image


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
