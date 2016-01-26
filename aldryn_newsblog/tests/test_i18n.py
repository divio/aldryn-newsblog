# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch
from django.utils.translation import override

from . import NewsBlogTestCase


class TestI18N(NewsBlogTestCase):

    def test_absolute_url_fallback(self):
        # Create an EN article
        with override('en'):
            article = self.create_article(
                title='God Save the Queen!', slug='god-save-queen')
        # Add a DE translation
        article.create_translation('de',
            title='Einigkeit und Recht und Freiheit!',
            slug='einigkeit-und-recht-und-freiheit')

        # Reload for good measure
        article = self.reload(article)

        self.assertEquals(article.get_absolute_url(language='en'),
            '/en/page/god-save-queen/')
        # Test that we can request the other defined language too
        self.assertEquals(article.get_absolute_url(language='de'),
            '/de/page/einigkeit-und-recht-und-freiheit/')

        # Now, let's request a language that article has not yet been translated
        # to, but has fallbacks defined, we should get EN
        self.assertEquals(article.get_absolute_url(language='fr'),
            '/en/page/god-save-queen/')

        # With settings changed to 'redirect_on_fallback': False, test again.
        with self.settings(CMS_LANGUAGES=self.NO_REDIRECT_CMS_SETTINGS):
            self.assertEquals(article.get_absolute_url(language='fr'),
                '/fr/page/god-save-queen/')

        # Now, let's request a language that has a fallback defined, but it is
        # not available either (should raise NoReverseMatch)
        with self.assertRaises(NoReverseMatch):
            article.get_absolute_url(language='it')
