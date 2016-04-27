.. _plugins:

###################################
Using plugins
###################################

Aldryn News & Blog comes with a set of useful plugins. They are mostly self-explanatory.


********************
Where to use plugins
********************

Though you can add any of these plugins to any placeholder or static placeholder, some really make
only sense in particular contexts (and some will simply do nothing at all in a context where they
don't make sense).

For example, the :ref:`related_articles` plugin only makes sense when attached to an article. Dropped into a django CMS page for example, it will do nothing.

On the other hand, it would be possible but probably not very desirable to have a list of *Recent
articles* appear in the template of an article.


********************
List of plugins
********************

Most of the plugins produce output specific to a particular apphook configuration. In these the
*Application configuration* is a required field.


In alphabetical order:

Archive
=======

.. image:: /images/news-archive.png
   :alt: archive plugin output
   :align: right
   :width: 171

*Archive* creates a list of dates representing published articles.

Selecting a date takes you a sub-page in the archive, with a paginated list of articles for that
date.


.. _article_search_plugin:

Article search
==============

*Article search* provides a search field. The search mechanism will search through article *Titles*
and *Lead-in* fields, but not other content.


.. _authors:

Authors
=======

.. image:: /images/authors.png
   :alt: a list of authors
   :align: right
   :width: 171

*Authors* creates a list of authors who have published articles.

Selecting an author takes you a sub-page in the archive, with a paginated list of articles for that
author.


.. _categories:

Categories
==========

*Categories* creates a list of categories articles have been placed in.

Selecting a category takes you a sub-page in the archive, with a paginated list of articles for that
category.


.. _featured_articles:

Featured articles
=================

*Featured articles* creates a list of articles that have been marked as *Featured*. Their display
can be styled with CSS to achieve the effect you require - see :ref:`customising_news_output` for an
example.


Latest articles
===============

*Latest articles* creates a list of the most recent articles.


.. _related_articles:

Related articles
================

*Related articles* creates a list of the most recent articles.


Tags
====

.. image:: /images/tags.png
   :alt: a list of tags
   :align: right
   :width: 171

*Tags* displays a list of tags associated with articles.
