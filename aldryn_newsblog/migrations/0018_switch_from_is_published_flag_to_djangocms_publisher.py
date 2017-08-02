# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


def to_djangocms_publisher(apps, schema_editor):
    Article = apps.get_model('aldryn_newsblog', 'Article')
    (
        Article.objects
        .filter(is_published=True)
        .update(publisher_is_published_version=True)
    )
    (
        Article.objects
        .filter(is_published=False)
        .update(publisher_is_published_version=False)
    )


def back_to_native(apps, schema_editor):
    Article = apps.get_model('aldryn_newsblog', 'Article')
    (
        Article.objects
        .filter(publisher_is_published_version=True)
        .update(is_published=True)
    )
    (
        Article.objects
        .filter(publisher_is_published_version=False)
        .update(is_published=False)
    )


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0017_auto_20170727_0724'),
    ]

    operations = [
        migrations.RunPython(
            to_djangocms_publisher,
            reverse_code=back_to_native,
        )
    ]
