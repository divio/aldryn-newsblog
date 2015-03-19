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
        'aldryn_apphooks_config',
        'aldryn_boilerplates',
        'aldryn_categories',
        'aldryn_newsblog',
        'aldryn_people',
        'aldryn_reversion',
        'djangocms_text_ckeditor',
        'easy_thumbnails',
        'filer',
        'mptt',
        'parler',
        'reversion',
        'sortedm2m',
        'taggit',
    ],
    'STATICFILES_FINDERS': [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        # important! place right before django.contrib.staticfiles.finders.AppDirectoriesFinder
        'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ],
    'TEMPLATE_LOADERS': [
        'django.template.loaders.filesystem.Loader',
        # important! place right before django.template.loaders.app_directories.Loader
        'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
        'django.template.loaders.app_directories.Loader',
    ],
    'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
    # app-specific
    'PARLER_LANGUAGES': {
        1: (
            {'code': 'de', },
            {'code': 'fr', },
            {'code': 'en', },
        ),
        'default': {
            'hide_untranslated': False,
        }
    },
    'HAYSTACK_CONNECTIONS': {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
        'de': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    },
    'MIGRATION_MODULES': {
        'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
        'filer': 'filer.migrations_django',
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
