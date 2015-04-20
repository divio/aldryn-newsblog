#!/usr/bin/env python

import django
from django.conf.urls import patterns

import app_manage

urlpatterns = patterns('')

if __name__ == '__main__':

    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sites',
        'parler',
        'taggit',
        'aldryn_categories',
        'aldryn_people',
        'filer',
        'mptt',
        'cms',
        'treebeard',
    ]

    TEMPLATE_CONTEXT_PROCESSORS = (
        'django.contrib.auth.context_processors.auth',
        'django.contrib.messages.context_processors.messages',
        'django.core.context_processors.i18n',
        'django.core.context_processors.request',
        'django.core.context_processors.media',
        'django.core.context_processors.static',
        'cms.context_processors.cms_settings',
        'sekizai.context_processors.sekizai',
    )

    if django.VERSION < (1, 7):
        INSTALLED_APPS += [
            'south',
        ]

    app_manage.main(
        ['aldryn_newsblog', ],
        INSTALLED_APPS=INSTALLED_APPS,
        DATABASES=app_manage.DatabaseConfig(
            env='DATABASE_URL',
            arg='--db-url',
            default='sqlite://localhost/local.sqlite'
        ),
        SOUTH_MIGRATION_MODULES={
            'aldryn_newsblog': 'aldryn_newsblog.south_migrations',
        },
        MIGRATION_MODULES = {
            'filer': 'filer.migrations_django',
        },
        TEMPLATE_CONTEXT_PROCESSORS=TEMPLATE_CONTEXT_PROCESSORS,
        ROOT_URLCONF='manage',
        SITE_ID=1,
        STATIC_ROOT=app_manage.TempDir(),
        MEDIA_ROOT=app_manage.TempDir(),
    )
