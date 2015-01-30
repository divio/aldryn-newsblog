# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='latestentriesplugin',
            name='namespace',
            field=models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig', null=True),
            preserve_default=True,
        ),
    ]
