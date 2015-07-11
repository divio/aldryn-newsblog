# -*- coding: utf-8 -*-
from optparse import make_option

from django.conf import settings
from django.core.management.base import BaseCommand

from parler.utils.context import switch_language

from aldryn_newsblog.models import Article


class Command(BaseCommand):
    can_import_settings = True

    base_options = (
        make_option(
            "-l",
            "--language",
            action="append",
            dest="languages",
            default=None,
        ),
    )
    option_list = BaseCommand.option_list + base_options

    def handle(self, *args, **options):
        languages = options.get('languages')

        if languages is None:
            languages = [language[0] for language in settings.LANGUAGES]

        # ArticleTranslation
        translation_model = Article._parler_meta.root_model

        for article in Article.objects.published():
            translations = article.translations.filter(
                language_code__in=languages
            )

            # build internal parler cache
            parler_cache = dict(
                (trans.language_code, trans) for trans in translations)

            # set internal parler cache
            # to avoid parler hitting db for every language
            article._translations_cache[translation_model] = parler_cache

            for translation in translations:
                language = translation.language_code

                with switch_language(article, language_code=language):
                    translation.search_data = article.get_search_data()
                    # make sure to only update the search_data field
                    translation.save(update_fields=["search_data"])
