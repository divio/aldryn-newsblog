# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsblogconfig',
            name='template_prefix',
            field=models.CharField(max_length=20, null=True, verbose_name='Prefix for template dirs', blank=True),
            preserve_default=True,
        ),
    ]
