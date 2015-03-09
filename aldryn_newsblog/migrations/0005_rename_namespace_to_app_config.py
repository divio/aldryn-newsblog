# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0004_latestentriesplugin_set_namespace_not_null'),
    ]

    operations = [
        migrations.RenameField(
            model_name='article',
            old_name='namespace',
            new_name='app_config',
        ),
        migrations.RenameField(
            model_name='latestentriesplugin',
            old_name='namespace',
            new_name='app_config',
        ),
    ]
