"""Purpose of this file

This file contains the test cases for /content/models.py.
"""

import os


from test.test_cases import MediaTestCase
from test import utils

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
