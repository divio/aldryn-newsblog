#!/usr/bin/env python
# -*- coding: utf-8 -*-

HELPER_SETTINGS = {
    'TIME_ZONE': 'Europe/Zurich',
    'LANGUAGES': (
        ('en', 'English'),
        ('de', 'German'),
        ('fr', 'French'),
    ),
    'INSTALLED_APPS': [
        'reversion',
        'taggit',
        'aldryn_categories',
        'aldryn_newsblog',
        'aldryn_people',
        'filer',
        'djangocms_text_ckeditor',
        'parler',
    ],
    # app-specific
    'ALDRYN_NEWSBLOG_PAGINATE_BY': 10,
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_newsblog')

if __name__ == "__main__":
    run()
