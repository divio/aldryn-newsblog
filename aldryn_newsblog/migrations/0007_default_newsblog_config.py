# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import apps as django_apps
from django.conf import settings
from django.db import models, migrations, transaction
from django.db.utils import ProgrammingError, OperationalError


def noop(apps, schema_editor):
    pass


def get_config_count_count(model_class):
    with transaction.atomic():
        count = model_class.objects.count()
    return count


def create_default_newsblog_config(apps, schema_editor):
    import cms.models.fields
    from cms.models import Placeholder
    NewsBlogConfig = apps.get_model('aldryn_newsblog', 'NewsBlogConfig')

    # if we try to execute this migration after cms migrations were migrated
    # to latest - we would get an exception because apps.get_model
    # contains cms models in the last known state (which is the dependency
    # migration state). If that is the case we need to import the real model.
    try:
        # to avoid the following error:
        #   django.db.utils.InternalError: current transaction is aborted,
        #   commands ignored until end of transaction block
        # we need to cleanup or avoid that by making transaction atomic.
        count = get_config_count_count(NewsBlogConfig)
    except (ProgrammingError, OperationalError):
        NewsBlogConfig = django_apps.get_model('aldryn_newsblog.NewsBlogConfig')
        count = get_config_count_count(NewsBlogConfig)

    if not count == 0:
        return
    # create only if there is no configs because user may already have
    # existing and configured config.
    app_config = NewsBlogConfig(namespace='aldryn_newsblog_default')
    # usually generated in aldryn_apphooks_config.models.AppHookConfig
    # but in migrations we don't have real class with correct parents.
    app_config.type = 'aldryn_newsblog.cms_appconfig.NewsBlogConfig'
    # placeholders
    # cms checks if instance.pk is set, and if it isn't cms creates a new
    # placeholder but it does that with real models, and fields on instance
    # are faked models. To prevent that we need to manually set instance pk.
    app_config.pk = 1

    for field in app_config._meta.fields:
        if not field.__class__ == cms.models.fields.PlaceholderField:
            # skip other fields.
            continue
        placeholder_name = field.name
        placeholder_id_name = '{0}_id'.format(placeholder_name)
        placeholder_id = getattr(app_config, placeholder_id_name, None)
        if placeholder_id is not None:
            # do not process if it has a reference to placeholder field.
            continue
        # since there is no placeholder - create it, we cannot use
        # get_or_create because it can get placeholder from other config
        new_placeholder = Placeholder.objects.create(
            slot=placeholder_name)
        setattr(app_config, placeholder_id_name, new_placeholder.pk)
    # after we process all placeholder fields - save config,
    # so that django can pick up them.
    app_config.save()

    # translations
    app_config_translation = app_config.translations.create()
    app_config_translation.language_code = settings.LANGUAGES[0][0]
    app_config_translation.app_title = 'News & Blog'
    app_config_translation.save()


class Migration(migrations.Migration):

    dependencies = [
        ('cms', '0003_auto_20140926_2347'),
        ('aldryn_newsblog', '0006_auto_20160105_1013'),
    ]

    operations = [
        migrations.RunPython(create_default_newsblog_config, noop)
    ]
