# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
        ('aldryn_newsblog', '0009_auto_20150310_2226'),
    ]

    operations = [
        migrations.CreateModel(
            name='AuthorsPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('app_config', models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.CreateModel(
            name='CategoriesPlugin',
            fields=[
                ('cmsplugin_ptr', models.OneToOneField(parent_link=True, auto_created=True, primary_key=True, serialize=False, to='cms.CMSPlugin')),
                ('app_config', models.ForeignKey(to='aldryn_newsblog.NewsBlogConfig')),
            ],
            options={
                'abstract': False,
            },
            bases=('cms.cmsplugin',),
        ),
        migrations.AddField(
            model_name='newsblogconfig',
            name='create_authors',
            field=models.BooleanField(default=True, help_text='Automatically create authors from logged-in user?', verbose_name='Auto-create authors?'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newsblogconfig',
            name='paginate_by',
            field=models.PositiveIntegerField(default=5, help_text='When paginating list views, how many articles per page?', verbose_name='Paginate size'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='newsblogconfig',
            name='search_indexed',
            field=models.BooleanField(default=True, help_text='Include articles in search indexes?', verbose_name='Include in search index?'),
            preserve_default=True,
        ),
    ]
