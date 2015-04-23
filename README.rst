|PyPI Version| |Build Status| |Coverage Status|

===============
Aldryn Newsblog
===============

NOTICE: ::

    *FROM VERSION 1.0.0, ALDRYN_NEWSBLOG WILL REQUIRE CMS 3.0 OR LATER*

    If you intend to migration from a 2.x project, please make sure you first
    upgrade your project to the latest CMS 3.0.x, run all South migrations,
    then, you can upgrade to futher CMS releases (3.1.x, etc.)

NOTICE: ::

    *IF YOU'RE UPGRADING FROM A VERSION EARLIER THAN 0.5.0, PLEASE READ THIS.*

    In this version 0.5.0, we're deprecating all of the static placeholders and
    instead making them PlaceholderFields on the app_config object. This means
    that you'll be able to have content that is different in each instance of
    the app, which was originally intended.

    Because some may have already used these static placeholders, there will be
    a (very) short deprecation cycle. 0.5.0 will introduce the new
    PlaceholderFields whilst leaving the existing static placeholders intact.
    This will allow developers and content managers to move plugins from the old
    to the new.

    Version 0.6.0 will remove the old static placeholders to avoid any further
    confusion.

    ALSO NOTE: The article's PlaceholderField has also had its visible name
    updated. The old name will continue to be displayed in structure mode until
    the article is saved. Similarly, the new app_config-based PlaceholderFields
    will not actually appear in structure mode until the app_config is saved
    again.

Description
~~~~~~~~~~~

A combined news/weblog application for Aldryn and django CMS.

Aldryn NewsBlog is intended to serve as a model of good practice for development
of django CMS and Aldryn applications.


--------------------
Installation & Usage
--------------------

django CMS Requirements
~~~~~~~~~~~~~~~~~~~~~~~

This project requires django CMS 3.0.12 or later.


Aldryn Platform Users
~~~~~~~~~~~~~~~~~~~~~

1) Choose a site you want to install the add-on to from the dashboard.

2) Go to **Apps** > **Install App**

3) Click **Install** next to the **NewsBlog** app.

4) Redeploy the site.


Manual Installation
~~~~~~~~~~~~~~~~~~~

1) Run `pip install aldryn-newsblog`. Also note that a number of other packages
   may need to be installed if they are not already: ::

      aldryn-apphooks-config
      aldryn-boilerplates
      aldryn-categories
      aldryn-people
      aldryn-reversion
      djangocms-text-ckeditor
      easy_thumbnails
      django-filer
      django-parler
      django-reversion
      django-taggit

2) Add below apps to ``INSTALLED_APPS``: ::

    INSTALLED_APPS = [
        …
        'aldryn_apphooks_config',
        'aldryn_boilerplates',
        'aldryn_categories',
        'aldryn_newsblog',
        'aldryn_people',
        'aldryn_reversion',
        'djangocms_text_ckeditor',
        'easy_thumbnails',
        'filer',
        'parler',
        'reversion',
        'sortedm2m',
        'taggit',
        …
    ]

   Please see notes regarding `Django CMS Requirements`_ and `Django Appdata`_
   below, however.

3) Configure ``aldryn-boilerplates`` (https://pypi.python.org/pypi/aldryn-boilerplates/).

   To use the old templates, set ``ALDRYN_BOILERPLATE_NAME='legacy'``.
   To use https://github.com/aldryn/aldryn-boilerplate-standard (recommended, will be renamed to
   ``aldryn-boilerplate-bootstrap3``) set ``ALDRYN_BOILERPLATE_NAME='bootstrap3'``.

4) Run migrations: ``python manage.py migrate aldryn_newsblog``.

   NOTE: aldryn_newsblog supports both South and Django 1.7 migrations. If using
   Django 1.7, you may need to add the following to your settings: ::

    MIGRATION_MODULES = {
       …
       # The following are for some of the dependencies.
       'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
       'filer': 'filer.migrations_django',
       …
    }

4) Add Required Easy Thumbnail setting

   aldryn-newsblog requires the use of the optional "subject location" processor
   from Django Filer for Easy Thumbnails. This requires setting the
   THUMBNAIL_PROCESSORS tuple in your project's settings and explicitly omitting
   the default processor ``scale_and_crop`` and including the optional
   ``scale_and_crop_with_subject_location`` processor. For example: ::

    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        # 'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
    )

   For more information on this optional processor, see the `documentation for Django Filer`__.

__ http://django-filer.readthedocs.org/en/latest/installation.html#subject-location-aware-cropping

5) (Re-)Start your application server.


Settings
~~~~~~~~

The flag `ALDRYN_NEWSBLOG_SEARCH` can be set to `False` in settings if indexing
should be globally disabled for NewsBlog. When this is `False`, it overrides
the setting in the application configuration on each apphook.

If aldryn-search, Haystack, et al, are not installed, this setting does nothing.


-----
Notes
-----

Related Articles Plugin
~~~~~~~~~~~~~~~~~~~~~~~

The Related Articles plugin is only appropriate for use only on the article
detail view. If the plugin in placed on any other page, it will render an empty
<DIV></DIV>.


Known Issues
~~~~~~~~~~~~

Due to the way existing versions of Django work, after creating a new app-hook,
django CMS requires that the server is restarted. This is a long-standing issue.
For more information, see the `documentation for django CMS`__.

__ https://django-cms.readthedocs.org/en/support-3.0.x/how_to/apphooks.html#apphooks


.. |PyPI Version| image:: http://img.shields.io/pypi/v/aldryn-newsblog.svg
   :target: https://pypi.python.org/pypi/aldryn-newsblog
.. |Build Status| image:: http://img.shields.io/travis/aldryn/aldryn-newsblog/master.svg
   :target: https://travis-ci.org/aldryn/aldryn-newsblog
.. |Coverage Status| image:: http://img.shields.io/coveralls/aldryn/aldryn-newsblog/master.svg
   :target: https://coveralls.io/r/aldryn/aldryn-newsblog?branch=master
