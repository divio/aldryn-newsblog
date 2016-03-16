# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('aldryn_newsblog', '0009_auto_20160211_1022'),
    ]

    operations = [
        migrations.AddField(
            model_name='newsblogconfig',
            name='pagination_pages_start',
            field=models.PositiveIntegerField(default=10, help_text='When paginating list views, after how many pages should we start grouping the page numbers.', verbose_name='Pagination pages start'),
        ),
        migrations.AddField(
            model_name='newsblogconfig',
            name='pagination_pages_visible',
            field=models.PositiveIntegerField(default=4, help_text='When grouping page numbers, this determines how many pages are visible on each side of the active page.', verbose_name='Pagination pages visible'),
        ),
    ]
