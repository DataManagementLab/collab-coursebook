"""Purpose of this file

This file contains the test cases for /content/widgets.py
"""
from django.test import TestCase

from content.widgets import ModifiedClearableFileInput

# Attributes
attrs = {'required': 'true',
         'accept': 'image/*',
         'class': 'form-control-file',
         'title': '',
         'id': ' id_form-0-image'}


class WidgetsTest(TestCase):
    """Models test case

    Defines the test cases for the widgets.
    """

    def test_modified_clearable_file_get_context_required(self):
        """Test get_context()

        Tests that the field is required if the given value is None.
        """
        widget = ModifiedClearableFileInput()
        ctx = widget.get_context('form-0-image', None, attrs)
        self.assertTrue(ctx['widget']['attrs']['required'])

    def test_modified_clearable_file_input_get_context_not_required(self):
        """Test get_context()

        Tests that the field is not required if the given value is not None.
        """
        widget = ModifiedClearableFileInput()
        ctx = widget.get_context('form-0-image', "Test", attrs)
        self.assertFalse(ctx['widget']['attrs']['required'])
