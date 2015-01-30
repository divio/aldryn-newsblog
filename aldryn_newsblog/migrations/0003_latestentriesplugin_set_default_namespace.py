# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


def create_default_namespace(apps, schema_editor):
    NewsBlogConfig = apps.get_model("aldryn_newsblog", "NewsBlogConfig")
    LatestEntriesPlugin = apps.get_model("aldryn_newsblog", "LatestEntriesPlugin")

    ns, created = NewsBlogConfig.objects.get_or_create(
        namespace='latest_entries_plugin_default_namespace')

    for plugin in LatestEntriesPlugin.objects.all():
        if plugin.namespace is None:
            plugin.namespace = ns
            plugin.save()


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0002_latestentriesplugin_namespace'),
    ]

    operations = [
        migrations.RunPython(create_default_namespace),
    ]
