############
Installation
############

You can install Aldryn News & Blog either on `Aldryn <http://www.aldryn.com>`_
or by hand into your own project.


*********************
Aldryn Platform Users
*********************

To install the addon on Aldryn, all you need to do is follow this
`installation link <https://control.aldryn.com/control/?select_project_for_addon=aldryn-newsblog>`_
on the Aldryn Marketplace and follow the instructions.

Manually you can:

#. Choose a site you want to install the add-on to from the dashboard.
#. Go to Apps > Install App
#. Click Install next to the News & Blog app.
#. Redeploy the site.


*******************
Manual Installation
*******************


Requirements
============

- This project requires **django CMS 3.0.12** or later.


PIP dependency
==============

If you're installing into an existing django CMS project, you can run either::

    pip install aldryn-newsblog

or::

    pip install -e git+https://github.com/aldryn/aldryn-newsblog.git#egg=aldryn-newsblog

If you need to start a new project, we recommend that first you use the
`django CMS Installer <http://djangocms-installer.readthedocs.org>`_ to create
it, and then install Aldryn News & Blog on top of that.


settings.py
===========

In your project's ``settings.py`` make sure you have all of::

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

listed in ``INSTALLED_APPS``, *after* ``'cms'``.


Additional Configuration
========================

.. important::

    To get Aldryn News & Blog to work you need to add additional configurations:


1. Aldryn-Boilerplates
----------------------

You need set additional configurations to ``settings.py`` for `Aldryn
Boilerplates  <https://github.com/aldryn/aldryn-boilerplates#configuration>`_.

To use the old templates, set ``ALDRYN_BOILERPLATE_NAME='legacy'``.
To use https://github.com/aldryn/aldryn-boilerplate-bootstrap3 (recommended)
``set ALDRYN_BOILERPLATE_NAME='bootstrap3'``.


2. Django-Filer
---------------

Aldryn News & Blog requires the use of the optional "subject location"
processor from Django Filer for Easy Thumbnails. This requires setting the
``THUMBNAIL_PROCESSORS`` tuple in your project's settings and explicitly
omitting the default processor ``scale_and_crop`` and including the optional
``scale_and_crop_with_subject_location`` processor. For example: ::

    THUMBNAIL_PROCESSORS = (
        'easy_thumbnails.processors.colorspace',
        'easy_thumbnails.processors.autocrop',
        # 'easy_thumbnails.processors.scale_and_crop',
        'filer.thumbnail_processors.scale_and_crop_with_subject_location',
        'easy_thumbnails.processors.filters',
        'easy_thumbnails.processors.background',
    )

For more information on this optional processor, see the
`documentation for Django Filer
<http://django-filer.readthedocs.org/en/latest/installation.html#subject-location-aware-cropping>`_.


Migrations
==========

Now run ``python manage.py migrate`` if you have not already done so,
foloowed by ``python manage.py migrate`` to prepare the database for the new applications.

Now run ``python manage.py migrate aldryn_newsblog``.

.. note::

    Aldryn News & Blog supports both South and Django 1.7 migrations.

If using Django 1.7, you may need to add the following to your settings: ::

    MIGRATION_MODULES = {
       ...
       # The following are for some of the dependencies.

       # Use this if you're using a version of djangocms_text_ckeditor < 2.5.1
       # 'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations_django',

       # Use this if you're using a version of Filer < 0.9.10
       # 'filer': 'filer.migrations_django',
       ...
    }


Server
======

To finish the setup, you need to create a page, change to the
*Advanced Settings* and choose *NewsBlog* within the *Application* drop-down.

You also need to set the *Application configurations* and
**publish the changes**.

Finally you just need to **restart your local development server** and you are
ready to go.

This process is described in more depth within :doc:`/how_to/basic_usage`.
