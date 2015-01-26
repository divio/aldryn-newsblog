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
        'mptt',
        'taggit',
        'aldryn_categories',
        'aldryn_newsblog',
        'aldryn_people',
        'filer',
        'djangocms_text_ckeditor',
        'parler',
        'easy_thumbnails'
    ],
    # app-specific
    'ALDRYN_NEWSBLOG_PAGINATE_BY': 10,
    'PARLER_LANGUAGES': {
        1: (
            {'code': 'de',},
            {'code': 'fr',},
            {'code': 'en',},
        ),
        'default': {
            'hide_untranslated': False,
        }
    },
    'THUMBNAIL_HIGH_RESOLUTION': True,
    'THUMBNAIL_PROCESSORS': (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        #'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    )
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_newsblog')

if __name__ == "__main__":
    run()
