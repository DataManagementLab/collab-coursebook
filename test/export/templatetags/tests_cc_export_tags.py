"""Purpose of this file

This file contains the test cases for /export/templatetags/cc_export_tags.py
"""
import os

from django.test import TestCase

import content
import content.models as model

from export.templatetags.cc_export_tags import export_template


class ExportTemplateTestCases(TestCase):
    """Export template test case

    Defines the test cases for the function export_template.

    :attr ExportTemplateTestCases.base_path: The base directory path of the templates.
    :type ExportTemplateTestCases.base_path: str
    :attr ExportTemplateTestCase.path: The path to the templates
    :type ExportTemplateTestCases.path: str
    """
    base_path = os.path.dirname(content.__file__)
    path = base_path + "/templates/content/export/"

    def test_image(self):
        """Test image content

        Tests that the function returns the correct path for the image template.
        """
        image_template = export_template(model.ImageContent.TYPE)
        self.assertEqual(image_template, self.path + 'Image.tex')

    def test_latex(self):
        """Test LaTex content

        Tests that the function returns the correct path for the LaTeX template.
        """
        image_template = export_template(model.Latex.TYPE)
        self.assertEqual(image_template, self.path + 'Latex.tex')

    def test_textfield(self):
        """Test TextField content

        Tests that the function returns the correct path for the TextField template.
        """
        image_template = export_template(model.TextField.TYPE)
        self.assertEqual(image_template, self.path + 'Textfield.tex')

    def test_ytvideo(self):
        """Test YouTube video content

        Tests that the function returns the correct path for the YouTube video template.
        """
        image_template = export_template(model.YTVideoContent.TYPE)
        self.assertEqual(image_template, self.path + 'YouTubeVideo.tex')

    def test_error(self):
        """Test error

        Tests that the function returns the correct path for the error template.
        """
        image_template = export_template('error')
        self.assertEqual(image_template, self.path + 'error.tex')

    def test_invalid(self):
        """Test invalid

        Tests that the function returns the correct path for the invalid template.
        """
        image_template = export_template('lol')
        self.assertEqual(image_template, self.path + 'invalid.tex')
