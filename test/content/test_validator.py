"""Purpose of this file

This file contains the test cases for this /content/validator.py.
"""

import os

from test import utils
from test.test_cases import MediaTestCase

from django.core.exceptions import ValidationError

import content.models as model
from content.validator import Validator

import re

class ValidatorTestCase(MediaTestCase):
    """Validator test case

    Defines the test cases for the validators.
    """

    def test_latex_valid(self):
        """Validate LaTeX test case - valid

        Tests that the function validate_latex raises no error for a valid pdf and returns None.
        """
        latex = model.Latex.objects.first()
        self.assertIsNone(Validator.validate_pdf(latex.pdf))

    def test_latex_invalid_filetype(self):
        """Validate LaTeX test case - invalid file type

        Tests that the function validate_latex raises the correct error for an invalid file
        type (image).
        """
        not_a_pdf = utils.generate_image_file(1)
        with self.assertRaises(ValidationError) as context_manager:
            Validator.validate_pdf(not_a_pdf)
        self.assertEqual('Unsupported file type.', context_manager.exception.message)

    def test_latex_invalid_extension(self):
        """Validate LaTeX test case -  invalid file extension

        Tests that the function validate_latex raises the correct error for a pdf with an invalid
        file extension (jpg).
        """
        latex = model.Latex.objects.first()
        split = os.path.splitext(latex.pdf.path)
        pre = split[0]
        new_path = pre + '.jpg'
        os.rename(latex.pdf.path, new_path)
        latex.pdf.name = new_path
        with self.assertRaises(ValidationError) as context_manager:
            Validator.validate_pdf(latex.pdf)
        self.assertEqual('Unacceptable file extension.', context_manager.exception.message)

    def test_validate_panopto_url_valid(self):
        """Test validate_panopto_url - valid URL

        Tests that the function validate_panopto_url does not raise a ValidationError
        for a valid Panopto URL.
        """
        url = "https://tu-darmstadt.cloud.panopto.eu/Panopto/Pages/Viewer.aspx?id=12345678-1234-1234-1234-1234567890ab"
        try:
            Validator.validate_panopto_url(url)
        except ValidationError:
            self.fail("validate_panopto_url raised ValidationError unexpectedly")

    def test_validate_panopto_url_invalid(self):
        """Test validate_panopto_url - invalid URL

        Tests that the function validate_panopto_url raises a ValidationError
        for an invalid Panopto URL.
        """
        url = "https://example.com"
        with self.assertRaises(ValidationError):
            Validator.validate_panopto_url(url)

    def test_validate_anki_file_invalid_type(self):
        """Validate LaTeX test case - invalid file type

        Tests that the function validate_latex raises the correct error for an invalid file
        type (image).
        """
        invalid_file = utils.generate_image_file(1)

        with self.assertRaises(ValidationError) as context_manager:
            Validator.validate_anki_file(invalid_file)
        self.assertEqual('Unsupported file type.', context_manager.exception.message)

