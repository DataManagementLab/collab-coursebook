"""Purpose of this file

This file contains the test cases for /export/templatetags/cc_export_tags.py
"""
import os

from django.test import TestCase

import content
from content.models import ImageContent, Latex, TextField, YTVideoContent
from export.templatetags.cc_export_tags import export_template

base_path = os.path.dirname(content.__file__)
path = base_path + "/templates/content/export/"


class ExportTagsTest(TestCase):
    def test_export_template_image(self):
        image_template = export_template(ImageContent.TYPE)
        self.assertEqual(image_template, path + 'Image.tex')

    def test_export_template_latex(self):
        image_template = export_template(Latex.TYPE)
        self.assertEqual(image_template, path + 'Latex.tex')

    def test_export_template_textfield(self):
        image_template = export_template(TextField.TYPE)
        self.assertEqual(image_template, path + 'Textfield.tex')

    def test_export_template_ytvideo(self):
        image_template = export_template(YTVideoContent.TYPE)
        self.assertEqual(image_template, path + 'YouTubeVideo.tex')

    def test_export_template_error(self):
        image_template = export_template('error')
        self.assertEqual(image_template, path + 'error.tex')

    def test_export_template_invalid(self):
        image_template = export_template('lol')
        self.assertEqual(image_template, path + 'invalid.tex')
