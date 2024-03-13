"""Purpose of this file

This file contains the test cases for this /content/validator.py.
"""

import os

from test import utils
from test.test_cases import MediaTestCase

from django.core.exceptions import ValidationError

import content.models as model
from content.validator import Validator


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


    """
    Sadly we didn't figer out how to test the validate_anki_file function, because we couldn't find a way to generate a valid anki file in memory.
    With the genanki library we could generate an anki file and we were able to store it in a ByteIO buffer. We encountered the problem in the logical next
    step: while validating the generated file, the function validate_anki_file raised an error, because the file was not a valid anki file. Upon further
    inspection we found out that the generated file has the mimetype 'application/empty', expected was 'application/zip'. We tried to change the mimetype of the
    ByteIO buffer, but we were not able to do so.
    We came to the following conclusions:
    - Anki deck in memory: Mimetype is 'application/empty', expected is 'application/zip'
    - Anki deck on disk: Mimetype is 'application/octet-stream', expected is 'application/zip'
    - Anki deck imported via the webinterface: Mimetype is 'application/zip'

    Because of this we decided to skip the test for the validate_anki_file function.
    """
    @utils.skip
    def test_anki_file_valid(self):
        """Validate Anki Deck test case - valid

        Tests that the function validate_anki_file raises no error for a valid anki deck file and returns None.
        """
        anki_test_file = utils.generate_anki_file('name')
        self.assertIsNone(Validator.validate_anki_file(anki_test_file))
