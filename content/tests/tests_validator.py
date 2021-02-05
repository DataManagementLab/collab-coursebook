"""Purpose of this file

This file contains the test cases for this /content/models.py
"""
import os
import shutil

from django.core.exceptions import ValidationError
from django.test import TestCase, override_settings

import content.models as model
from content.validator import validate_pdf

from utility.test_utility import MEDIA_ROOT
from utility import test_utility


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ValidatorTest(TestCase):

    def setUp(self):
        """
        Sets up the test database
        """
        test_utility.setup_database()

    @classmethod
    def tearDownClass(cls):
        """
        Deletes the generated files after running the utility.
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_validate_pdf_valid(self):
        latex = model.Latex.objects.first()
        self.assertIsNone(validate_pdf(latex.pdf))

    def test_validate_pdf_invalid_filetype(self):
        not_a_pdf = test_utility.generate_image_file(1)
        with self.assertRaises(ValidationError) as cm:
            validate_pdf(not_a_pdf)
        exception = cm.exception
        self.assertEqual('Unsupported file type.', exception.message)

    def test_validate_pdf_invalid_file_extension(self):
        latex = model.Latex.objects.first()
        pre, ext = os.path.splitext(latex.pdf.path)
        new_path = pre + '.jpg'
        os.rename(latex.pdf.path, new_path)
        latex.pdf.name = new_path
        with self.assertRaises(ValidationError) as cm:
            validate_pdf(latex.pdf)
        exception = cm.exception
        self.assertEqual('Unacceptable file extension.', exception.message)
