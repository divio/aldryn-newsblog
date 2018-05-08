# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0017_auto_20170726_0827'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='articletranslation',
            unique_together=set([('language_code', 'master')]),
        ),
    ]
