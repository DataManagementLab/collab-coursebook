"""Purpose of this file

This file contains the test cases for this /content/models.py
"""
import os

from django.core.exceptions import ValidationError
from django.test import override_settings

import content.models as model
from content.tests.base_test_case import BaseTestCase
from content.validator import validate_pdf

from utils import test_utility
from utils.test_utility import MEDIA_ROOT


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ValidatorTest(BaseTestCase):
    """Validator test case

    Defines the test cases for the validators.
    """

    def test_validate_pdf_valid(self):
        """Test validate_pdf() with a valid pdf

        Tests that validate_pdf raises no error for a valid pdf and returns None.
        """
        latex = model.Latex.objects.first()
        self.assertIsNone(validate_pdf(latex.pdf))

    def test_validate_pdf_invalid_filetype(self):
        """Test validate_pdf() with an invalid file type

        Tests that validate_pdf raises the correct error for an image.
        """
        not_a_pdf = test_utility.generate_image_file(1)
        with self.assertRaises(ValidationError) as context_manager:
            validate_pdf(not_a_pdf)
        self.assertEqual('Unsupported file type.', context_manager.exception.message)

    def test_validate_pdf_invalid_file_extension(self):
        """Test validate_pdf() with an invalid file extension

        Tests that validate_pdf raises the correct error for a pdf with a .jpg extension.
        """
        latex = model.Latex.objects.first()
        split = os.path.splitext(latex.pdf.path)
        pre = split[0]
        new_path = pre + '.jpg'
        os.rename(latex.pdf.path, new_path)
        latex.pdf.name = new_path
        with self.assertRaises(ValidationError) as context_manager:
            validate_pdf(latex.pdf)
        self.assertEqual('Unacceptable file extension.', context_manager.exception.message)
