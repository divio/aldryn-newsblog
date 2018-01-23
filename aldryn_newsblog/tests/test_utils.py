# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.core.urlresolvers import NoReverseMatch, reverse

from unittest import TestCase

from ..utils import add_prefix_to_path, default_reverse


class TestAddPrefixToPath(TestCase):

    def test_no_directory(self):
        self.assertEqual(
            add_prefix_to_path('template.html', 'prefix'),
            'prefix/template.html')

    def test_with_directory(self):
        self.assertEqual(
            add_prefix_to_path('directory/template.html', 'prefix'),
            'directory/prefix/template.html')

    def test_default_reverse(self):
        non_pattern = 'invalid_url_pattern'

        # *********************************************************************
        # NOTE: Until we drop support for Python 2.6, we can't use the context-
        # manager form of assertRaises =(
        # *********************************************************************

        # First, test that the normal reverse works as expected (this proves
        # that our setup conditions make sense)
        try:
            reverse(non_pattern)
        except NoReverseMatch:
            pass
        except Exception as e:
            raise e
        else:
            self.fail('reverse did not raise expected NoReverseMatch.')

        # Test that default_reverse without a default set, acts the same
        # as above.
        try:
            default_reverse(non_pattern)
        except NoReverseMatch:
            pass
        except Exception as e:
            raise e
        else:
            self.fail('reverse did not raise expected NoReverseMatch.')

        # Now prove that default_reverse WITH a default returns that default.
        # Trying with multiple types of values
        class MyClass():
            pass

        defaults = [
            'some_value', '', 'Undefined',
            1, 0,
            True, False,
            None, MyClass, MyClass(),
        ]

        for default in defaults:
            try:
                self.assertEquals(
                    default_reverse(non_pattern, default=default),
                    default
                )
            except:  # noqa: E722
                self.fail('default_reverse raised exception even though we '
                          'set a default value of: {0}.'.format(default))
