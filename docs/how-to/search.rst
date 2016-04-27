.. _search:

##########################################
Search functionality
##########################################

****************************
Default search functionality
****************************

By default, the :ref:`article_search_plugin` plugin searches through articles' *Title* and
*Lead-in* fields. To have it search through the main content of articles, you need to add a
setting::

    ALDRYN_NEWSBLOG_UPDATE_SEARCH_DATA_ON_SAVE = True

When this is enabled, when articles and plugins are saved they will render their content and save it to the database.
This rendered content will be added to the search corpus.


Rebuilding the search corpus
============================

Enabling ``ALDRYN_NEWSBLOG_UPDATE_SEARCH_DATA_ON_SAVE`` will not automatically add the rendered
content of previously-saved articles.

To have them added, you will need to run a management command, ``rebuild_article_search_data`` -
i.e.

    python manage.py rebuild_article_search_data

The command optionally takes ``--language`` or the short-hand ``-l`` to specify the translations to
process, for example::

    python manage.py rebuild_article_search_data -l en de

If this option is not provided, all languages will be processed.


**************************
Aldryn Search and Haystack
**************************

Aldryn News & Blog supports `Aldryn Search <https://github.com/aldryn/aldryn-search>`_ and `Django
Haystack <http://django-haystack.readthedocs.org>`_.

If you have Aldryn Search and Haystack installed and configured in your project, News & Blog's
content can also be rendered searchable. To enable this, add::

    ALDRYN_NEWSBLOG_SEARCH = True

in your settings. Note that if your search infrastructure is not configured, this setting will have
no effect.


.. _per_apphook_indexing:

Per-apphook indexing
====================

If you have configured your system for Aldryn Search and Haystack support and have enabled it for
Aldryn News & Blog, you can control it on a per-apphook basis. That is, you can turn it on or off
for the articles belonging to a particular apphook, using the *Include in search index?* setting of
the apphook configuration.

This *doesn't* affect the default search mechanism - only the Haystack-based search.
