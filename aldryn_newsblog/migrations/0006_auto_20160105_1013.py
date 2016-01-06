# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import djangocms_text_ckeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0005_auto_20150807_0207'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsblogconfig',
            options={'verbose_name': 'config', 'verbose_name_plural': 'configs'},
        ),
        migrations.AlterModelOptions(
            name='newsblogconfigtranslation',
            options={'default_permissions': (), 'verbose_name': 'config Translation', 'managed': True},
        ),
        migrations.AlterField(
            model_name='articletranslation',
            name='lead_in',
            field=djangocms_text_ckeditor.fields.HTMLField(default='', help_text='Optional. Will be displayed in lists, and at the start of the detail page (in bold)', verbose_name='lead-in', blank=True),
        ),
    ]
