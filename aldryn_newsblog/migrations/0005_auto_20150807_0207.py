# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0004_auto_20150622_1606'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsblogconfig',
            name='template_prefix',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Prefix for template dirs', choices=[(b'dummy', b'dummy')]),
            preserve_default=True,
        ),
    ]
