"""Purpose of this file

This file contains the test cases for /content/models.py
"""
import os

from django.test import override_settings

from base.models.content import Content

import content.models as model
from content.tests.base_test_case import BaseTestCase

from utils.test_utils import MEDIA_ROOT


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ModelsTest(BaseTestCase):
    """Models test case

    Defines the test cases for the models.
    """

    def test_generate_preview(self):
        """Test BasePDFModel.generate_preview()

        Tests that a preview image gets generated in the preview folder
        after calling generate_preview on a Latex Content.
        """
        latex = model.Latex.objects.first()
        preview_folder = 'uploads/previews/'

        self.assertFalse(os.path.exists(os.path.join(MEDIA_ROOT, preview_folder)))
        preview_path = latex.generate_preview()
        self.assertTrue(os.path.exists(os.path.join(MEDIA_ROOT, preview_folder)))

        content = Content.objects.first()
        content.preview.name = preview_path
        content.save()

        self.assertEqual('uploads/previews/Topic_Category.jpg', content.preview.name)
        self.assertTrue(bool(content.preview))
