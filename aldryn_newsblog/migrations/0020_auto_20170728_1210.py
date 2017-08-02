# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0019_remove_article_is_published'),
    ]

    operations = [
        migrations.AddField(
            model_name='articletranslation',
            name='publisher_is_published_translation_version',
            field=models.NullBooleanField(default=None, editable=False),
        ),
        migrations.AlterUniqueTogether(
            name='articletranslation',
            unique_together=set([('language_code', 'master'), ('language_code', 'slug', 'publisher_is_published_translation_version')]),
        ),
    ]
