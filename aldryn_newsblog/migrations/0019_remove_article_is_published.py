# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0018_switch_from_is_published_flag_to_djangocms_publisher'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='article',
            name='is_published',
        ),
    ]
