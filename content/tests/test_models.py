"""Purpose of this file

This file contains the test cases for this /content/models.py
"""
import os
import shutil

from django.test import TestCase, override_settings

import content.models as model
from base.models.content import Content

from utility.test_utility import MEDIA_ROOT
from utility import test_utility


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class ModelsTest(TestCase):
    def setUp(self):
        """
        Sets up the test database
        """
        test_utility.setUp_database()

    @classmethod
    def tearDownClass(cls):
        """
        Deletes the generated files after running the utility.
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def test_generate_preview_latex(self):
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
