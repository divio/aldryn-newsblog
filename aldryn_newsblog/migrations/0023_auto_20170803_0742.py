# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0022_auto_20170802_2315'),
    ]

    operations = [
        migrations.AddField(
            model_name='articletranslation',
            name='publisher_translation_deletion_requested',
            field=models.BooleanField(default=False, db_index=True, editable=False),
        ),
        migrations.AddField(
            model_name='articletranslation',
            name='publisher_translation_published_at',
            field=models.DateTimeField(default=None, null=True, editable=False, blank=True),
        ),
        migrations.AlterUniqueTogether(
            name='articletranslation',
            unique_together=set([('language_code', 'master')]),
        ),
        migrations.RemoveField(
            model_name='articletranslation',
            name='publisher_is_published_translation_version',
        ),
    ]
