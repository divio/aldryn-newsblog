.. _introduction:

#######################
Installation and set-up
#######################

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


Install the package using pip
=============================

If you're installing into an existing django CMS project, you can run either::

    pip install aldryn-newsblog

or::

    pip install -e git+https://github.com/aldryn/aldryn-newsblog.git#egg=aldryn-newsblog

If you need to start a new project, we recommend that first you use `the instructions in the official
django CMS documentation
<http://docs.django-cms.org/en/latest/introduction/install.html#use-the-django-cms-installer>`_, which
will get you started in less than five minutes.

Once you have created a django CMS project, you can install Aldryn News & Blog in it.


settings.py
===========

In your project's ``settings.py`` make sure you have all of::

    # you will probably need to add these
    'aldryn_apphooks_config',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'aldryn_translation_tools',
    'parler',
    'sortedm2m',
    'taggit',

    # you'll almost certainly have these installed already
    'djangocms_text_ckeditor',
    'easy_thumbnails',
    'filer',

listed in ``INSTALLED_APPS``, *after* ``'cms'``.


Additional Configuration
========================

.. _aldryn_boilerplate_support:

Aldryn Boilerplate support
--------------------------

Aldryn News & Blog supports `Aldryn Boilerplates
<https://github.com/aldryn/aldryn-boilerplates/>`_, and has a set of templates that work with the
`Bootstrap 3 boilerplate
<http://aldryn-boilerplate-bootstrap3.readthedocs.org/en/latest/index.html>`_.

Boilerplates provide a convenient way to build optional support for advanced frontend frameworks
into Django applications. If the project in which the application is deployed uses a Boilerplate
supported by the application, the application will take advantage of it automatically, and
integrate seamlessly into the site's frontend.

If not, the application will fall back gracefully to more basic templates, or the developer
can readily add the appropriate Boilerplate support for the application.

If your site uses a boilerplate, you'll need to make some changes to your ``settings.py``:

* add ``aldryn_boilerplates`` to ``INSTALLED_APPS``

* set ``ALDRYN_BOILERPLATE_NAME`` - for example: ``ALDRYN_BOILERPLATE_NAME = 'bootstrap3'``


Django Filer
------------

Aldryn News & Blog *requires* the use of the "subject location" processor from Django Filer for
Easy Thumbnails. This requires setting the ``THUMBNAIL_PROCESSORS`` tuple in your project's
settings to:

* omit the default processor ``scale_and_crop``
* include the ``scale_and_crop_with_subject_location`` processor

For example::

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


*******************
Database migrations
*******************

Aldryn News & Blog includes new models that require database migrations. Run ``python manage.py
syncdb`` if you have not already done so, followed by ``python manage.py migrate`` to prepare the
database for the new applications.

.. note::

    Aldryn News & Blog supports both South and Django migrations.


.. _django-cms-setup:

*****************
django CMS set-up
*****************

In order to use Aldryn News & Blog, your django CMS project needs to have at least one page set up
with an Aldryn News & Blog `apphook <http://docs.django-cms.org/en/develop/how_to/apphooks.html>`_.

To do this:

#. Create a django CMS page in the normal way.
#. In *Advanced settings...* > *Application* settings, select *NewsBlog*.

You're now ready to begin using Aldryn News & Blog in earnest - see :ref:`basic_usage` for the next steps.
