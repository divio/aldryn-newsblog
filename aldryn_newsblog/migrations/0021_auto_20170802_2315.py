# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0020_auto_20170728_1210'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='publisher_deletion_requested',
            field=models.BooleanField(default=False, db_index=True, editable=False),
        ),
        migrations.AlterField(
            model_name='article',
            name='publisher_is_published_version',
            field=models.BooleanField(default=False, db_index=True, editable=False),
        ),
    ]
