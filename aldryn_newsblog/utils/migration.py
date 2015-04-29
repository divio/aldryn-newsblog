# -*- coding: utf-8 -*-

from __future__ import unicode_literals


#
# If new plugins are added, they should be added to this list.
#
default_cms_plugin_table_mapping = (
    # (old_name, new_name),
    ('cmsplugin_newsblogarchiveplugin',
        'aldryn_newsblog_newsblogarchiveplugin'),
    ('cmsplugin_newsblogarticlesearchplugin',
        'aldryn_newsblog_newsblogarticlesearchplugin'),
    ('cmsplugin_newsblogauthorsplugin',
        'aldryn_newsblog_newsblogauthorsplugin'),
    ('cmsplugin_newsblogcategoriesplugin',
        'aldryn_newsblog_newsblogcategoriesplugin'),
    ('cmsplugin_newsblogfeaturedarticlesplugin',
        'aldryn_newsblog_newsblogfeaturedarticlesplugin'),
    ('cmsplugin_newsbloglatestarticlesplugin',
        'aldryn_newsblog_newsbloglatestarticlesplugin'),
    ('cmsplugin_newsblogrelatedplugin',
        'aldryn_newsblog_newsblogrelatedplugin'),
    ('cmsplugin_newsblogtagsplugin', 'aldryn_newsblog_newsblogtagsplugin'),
)


def rename_tables(db, table_mapping=None, reverse=False):
    """
    renames tables from source to destination name, if the source exists and the
    destination does not exist yet.

    taken from cmsplugin-filer:cmsplugin_filer_utils.migration
    (thanks to @stefanfoulis)
    """
    from django.db import connection

    if not table_mapping:
        table_mapping = default_cms_plugin_table_mapping

    if reverse:
        table_mapping = [(dst, src) for src, dst in table_mapping]
    table_names = connection.introspection.table_names()
    for source, destination in table_mapping:
        if source in table_names and destination in table_names:
            print("    WARNING: not renaming {0} to {1}, because both tables "
                  "already exist.".format(source, destination))
        elif source in table_names and destination not in table_names:
            print("     - renaming {0} to {1}".format(source, destination))
            db.rename_table(source, destination)


def rename_tables_old_to_new(db, table_mapping=None):
    return rename_tables(db, table_mapping, reverse=False)


def rename_tables_new_to_old(db, table_mapping=None):
    return rename_tables(db, table_mapping, reverse=True)
