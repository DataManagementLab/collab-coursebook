"""Purpose of this file

This file contains the test cases for /content/widgets.py.
"""

from django.test import TestCase

from content.widgets import ModifiedClearableFileInput


class ModifiedClearableFileInputTestCase(TestCase):
    """ModifiedClearableFileInput test case

    Defines the test cases for the class ModifiedClearableFileInput.

    :attr ModifiedClearableFileInputTestCase.attrs: The test attributes
    :type ModifiedClearableFileInputTestCase.attrs: dict[str, str]
    """
    attrs = {'required': 'true',
             'accept': 'image/*',
             'class': 'form-control-file',
             'title': '',
             'id': ' id_form-0-image'}

    def test_context_required(self):
        """Context test case - required

        Tests that the field is required if the given value is None with the call of the
        function get_context.
        """
        widget = ModifiedClearableFileInput()
        ctx = widget.get_context('form-0-image', None, self.attrs)
        self.assertTrue(ctx['widget']['attrs']['required'])

    def test_context_not_required(self):
        """Context test case - not required

        Tests that the field is not required if the given value is not None with the call
        of the function get_context.
        """
        widget = ModifiedClearableFileInput()
        ctx = widget.get_context('form-0-image', "Test", self.attrs)
        self.assertFalse(ctx['widget']['attrs']['required'])
