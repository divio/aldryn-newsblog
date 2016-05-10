.. _basic_usage:

###################################
Creating Aldryn News & Blog content
###################################

Before using Aldryn News & Blog, you need to :ref:`set up your django CMS project appropriately
<django-cms-setup>` (in short, making sure that you have a page with a News & Blog apphook - this
only takes a moment).

This page is where your articles will be listed (see :ref:`multiple_news_sections` for multiple
lists of articles).

There are various different ways to create a new article:

* From the django CMS toolbar, select **Create** then *New news/blog article*. This opens the
  django CMS content wizard, providing a quick way to add new content.

* If you're on a page with a News & Blog apphook, select *News & Blog* > *Add new article...* from
  the django CMS toolbar.

* Add a new article in the Django Admin, in the *Aldryn News & Blog* section.


******
Fields
******

Most of the fields for an article are self-explanatory, and they behave in logical ways. For
example, setting the *Publishing date* in the future will publish the item automatically at that
date/time.

Note that items will not be published until the *Is published* option has been explicitly set (and the *Publishing
date* has been reached).

A *Featured* item will be given prominence in lists, such as on the home page of the news section.


Meta Options
============

.. note:

    Fields in the *Meta Options* section should override the default article title, description
    (taken from the *Lead-in* field) and so on, **but are currently ignored**. This will be fixed
    in a later revision.


Advanced settings
==================

*Tags* are a set of optional free labels. Note that Tags, unlike most other fields, are not language-aware (i.e. the
same set of tags is available across all languages). See the `Taggit documentation
<https://django-taggit.readthedocs.io/en/latest/index.html>`_ for more.

*Categories* offer a more formal taxonomy, managed by the `Aldryn Categories
<http://aldryn-categories.readthedocs.org>`_ application.

*Application configuration* allows you to select which list (if you have multiple Application Configurations) of
news/weblog articles the article will be associated with.


************
Main content
************

Unless you used the *Content creation wizard* (the **Create** button) your new article will not
have any content other than the *Lead-in*.

The main content in an article is maintained in its *Newsblog Article Content* placeholder.

To add content:

* Select your (empty) article, for example from the News & Blog home page on your site.
* By default, you will be in *Content* mode. Select *Structure* from the django CMS Toolbar.
* Hit the **+** button to add a plugin to the *Newsblog Article Content* placeholder.
* Typically, this will be a *Text* plugin; add some text and **Save**.

When you switch back to *Content* mode, you'll see your full article.

.. _shared_content:

Shared content
==============

If you're using one of the default templates, you'll find that your article also contains another
placeholder, called *Newsblog Social*. This is a *Static placeholder* - it's shared between all
templates that contain it; in other words, between all News & Blog articles. If you add or change
plugins in that placeholder, *all* your Aldryn News & Blog articles will display them.

In this template, it's intended to be a convenient way for you to add social media links and buttons
to all your News & Blog articles.

See :ref:`section_secific_content` for more fine-grained control over content that's shared across
articles.
