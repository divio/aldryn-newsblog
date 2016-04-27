.. raw:: html

    <style>
        .row {clear: both}
        .row h2  {border-bottom: 1px solid black;}

        .column img {border: 1px solid black;}

        @media only screen and (min-width: 1000px),
               only screen and (min-width: 500px) and (max-width: 768px){

            .column {
                padding-left: 5px;
                padding-right: 5px;
                float: left;
            }

            .column3  {
                width: 33.3%;
            }

            .column2  {
                width: 50%;
            }
        }
    </style>


##################
Aldryn News & Blog
##################

********
Overview
********

Aldryn News & Blog is an `Aldryn <http://aldryn.com>`_-compatible news and weblog application for
`django CMS <http://django-cms.org>`_.

.. rst-class:: clearfix row

.. rst-class:: column column2

:ref:`Get started <introduction>`
=================================

Get started - installation and basic configuration

.. rst-class:: column column2

:ref:`How to <how_to>`
=======================

Publishing news and weblog articles with News & Blog


.. rst-class:: clearfix row


***************
Features
***************

* guaranteed support and development - Aldryn News & Blog is a key application in the django
  CMS/Aldryn ecosystem, and is backed by commercial support
* one-click installation on the Aldryn platform
* multi-lingual by default
* supports advanced frontend frameworks through its compatibility with Aldryn Boilerplates


*************
Release Notes
*************

This document refers to version |release|.

See the `changelog <https://github.com/aldryn/aldryn-newsblog/blob/master/CHANGELOG.rst>`_ for
details of updates.

:ref:`upgrading` contains some information on how to upgrade from earlier versions.


#############
Documentation
#############


.. toctree::
   :maxdepth: 2

   introduction
   how-to/index
   contributing
   upgrade
