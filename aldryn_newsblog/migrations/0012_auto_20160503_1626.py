# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import aldryn_apphooks_config.fields


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0011_auto_20160412_1622'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='newsblogconfig',
            options={'verbose_name': 'application configuration', 'verbose_name_plural': 'application configurations'},
        ),
        migrations.AlterModelOptions(
            name='newsblogconfigtranslation',
            options={'default_permissions': (), 'verbose_name': 'application configuration Translation', 'managed': True},
        ),
        migrations.AlterField(
            model_name='article',
            name='app_config',
            field=aldryn_apphooks_config.fields.AppHookConfigField(verbose_name='Apphook configuration', to='aldryn_newsblog.NewsBlogConfig', help_text='When selecting a value, the form is reloaded to get the updated default'),
        ),
        migrations.AlterField(
            model_name='newsblogarchiveplugin',
            name='app_config',
            field=models.ForeignKey(verbose_name='Apphook configuration', to='aldryn_newsblog.NewsBlogConfig'),
        ),
        migrations.AlterField(
            model_name='newsblogarticlesearchplugin',
            name='app_config',
            field=models.ForeignKey(verbose_name='Apphook configuration', to='aldryn_newsblog.NewsBlogConfig'),
        ),
        migrations.AlterField(
            model_name='newsblogauthorsplugin',
            name='app_config',
            field=models.ForeignKey(verbose_name='Apphook configuration', to='aldryn_newsblog.NewsBlogConfig'),
        ),
        migrations.AlterField(
            model_name='newsblogcategoriesplugin',
            name='app_config',
            field=models.ForeignKey(verbose_name='Apphook configuration', to='aldryn_newsblog.NewsBlogConfig'),
        ),
        migrations.AlterField(
            model_name='newsblogfeaturedarticlesplugin',
            name='app_config',
            field=models.ForeignKey(verbose_name='Apphook configuration', to='aldryn_newsblog.NewsBlogConfig'),
        ),
        migrations.AlterField(
            model_name='newsbloglatestarticlesplugin',
            name='app_config',
            field=models.ForeignKey(verbose_name='Apphook configuration', to='aldryn_newsblog.NewsBlogConfig'),
        ),
        migrations.AlterField(
            model_name='newsblogtagsplugin',
            name='app_config',
            field=models.ForeignKey(verbose_name='Apphook configuration', to='aldryn_newsblog.NewsBlogConfig'),
        ),
    ]
