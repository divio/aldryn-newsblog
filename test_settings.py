#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

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
    'MIGRATION_MODULES': {
        # 'cms': 'cms.migrations_django',
        'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
        'filer': 'filer.migrations_django',
    },
    'TEMPLATE_DIRS': (
        os.path.join(
            os.path.dirname(__file__),
            'aldryn_newsblog', 'tests', 'templates'), ),
    'STATICFILES_FINDERS': [
        'django.contrib.staticfiles.finders.FileSystemFinder',
        # important! place right before:
        #     django.contrib.staticfiles.finders.AppDirectoriesFinder
        'aldryn_boilerplates.staticfile_finders.AppDirectoriesFinder',
        'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    ],
    'TEMPLATE_LOADERS': [
        'django.template.loaders.filesystem.Loader',
        # important! place right before:
        #     django.template.loaders.app_directories.Loader
        'aldryn_boilerplates.template_loaders.AppDirectoriesLoader',
        'django.template.loaders.app_directories.Loader',
    ],
    'ALDRYN_NEWSBLOG_TEMPLATE_PREFIXES': [('dummy', 'dummy'), ],
    'ALDRYN_BOILERPLATE_NAME': 'bootstrap3',
    # app-specific
    'PARLER_LANGUAGES': {
        1: (
            {'code': 'de', },
            {'code': 'fr', },
            {'code': 'en', },
        ),
        'default': {
            'hide_untranslated': True,  # PLEASE DO NOT CHANGE THIS
        }
    },
    'SITE_ID': 1,
    'CMS_LANGUAGES': {
        1: [
            {
                'code': 'de',
                'name': 'Deutsche',
                'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'fr' HERE
            },
            {
                'code': 'fr',
                'name': 'Française',
                'fallbacks': ['en', ]  # FOR TESTING DO NOT ADD 'de' HERE
            },
            {
                'code': 'en',
                'name': 'English',
                'fallbacks': ['de', 'fr', ]
            },
            {
                'code': 'it',
                'name': 'Italiano',
                'fallbacks': ['fr', ]  # FOR TESTING, LEAVE AS ONLY 'fr'
            },
        ],
        'default': {
            'redirect_on_fallback': True,  # PLEASE DO NOT CHANGE THIS
        }
    },
    #
    # NOTE: The following setting `PARLER_ENABLE_CACHING = False` is required
    # for tests to pass.
    #
    # There appears to be a bug in Parler which leaves translations in Parler's
    # cache even after the parent object has been deleted. In production
    # environments, this is unlikely to affect anything, because newly created
    # objects will have new IDs. In testing, new objects are created with IDs
    # that were previously used, which reveals this issue.
    #
    'PARLER_ENABLE_CACHING': False,
    'HAYSTACK_CONNECTIONS': {
        'default': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
        'de': {
            'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
        },
    },
    'THUMBNAIL_HIGH_RESOLUTION': True,
    'THUMBNAIL_PROCESSORS': (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        # 'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    ),
    # 'DATABASES': {
    #     'default': {
    #         'ENGINE': 'django.db.backends.sqlite3',
    #         'NAME': 'mydatabase',
    #     },
    #     'mysql': {
    #         'ENGINE': 'django.db.backends.mysql',
    #         'NAME': 'newsblog_test',
    #         'USER': 'root',
    #         'PASSWORD': '',
    #         'HOST': '',
    #         'PORT': '3306',
    #     },
    #     'postgres': {
    #         'ENGINE': 'django.db.backends.postgresql_psycopg2',
    #         'NAME': 'newsblog_test',
    #         'USER': 'test',
    #         'PASSWORD': '',
    #         'HOST': '127.0.0.1',
    #         'PORT': '5432',
    #     }
    # }
}


def run():
    from djangocms_helper import runner
    runner.cms('aldryn_newsblog')

if __name__ == "__main__":
    run()
