CHANGELOG
=========

0.9.6 (2015-05-31)
------------------

* Fixes search index bug
* Fixes testsuite issue with django-filer>=0.9.10
* Fixes bug with toolbar

0.9.5 (2015-05-21)
------------------

* Improves migration-ability
* improves support for some version of MySQL
* Improves auto-slugification process


0.9.4 (2015-04-26)
------------------

* Now requires v0.1.3+ of aldryn-common
* Now requires v0.5.2+ of aldryn-people
* Fixes a bad migration
* Tested to work in django CMS 3.0.x and 3.1.x
* Other minor refactoring


0.9.3 (2015-04-23)
------------------

* Fixes older South migration (0028) for CMS 3.1
* Add "magic" migrations to move from old-style CMS plugin table naming to new
  for users using older versions of CMS.
* Post a deprecation notice about supporting only CMS 3.0+ from version 1.0.0
  of Aldryn NewsBlog.


0.9.2 (2015-04-21)
------------------

* Pin parler to version 1.4, which is required by the latest migration.
* Reimplements a means of allowing users to use plugins and Articles before
  creating and publishing the corresponding apphook'ed page. This new method
  gives more flexibility to developers and template authors.


0.9.1
-----

Unreleased.


0.9.0 (2015-04-20)
------------------

* Adds breadcrump support by adding a CMSAttachMenu. NOTE: django CMS v3.0.14
  or v3.1 or later must be used to have working breadcrumbs.
* Adds support for swappable User models.
* Adds sitemaps support.
* Improves support of language fallbacks as defined in CMS_LANGUAGES
* Adds new app configuration option for setting a template prefix.
* Fix an error in search indexer that breaks indexing if an article has no
  search data
* Search indexer is using switch_language from parler
* Now requires aldryn-apphooks-config v0.2.4 or later

0.8.8 (2015-04-??)
------------------


0.8.7 (2015-04-??)
------------------


0.8.6 (2015-04-16)
------------------

* Use get_current_language from cms instead get_language from Django because Django bug #9340

0.7.5 (2015-04-16)
------------------

* Use get_current_language from cms instead get_language from Django because Django bug #9340

0.2.0 (2015-02-03)
------------------

* multi-boilerplate support
  new requirement: aldryn-boilerplates (needs configuration)
