############
Installation
############

If you're installing into an existing django CMS project, you can run either::

    pip install aldryn-newsblog

or::

    pip install -e git+https://github.com/aldryn/aldryn-newsblog.git#egg=aldryn-newsblog

If you need to start a new project, we recommend that first you use the `django CMS Installer
<http://djangocms-installer.readthedocs.org>`_ to create it, and then install
Aldryn News & Blog on top of that.

In your project's ``settings.py`` make sure you have all of::

    'parler',
    'hvad',
    'filer',
    'aldryn_people',
    'aldryn_categories',
    'taggit',
    'aldryn_newsblog',

listed in ``INSTALLED_APPS``, *after* ``'cms'``.

Now run ``python manage.py migrate`` if you have not already done so, foloowed by ``python
manage.py migrate`` to prepare the database for the new applications.
