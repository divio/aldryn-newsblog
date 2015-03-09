# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0005_rename_namespace_to_app_config'),
    ]

    # verbose_name changes
    operations = [
        migrations.AlterField(
            model_name='article',
            name='app_config',
            field=models.ForeignKey(verbose_name='app_config', to='aldryn_newsblog.NewsBlogConfig'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='article',
            name='publishing_date',
            field=models.DateTimeField(verbose_name='publishing date'),
            preserve_default=True,
        ),
    ]
