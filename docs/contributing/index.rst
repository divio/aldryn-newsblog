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

Aldryn News & Blog uses `django CMS Helper
<https://github.com/nephila/djangocms-helper>`_ to run its test suite.

There's more than one way to do this, but here's one to help you get started::

    # create a virtual environment
    virtualenv test-aldryn-newsblog

    # activate it
    cd test-aldryn-newsblog/
    source bin/activate

    # get Aldryn News & Blog from GitHub
    git clone git@github.com:aldryn/aldryn-newsblog.git

    # downgrade pip to a version < 6
    pip install -U 'pip<6'

    # install the dependencies for testing
    pip install -Ur aldryn-newsblog/test_requirements.txt

    # run the test suite
    # note that you must be in the aldryn-newsblog directory when you do this,
    # otherwise you'll get "Template not found" errors
    cd aldryn-newsblog
    ./test


*************
Documentation
*************

You can run the documentation locally for testing:

#. navigate to the documentation ``cd /docs``
#. run ``make install`` to install requirements
#. run ``make run`` to run the server

Now you can open **http://localhost:8000** on your favourite browser and start
changing the rst files within ``docs/``.
