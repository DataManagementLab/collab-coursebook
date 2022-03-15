"""Purpose of this file

This file contains the test cases for /content/forms.py.
"""
from django.core.files.uploadedfile import SimpleUploadedFile
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


class AddMDTestCase(TestCase):
    """ AddMD form test case

    Defines the test cases for the form AddMD, specifically, the clean() method of AddMD.

    """

    def test_invalid_options(self):
        """Test invalid options field

        Tests that when the options field has no value, the form is invalid and returns the
        correct message.
        The form should be invalid even when the file field and the text field are valid.
        """
        form_data = {'textfield': 'Lorem ipsum',
                     'md': SimpleUploadedFile("test_file.md", b"Lorem ipsum"),
                     'language': 'de',
                     'source': 'src', }
        test_form = form.AddMD(data=form_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors['options'], ["This field is required."])
        self.assertEqual(test_form.errors['__all__'], ["None of the options were chosen."])

    def test_missing_file_with_textfield(self):
        """
        Test invalid file field (with valid textfield supplied)

        Tests that when the options field is set to 'file', but there is no file inputted
        in the field,
        then the form is invalid and returns the correct message.
        The same message should be given out regardless of whether the textfield is inputted or not.
        """
        form_data = {'options': 'file',
                     'textfield': 'Lorem ipsum',
                     'language': 'de',
                     'source': 'src', }
        test_form = form.AddMD(data=form_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors['__all__'], ["You must upload a Markdown file."])

    def test_missing_file_without_textfield(self):
        """
        Test invalid file field (with no value of textfield)

        Tests that when the options field is set to 'file', but there is no file inputted
        in the field,
        then the form is invalid and returns the correct message.
        The same message should be given out regardless of whether the textfield is inputted or not.
        """
        form_data = {'options': 'file',
                     'language': 'de',
                     'source': 'src', }
        test_form = form.AddMD(data=form_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors['__all__'], ["You must upload a Markdown file."])

    def test_missing_text_with_filefield(self):
        """
        Test invalid text field (with file field supplied, but has the wrong extension).

        Tests that when the options field is set to 'text', but there no text is inputted
        in the field,
        then the form is invalid and returns the correct message.
        The same message should be given out regardless of whether the file field is inputted
        (with correct/incorrect
        extensions) or not.
        """
        form_data = {'options': 'text',
                     'md': SimpleUploadedFile("test_file.txt", b"Lorem ipsum"),
                     'language': 'de',
                     'source': 'src', }
        test_form = form.AddMD(data=form_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors['__all__'], ["You must put in some text."])

    def test_missing_text_without_filefield(self):
        """
        Test invalid textfield (with no files uploaded to the file field).

        Tests that when the options field is set to 'text', but there no text is inputted in the
        field,
        then the form is invalid and returns the correct message.
        The same message should be given out regardless of whether the file field is inputted
        (with correct/incorrect
        extensions) or not.
        """
        form_data = {'options': 'text',
                     'language': 'de',
                     'source': 'src', }
        test_form = form.AddMD(data=form_data)
        self.assertFalse(test_form.is_valid())
        self.assertEqual(test_form.errors['__all__'], ["You must put in some text."])
