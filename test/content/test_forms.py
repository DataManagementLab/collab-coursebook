"""Purpose of this file

This file contains the test cases for /content/forms.py.
"""

from django.test import TestCase

import content.forms as form
import content.models as model


class PlaceHolderTestCase(TestCase):
    """Place holder test case

    Defines the test cases for the function get_placeholder.
    """

    def test_valid(self):
        """Test valid arguments

        Tests that that the function get_placeholder returns the correct placeholder for the
        source of a TextField.
        """
        result = form.get_placeholder(model.TextField.TYPE, 'source')
        self.assertEqual(result, 'https://www.lipsum.com/')

    def test_invalid(self):
        """Test invalid arguments

        Tests that that the function get_placeholder returns an empty placeholder for invalid
        arguments.
        """
        result = form.get_placeholder('invalid Argument', 'src')
        self.assertEqual(result, '')
