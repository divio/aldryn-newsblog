|PyPI Version| |Build Status| |Coverage Status|

===============
Aldryn Newsblog
===============


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

This project requires django CMS 3.0.12.


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

      aldryn-categories
      aldryn-people
      aldryn-reversion
      djangocms-text-ckeditor
      easy_thumbnails
      django-filer
      django-parler
      django-reversion
      taggit

   IMPORTANT: As of this writing, you must install the latest, development
   version of django-appdata. ::

      pip install git+https://github.com/ella/django-appdata.git#egg=django_appdata

2) Add below apps to ``INSTALLED_APPS``: ::

    INSTALLED_APPS = [
        …
        'aldryn_categories',
        'aldryn_newsblog',
        'aldryn_people',
        'aldryn_reversion',
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
        # 'entercoms.apps.strategies.processors.reflect',
    )

   For more information on this optional processor, see the `documentation for Django Filer`__.

__ http://django-filer.readthedocs.org/en/latest/installation.html#subject-location-aware-cropping

5) (Re-)Start your application server.


------------------
Available settings
------------------

 * ``ALDRYN_NEWSBLOG_CREATE_AUTHOR`` - if set to ``False``, no author (Person
   object) would be implicitly created. Default value: ``True``.
 * ``ALDRYN_NEWSBLOG_PAGINATE_BY`` - the number of objects to show per page.
   Default value: ``10``.


-----
Notes
-----

Known Issues
~~~~~~~~~~~~

Due to the way existing versions of Django work, after creating a new app-hook,
django CMS requires that the server is restarted. This is a long-standing issue.
For more information, see the `documentation for django CMS`__.

__ https://django-cms.readthedocs.org/en/support-3.0.x/how_to/apphooks.html#apphooks


Django 1.7
~~~~~~~~~~

At time of this writing, due to circumstances beyond our control, we are unable
to support both django-taggit and django-sortedm2m in the same Django 1.7
environment. As both of these projects are dependences, this application is not
yet compatible with Django 1.7. We expect this to be resolved very soon.


Django Appdata
~~~~~~~~~~~~~~

At the time of this writing, the very latest version of django-appdata, a
requirement of aldryn-app-config is not yet available in PyPI but is required.
Consider installing the most recent version with: ::

    pip install git+https://github.com/ella/django-appdata.git#egg=django_appdata

.. |PyPI Version| image:: http://img.shields.io/pypi/v/aldryn-newsblog.svg
   :target: https://pypi.python.org/pypi/aldryn-newsblog
.. |Build Status| image:: http://img.shields.io/travis/aldryn/aldryn-newsblog/master.svg
   :target: https://travis-ci.org/aldryn/aldryn-newsblog
.. |Coverage Status| image:: http://img.shields.io/coveralls/aldryn/aldryn-newsblog/master.svg
   :target: https://coveralls.io/r/aldryn/aldryn-newsblog?branch=master
