# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0006_article_adjust_verbose_names'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_published',
            field=models.BooleanField(default=True, db_index=True, verbose_name='is published'),
            preserve_default=True,
        ),
    ]
