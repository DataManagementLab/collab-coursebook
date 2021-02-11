"""Purpose of this file

This file contains the test cases for /export/templatetags/cc_export_tags.py
"""
import os

from django.test import TestCase

import content

from content.models import ImageContent, Latex, TextField, YTVideoContent

from export.templatetags.cc_export_tags import export_template

# Base path
base_path = os.path.dirname(content.__file__)
path = base_path + "/templates/content/export/"


class ExportTagsTest(TestCase):
    """Export tags test case

    Defines the test cases for the export tags.
    """

    def test_export_template_image(self):
        """Test export_template() for image Contents

        Tests that export_template returns the correct Path for the image template.
        """
        image_template = export_template(ImageContent.TYPE)
        self.assertEqual(image_template, path + 'Image.tex')

    def test_export_template_latex(self):
        """Test export_template() for Latex Contents

        Tests that export_template returns the correct Path for the Latex template.
        """
        image_template = export_template(Latex.TYPE)
        self.assertEqual(image_template, path + 'Latex.tex')

    def test_export_template_textfield(self):
        """Test export_template() for TextField Contents

        Tests that export_template returns the correct Path for the TextField template.
        """
        image_template = export_template(TextField.TYPE)
        self.assertEqual(image_template, path + 'Textfield.tex')

    def test_export_template_ytvideo(self):
        """Test export_template() for YouTube Video Contents

        Tests that export_template returns the correct Path for the YouTube Video template.
        """
        image_template = export_template(YTVideoContent.TYPE)
        self.assertEqual(image_template, path + 'YouTubeVideo.tex')

    def test_export_template_error(self):
        """Test export_template() for the error template

        Tests that export_template returns the correct Path for the Error template.
        """
        image_template = export_template('error')
        self.assertEqual(image_template, path + 'error.tex')

    def test_export_template_invalid(self):
        """Test export_template() for invalid templates

        Tests that export_template returns the correct Path for the invalid template.
        """
        image_template = export_template('lol')
        self.assertEqual(image_template, path + 'invalid.tex')
