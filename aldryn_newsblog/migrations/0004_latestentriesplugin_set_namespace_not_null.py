# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0003_latestentriesplugin_set_default_namespace'),
    ]

    operations = [
        migrations.AlterField(
            model_name='latestentriesplugin',
            name='namespace',
            field=models.ForeignKey(default=1, to='aldryn_newsblog.NewsBlogConfig'),
            preserve_default=False,
        ),
    ]
