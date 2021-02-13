"""Purpose of this file

This file contains the custom test cases used to reduce redundant code..
"""
import shutil

import test.utils as utils

from django.test import TestCase, override_settings


@override_settings(MEDIA_ROOT=utils.MEDIA_ROOT)
class MediaTestCase(TestCase):
    """Media test case

    Defines the test cases related operations related to media.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        utils.setup_database()

    @classmethod
    def tearDownClass(cls):
        """Tear down class

        Deletes the generated files after running the tests.
        """
        shutil.rmtree(utils.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
