# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import sortedm2m.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0014_auto_20160821_1156'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='related',
            field=sortedm2m.fields.SortedManyToManyField(help_text=None, to='aldryn_newsblog.Article', verbose_name='related articles', blank=True),
        ),
    ]
