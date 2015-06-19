###########
Basic Usage
###########

Aldryn News & Blog works the way that many django-CMS-compatible applications
to. It expects you to create a new page for it in django CMS, and then attach
it to that page with an Apphook.


***************
Getting started
***************

#. if this is a new project, change the default *example.com* ``Site`` in the
   Admin to whatever is appropriate for your setup (typically, *localhost:8000*)
#. in Admin > Aldryn_Newsblog, create a new ``Apphook config`` with the value
   *aldryn_newsblog*
#. create a new django CMS page; this page will be associated with the
   Aldryn News & Blog application
#. open the new page's ``Advanced settings``
#. from the ``Application`` choices menu select *NewsBlog*
#. save the page
#. restart the runserver (necessary because of the new Apphook)

Now you have a new page to which the Aldryn NewsBlog will publish content.

Let's create a new weblog article, at Admin > Aldryn_NewsBlog. Fill in the
fields as appropriate - most are self-explanatory - and **Save**.

The page you created a moment ago should now list your new article.
