"""Purpose of this file

This file contains the test cases for /content/models.py.
"""

import os

from django.core.exceptions import ValidationError

from test.test_cases import MediaTestCase
import test.utils as utils

from django.test import override_settings

from base.models import Content

import content.models as model


@override_settings(MEDIA_ROOT=utils.MEDIA_ROOT)
class LatexTestCase(MediaTestCase):  # pylint: disable=too-few-public-methods)
    """LaTeX test case

    Defines the test cases for the model Latex.
    """

    def test_generate_preview_successful(self):
        """Generate preview test case - successful

        Tests that a preview image gets generated in the preview folder
        after calling generate_preview on a LaTeX Content.
        """
        latex = model.Latex.objects.first()
        preview_folder = 'uploads/previews/'

        self.assertFalse(os.path.exists(os.path.join(utils.MEDIA_ROOT, preview_folder)))
        preview_path = latex.generate_preview()
        self.assertTrue(os.path.exists(os.path.join(utils.MEDIA_ROOT, preview_folder)))

        content = Content.objects.first()
        content.preview.name = preview_path
        content.save()

        self.assertEqual('uploads/previews/Topic_Category.jpg', content.preview.name)
        self.assertTrue(bool(content.preview))

class MDContentTestCase(MediaTestCase): # pylint: disable=too-few-public-methods)
    """LaTeX test case

        Defines the test cases for the model MDContent.
    """
    def testClean(self):
        md = model.MDContent.objects.create()
        self.assertFalse(bool(md.md))
        self.assertFalse(bool(md.textfield))
        with self.assertRaises(ValidationError) as context_manager:
            md.clean()
        self.assertEqual("You must input either a Markdown file or Markdown script.", context_manager.exception.message)