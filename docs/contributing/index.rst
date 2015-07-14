#######################
Development & community
#######################

Aldryn News & Blog is an open-source project.

You don't need to be an expert developer to make a valuable contribution - all
you need is a little knowledge, and a willingness to follow the contribution
guidelines.


********
Divio AG
********

Aldryn News & Blog is developed by `Divio AG <https://divio.ch/>`_
and released under a BSD licence.

Aldryn News & Blog is compatible with Divio's `Aldryn <http://aldryn.com>`_
cloud-based `django CMS <http://django-cms.org>`_ hosting platform, and
therefore with any standard django CMS installation. The additional requirements
of an Aldryn application do not preclude its use with any other django CMS
deployment.

Divio is committed to Aldryn News & Blog as a high-quality application that
helps set standards for others in the Aldryn/django CMS ecosystem, and as a
healthy open source project.

Divio maintains overall control of the `Aldryn News & Blog repository
<https://github.com/aldryn/aldryn-newsblog>`_.


********************
Standards & policies
********************

Aldryn News & Blog is a django CMS application, and shares much of django CMS's
standards and policies.

These include:

* `guidelines and policies
  <http://docs.django-cms.org/en/support-3.0.x/contributing/contributing.html>`_
  for contributing to the project, including standards for code and
  documentation
* standards for `managing the project's development
  <http://docs.django-cms.org/en/support-3.0.x/contributing/management.html>`_
* a `code of conduct
  <http://docs.django-cms.org/en/support-3.0.x/contributing/code_of_conduct.html>`_
  for community activity

Please familiarise yourself with this documentation if you'd like to contribute
to Aldryn News & Blog.


*************
Running tests
*************

Aldryn News & Blog uses `django CMS Helper <https://github.com/nephila/djangocms-helper>`_ to run its
test suite.

Backend Tests
=============

To run the tests, in the aldryn-newsblog directory::

    virtualenv env  # create a virtual environment
    source env/bin/activate  # activate it
    python setup.py install  # install the package requirements
    pip install -r test_requirements/django-1.7.txt  # install the test requirements
    python test_settings.py  # run the tests

You can run the tests against a different version of Django by using the appropriate value in
``django-x.x.txt`` when installing the test requirements.


Frontend Tests
==============

Follow the instructions in the `aldryn-boilerplate-bootstrap3
<https://aldryn-boilerplate-bootstrap3.readthedocs.org/en/latest/testing/index.html>`_
documentation and setup the environment through the `Backend Tests` section.

Instead of using ``python test_settings.py`` described above, you need to excecute
``python test_settings.py server`` to get a running local server. You can open the
development server locally through ``http://127.0.0.1:8000/``. The database is added
within the root of this project ``local.sqlite``. You might want to delete the database
from time to time to start with a fresh installation. Don't forget to restart the
server if you do so.


*************
Documentation
*************

You can run the documentation locally for testing:

#. navigate to the documentation ``cd /docs``
#. run ``make install`` to install requirements
#. run ``make run`` to run the server

Now you can open **http://localhost:8000** on your favourite browser and start
changing the rst files within ``docs/``.
