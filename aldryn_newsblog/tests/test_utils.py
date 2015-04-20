from unittest import TestCase

from aldryn_newsblog.utils import add_prefix_to_path


class TestAddPrefixToPath(TestCase):

    def test_no_directory(self):
        self.assertEqual(
            add_prefix_to_path('template.html', 'prefix'),
            'prefix/template.html')

    def test_with_directory(self):
        self.assertEqual(
            add_prefix_to_path('directory/template.html', 'prefix'),
            'directory/prefix/template.html')
