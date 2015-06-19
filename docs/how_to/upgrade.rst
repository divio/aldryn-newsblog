#########
Upgrading
#########

The `CHANGELOG <https://github.com/aldryn/aldryn-newsblog/blob/master/CHANGELOG.rst>`_
is maintained and updated within the repository.


******************
Upgrade from 0.5.0
******************

.. note::

    If you're upgrading from a version earlier than 0.5.0.

In this version 0.5.0, we're deprecating all of the static placeholders and
instead making them PlaceholderFields on the app_config object. This means
that you'll be able to have content that is different in each instance of
the app, which was originally intended.

Because some may have already used these static placeholders, there will be
a (very) short deprecation cycle. 0.5.0 will introduce the new
PlaceholderFields whilst leaving the existing static placeholders intact.
This will allow developers and content managers to move plugins from the old
to the new.

Version 0.6.0 will remove the old static placeholders to avoid any further
confusion.

**Also note:** The article's PlaceholderField has also had its visible name
updated. The old name will continue to be displayed in structure mode until
the article is saved. Similarly, the new app_config-based PlaceholderFields
will not actually appear in structure mode until the app_config is saved
again.
