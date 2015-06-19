#########
Upgrading
#########

Pleae mind the following upgrade notices:


******************
Upgrade from 1.0.0
******************

.. note::

    FROM VERSION 1.0.0, ALDRYN_NEWSBLOG WILL REQUIRE CMS 3.0 OR LATER

If you intend to migrate from a 2.x project, please make sure you first
upgrade your project to the latest CMS 3.0.x, run all South migrations,
then, you can upgrade to futher CMS releases (3.1.x, etc.)


******************
Upgrade from 1.0.0
******************

.. node::

    IF YOU'RE UPGRADING FROM A VERSION EARLIER THAN 0.5.0, PLEASE READ THIS.

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

ALSO NOTE: The article's PlaceholderField has also had its visible name
updated. The old name will continue to be displayed in structure mode until
the article is saved. Similarly, the new app_config-based PlaceholderFields
will not actually appear in structure mode until the app_config is saved
again.
