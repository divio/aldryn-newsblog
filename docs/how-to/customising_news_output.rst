.. _customising_news_output:

#############################
Customising news output
#############################

By default, a News & Blog page will simply list items, using the ``article_list.html`` template,
while an article will use the ``article_detail`` page.

At its most basic, all the ``article_list.html`` template does is `extend a base template and add
the article list
<https://github.com/aldryn/aldryn-newsblog/blob/master/aldryn_newsblog/templates/aldryn_newsblog/article_list.html>`_. Similarly, the ``article_detail`` will extend a base template.

It's easy to override these templates to add your own components to your News & Blog pages. If you
add static placeholders to the templates, then you will be able to add arbitrary plugins to it;
these will then appear on all the News & Blog pages that use those templates.


*******************************
Customising a news section page
*******************************

The simplest news section page (the django CMS page that has a News & Blog apphook attached to it)
is a list of articles.

The optional Aldryn Bootstrap Boilerplate templates, which will be used if you are using the Aldryn
Boilerplate Bootstrap 3 components - see :ref:`aldryn_boilerplate_support` - offer something more
sophisticated.

In that case, the `article list template
<https://github.com/aldryn/aldryn-newsblog/blob/master/aldryn_newsblog/boilerplates/bootstrap3/templ
ates/aldryn_newsblog/article_list.html>`_ will extend `a more complex
template
<https://github.com/aldryn/aldryn-newsblog/blob/master/aldryn_newsblog/boilerplates/bootstrap3/templ
ates/aldryn_newsblog/two_column.html>`_, that implements some static placeholders.

.. image:: /images/news-page-example.jpg
   :alt: a custom news page example layout
   :align: right
   :width: 348

It makes possible the layout represented here, which was taken from the `Divio website
<http://divio.com/blog>`_. It's worth describing how it's implemented, to show some of the
possibilities.

The page has a static_placeholder ``newsblog_feature``. Into this are placed:

#. a heading, *Featured articles*
#. a :ref:`featured_articles` plugin, set to display the latest three articles on which the
   "featured" flag has been set
#. a heading, *Recent articles*

Below the ``newsblog_feature`` static placeholder, the ``article_list.html`` template
simply lists the articles (4).

On the right are the items from the ``newsblog_sidebar``. These are:

5. a :ref:`categories` plugin, that lists the different categories of article that have been
   published
6. an :ref:`authors` plugin, that lists different authors of published articles

See :ref:`plugins` for more details of the different plugins available.


*******************************************
Customising News & Blog article templates
*******************************************

Articles can be similarly customised. For example you might add a *Related articles* plugin to the
static placeholder of your articles, so that each article will display a list of related articles.


************************
Section-specific content
************************

If you have multiple news sections, you can also have :ref:`section_secific_content`, by using
*apphook-configuration-aware* placeholder template tags as described in
:ref:`section_secific_content`.

