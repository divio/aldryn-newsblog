# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0007_article_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='is_featured',
            field=models.BooleanField(default=False, db_index=True, verbose_name='is featured'),
            preserve_default=True,
        ),
    ]
