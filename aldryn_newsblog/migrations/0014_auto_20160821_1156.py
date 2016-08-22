# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0013_auto_20160623_1703'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsblogarchiveplugin',
            name='cache_duration',
            field=models.PositiveSmallIntegerField(default=0, help_text="The maximum duration (in seconds) that this plugin's content should be cached."),
        ),
        migrations.AlterField(
            model_name='newsbloglatestarticlesplugin',
            name='cache_duration',
            field=models.PositiveSmallIntegerField(default=0, help_text="The maximum duration (in seconds) that this plugin's content should be cached."),
        ),
        migrations.AlterField(
            model_name='newsblogrelatedplugin',
            name='cache_duration',
            field=models.PositiveSmallIntegerField(default=0, help_text="The maximum duration (in seconds) that this plugin's content should be cached."),
        ),
    ]
