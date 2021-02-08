"""Purpose of this file

This file contains the test cases for /content/forms.py
"""
from django.test import TestCase

import content.forms as form
import content.models as model


class FormsTest(TestCase):
    def test_get_placeholder_valid(self):
        """Test get_placeholder with valid arguments

        Tests that that the form.get_placeholder returns the correct placeholder for the source of
        a TextField.
        """
        result = form.get_placeholder(model.TextField.TYPE, 'source')
        self.assertEqual(result, 'https://www.lipsum.com/')

    def test_get_placeholder_invalid(self):
        """Test get_placeholder with invalid arguments

        Tests that that the form.get_placeholder returns an empty placeholder for invalid arguments.
        """
        result = form.get_placeholder('invalid Argument', 'src')
        self.assertEqual(result, '')
