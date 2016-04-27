.. _multiple_news_sections:

#############################
Multiple news/weblog sections
#############################

Your project can host multiple independent news/weblog sections, each with their own items. For
example, a company website might have a news section for publishing press releases, and a weblog for
publishing more informal articles.

To do this, you need to create a django CMS page for each news/weblog section, and add an apphook
for Aldryn News & Blog to each of them. You will also need to create a separate apphook
configuration for each of them - apphook configurations cannot be shared between apphook instances.

.. note:

    Creating a new News & Blog section on your site implies setting up a new apphook instance.
    The apphook instance however doesn't actually do anything until a page has been set up with it.


**********************************
Creating a new News & Blog section
**********************************

The quickest way to do this is:

* Create the new page.
* In its *Advanced settings*, choose *Newsblog* in the *Application* field. A new field,
  *Application configurations*, will appear immediately below it.
* Add a new application configuration, by selecting the **+** icon.


Fields
======

*Instance namespace* - a unique (and slug-like) name for this configuration. Note that this cannot be subsequently
changed.

*Application title* - A human-readable name for the configuration, that helps explain its purpose
to the users of the system. For example, if this news section will publish press releases, call it
*Press releases*. The name will be reflected in the django CMS toolbar when you're on that page.

*Permalink type* - the format of canonical URLs for articles in this section.

*Non-permalink-handling* - For convenience, the system can optionally resolve URLs that are not in
the canonical format. For example, if the canonical URL is ``2016/11/27/man-bites-dog``, the URL
``man-bites-dog`` can redirect to it. This behaviour is the default, but optional.

*Prefix for template directories* - If you'd like this news section to use custom templates, create
a set in a new directory. So for example, instead of using the default
``aldryn_newsblog/article_list.html``, it will look for
``aldryn_newsblog/custom-directory/article_list.html``.

*Include in search index* - see :ref:`per_apphook_indexing`.

Other fields are self-explanatory.

Apphook configurations can also be created and edited in other ways:

* from the Django Admin, in *Aldryn News & Blog* > *Application configuration*
* from the option *Configure addon...* in the apphook's menu in the django CMS toolbar


***********************************
Access to application configuration
***********************************

Typically, you will not provide most content editors of your site with admin permissions to manage
apphooks - this should be reserved for site managers.


**************************************************
Creating content in a specific News & Blog section
**************************************************

Articles
========

The section that a particular article is attached to is set in its *Application Configuration*
field, in its *Advanced settings*. This can be changed once an article has been created, thus
moving it from one section of a site to another.

.. _section_secific_content:

Section-specific shared content
===============================

In :ref:`shared_content`, we noted that you can use *Static placeholders* in your article templates
``article_detail.html``, so that all articles can incorporate some boilerplate content (a typical
example would be a list of social media links)::

    {% static_placeholder "newsblog_social" %}

Sometimes this is all you need, but if you are maintaining multiple News & Blog sections, you might
not want *site-wide* shared content of this kind, but only *section-specific* shared content. For
example, you might require one set of social media links for news pages aimed at your customers and
another for pages aimed at your investors.

In this case, you will need to override the default templates, which you can do at project level.
You can remove the default ``{% static_placeholder %}`` altogether if you wish, or you can simply
add new *apphook-configuration-aware* placeholder template tags where you need them. For example::

    {% render_placeholder view.config.placeholder_detail_bottom %}

Unlike static placeholder template tags, which can be added arbitrarily to your templates as you
need them, these are standard ``PlaceholderFields``, defined in the `NewsBlogConfig model
<https://github.com/aldryn/aldryn-newsblog/blob/master/aldryn_newsblog/cms_appconfig.py>`_.

Several are defined there ready for you to use if you need them, and you advised to use them rather
than amend that model to add your own (which will require forking the News & Blog code-base, and
creating your own migrations for them.)
