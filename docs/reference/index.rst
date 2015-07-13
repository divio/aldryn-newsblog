#########
Reference
#########


********
Settings
********

The flag ``ALDRYN_NEWSBLOG_SEARCH`` can be set to ``False`` in settings if
indexing should be globally disabled for Aldryn News & Blog. When this is
``False``, it overrides the setting in the application configuration on each
apphook.

If Aldryn Search, Haystack, et al, are not installed, this setting does nothing.

The flag ``ALDRYN_NEWSBLOG_UPDATE_SEARCH_DATA_ON_SAVE``, when set to True
(default value), updates the article's search_data field whenever the article
is saved or a plugin is saved on the article's content placeholder. Set to false
to disable this feature.


*******************
Management Commands
*******************

The management command: ``rebuild_article_search_data`` can be used to update
the search_data in all articles for searching. It can accept a switch
``--language`` or the short-hand ``-l`` to specify the translations to process.
If this switch is not provided, all translations are indexed by default.


*******
Plugins
*******


Related Articles Plugin
=======================

The Related Articles plugin is only appropriate for use only on the article
detail view. If the plugin in placed on any other page, it will render an empty
``<div></div>``.
