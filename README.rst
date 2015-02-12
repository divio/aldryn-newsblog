|PyPI Version| |Build Status| |Coverage Status|

Aldryn Newsblog
===============


Description
~~~~~~~~~~~

A combined news/weblog application for Aldryn and django CMS.

Aldryn NewsBlog is intended to serve as a model of good practice for development
of django CMS and Aldryn applications.


Installation & Usage
--------------------


Aldryn Platform Users
~~~~~~~~~~~~~~~~~~~~~

1) Choose a site you want to install the add-on to from the dashboard.

2) Go to **Apps** > **Install App**

3) Click **Install** next to the **NewsBlog** app.

4) Redeploy the site.


Manual Installation
~~~~~~~~~~~~~~~~~~~

1) Run `pip install aldryn-newsblog`.

2) Add below apps to ``INSTALLED_APPS``: ::

    INSTALLED_APPS = [
        …
        'aldryn_categories',
        'aldryn_people',
        'djangocms_text_ckeditor',
        'easy_thumbnails',
        'filer',
        'parler',
        'reversion',
        'taggit',
        …
    ]

   Please see notes regarding `Django CMS Requirements`_ and `Django Appdata`_
   below, however.

3) Run migrations: ``python manage.py migrate aldryn_newsblog``.

   NOTE: aldryn_newsblog supports both South and Django 1.7 migrations. If using
   Django 1.7, you may need to add the following to your settings: ::

    MIGRATION_MODULES = [
       …
       'aldryn_newsblog': 'aldryn_newsblog.south_migrations',
       # The following are for some of the depenencies.
       'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',
       'filer': 'filer.migrations_django',
       …
    ]

4) (Re-)Start your application server.

Available settings
------------------

 * ``ALDRYN_NEWSBLOG_CREATE_AUTHOR`` - if set to ``False``, no author (Person
   object) would be implicitly created. Default value: ``True``.

Notes
-----

Django 1.7
~~~~~~~~~~

At time of this writing, due to circumstances beyond our control, we are unable
to support both django-taggit and django-sortedm2m in the same Django 1.7
environment. As both of these projects are dependences, this application is not
yet compatible with Django 1.7. We expect this to be resolved very soon.


Django CMS Requirements
~~~~~~~~~~~~~~~~~~~~~~~

At time of this writing, released versions of `django CMS`__ do not have the
required support for aldryn_apphook_config. This should be available in a near-
future release (v3.1.0 or earlier).

__ https://github.com/divio/django-cms

In the meantime, `this special branch`__ based on 3.0.9 does have the required
support.

__ https://github.com/yakky/django-cms/archive/feature/appspaced_apphooks.zip


Django Appdata
~~~~~~~~~~~~~~

At the time of this writing, the very latest version of django-appdata, a
requirement of aldryn-app-config is not yet available in PyPI but is required
under Django 1.7. Consider installing `the most recent version`__ with: ::

    pip install https://github.com/ella/django-appdata/archive/master.zip

__ https://github.com/ella/django-appdata/archive/master.zip

.. |PyPI Version| image:: http://img.shields.io/pypi/v/aldryn-newsblog.svg
   :target: https://pypi.python.org/pypi/aldryn-newsblog
.. |Build Status| image:: http://img.shields.io/travis/aldryn/aldryn-newsblog/master.svg
   :target: https://travis-ci.org/aldryn/aldryn-newsblog
.. |Coverage Status| image:: http://img.shields.io/coveralls/aldryn/aldryn-newsblog/master.svg
   :target: https://coveralls.io/r/aldryn/aldryn-newsblog?branch=master
