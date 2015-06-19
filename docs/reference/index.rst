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


*******
Plugins
*******


Related Articles Plugin
=======================

The Related Articles plugin is only appropriate for use only on the article
detail view. If the plugin in placed on any other page, it will render an empty
``<div></div>``.
