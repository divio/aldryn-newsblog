# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.conf import settings
from django.contrib.auth.models import AnonymousUser
from django.contrib.sites.models import Site
try:
    from django.contrib.sites.shortcuts import get_current_site
except ImportError:
    # Django 1.6
    from django.contrib.sites.models import get_current_site
from django.core.urlresolvers import reverse, NoReverseMatch
from django.db import models
from django.template import RequestContext
from django.test import RequestFactory
from django.utils import translation
try:
    from django.utils.encoding import force_unicode
except ImportError:
    from django.utils.encoding import force_text as force_unicode
from django.utils.html import strip_tags as _strip_tags
from django.utils.text import smart_split

from cms.utils.i18n import force_language, get_language_object

from lxml.html.clean import Cleaner as LxmlCleaner


def default_reverse(*args, **kwargs):
    """
    Acts just like django.core.urlresolvers.reverse() except that if the
    resolver raises a NoReverseMatch exception, then a default value will be
    returned instead. If no default value is provided, then the exception will
    be raised as normal.

    NOTE: Any exception that is not NoReverseMatch will always be raised as
    normal, even if a default is provided.
    """

    # We're explicitly NOT happy to just re-raise the exception, as that may
    # adversely affect stack traces.
    if 'default' not in kwargs:
        return reverse(*args, **kwargs)
    else:
        default = kwargs.pop('default', None)
        try:
            return reverse(*args, **kwargs)
        except NoReverseMatch:
            return default


def get_request(language=None):
    """
    Returns a Request instance populated with cms specific attributes.
    """
    request_factory = RequestFactory()
    request = request_factory.get("/")
    request.session = {}
    request.LANGUAGE_CODE = language or settings.LANGUAGE_CODE
    request.current_page = None
    request.user = AnonymousUser()
    return request


def strip_tags(value):
    """
    Returns the given HTML with all tags stripped.
    We use lxml to strip all js tags and then hand the result to django's
    strip tags.
    """
    # strip any new lines
    if value:
        value = value.strip()

    if value:
        partial_strip = LxmlCleaner().clean_html(value)
        value = _strip_tags(partial_strip)
    return value


def get_cleaned_bits(data):
    decoded = force_unicode(data)
    stripped = strip_tags(decoded)
    return smart_split(stripped)


def get_field_value(obj, name):
    """
    Given a model instance and a field name (or attribute),
    returns the value of the field or an empty string.
    """
    fields = name.split('__')

    name = fields[0]

    try:
        obj._meta.get_field(name)
    except (AttributeError, models.FieldDoesNotExist):
        # we catch attribute error because obj will not always be a model
        # specially when going through multiple relationships.
        value = getattr(obj, name, None) or ''
    else:
        value = getattr(obj, name)

    if len(fields) > 1:
        remaining = '__'.join(fields[1:])
        return get_field_value(value, remaining)
    return value


def get_plugin_index_data(base_plugin, request):
    text_bits = []

    instance, plugin_type = base_plugin.get_plugin_instance()

    if instance is None:
        # this is an empty plugin
        return text_bits

    search_fields = getattr(instance, 'search_fields', [])

    if hasattr(instance, 'search_fulltext'):
        # check if the plugin instance has search enabled
        search_contents = instance.search_fulltext
    elif hasattr(base_plugin, 'search_fulltext'):
        # now check in the base plugin instance (CMSPlugin)
        search_contents = base_plugin.search_fulltext
    elif hasattr(plugin_type, 'search_fulltext'):
        # last check in the plugin class (CMSPluginBase)
        search_contents = plugin_type.search_fulltext
    else:
        # disabled if there's search fields defined,
        # otherwise it's enabled.
        search_contents = not bool(search_fields)

    if search_contents:
        plugin_contents = instance.render_plugin(
            context=RequestContext(request))

        if plugin_contents:
            text_bits = get_cleaned_bits(plugin_contents)
    else:
        values = (get_field_value(instance, field) for field in search_fields)

        for value in values:
            cleaned_bits = get_cleaned_bits(value or '')
            text_bits.extend(cleaned_bits)
    return text_bits


def add_prefix_to_path(path, prefix):
    splitted_path = path.split('/', 1)
    if len(splitted_path) == 1:
        # template is not in directory
        # template.html => prefix/template.html
        return "{0}/{1}".format(prefix, splitted_path[0])
    # directory/template.html => directory/prefix/template.html
    return "{0}/{1}/{2}".format(splitted_path[0], prefix, splitted_path[1])


def is_valid_namespace(namespace):
    """
    Check if provided namespace has an app-hooked page.
    Returns True or False.
    """
    try:
        reverse('{0}:article-list'.format(namespace))
    except NoReverseMatch:
        return False
    return True


def is_valid_namespace_for_language(namespace, language_code):
    """
    Check if provided namespace has an app-hooked page for given language_code.
    Returns True or False.
    """
    with force_language(language_code):
        return is_valid_namespace(namespace)


def get_valid_languages_from_request(namespace, request):
    language = translation.get_language_from_request(
        request, check_path=True)
    site_id = getattr(get_current_site(request), 'id', None)
    return get_valid_languages(
        namespace,
        language_code=language,
        site_id=site_id)


def get_valid_languages(namespace, language_code, site_id=None):
    langs = [language_code]
    if site_id is None:
        site_id = getattr(Site.objects.get_current(), 'pk', None)
    current_language = get_language_object(language_code, site_id)
    fallbacks = current_language.get('fallbacks', None)
    if fallbacks:
        langs += list(fallbacks)
    valid_translations = [
        lang_code for lang_code in langs
        if is_valid_namespace_for_language(namespace, lang_code)]
    return valid_translations
