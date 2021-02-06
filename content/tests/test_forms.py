"""Purpose of this file

This file contains the test cases for /content/forms.py
"""
from django.test import TestCase

import content.forms as form
import content.models as model


class FormsTest(TestCase):
    def test_get_placeholder_valid(self):
        result = form.get_placeholder(model.TextField.TYPE, 'source')
        self.assertEqual(result, 'https://www.lipsum.com/')

    def test_get_placeholder_invalid(self):
        result = form.get_placeholder('invalid Argument', 'src')
        self.assertEqual(result, '')
