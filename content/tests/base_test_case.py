"""Purpose of this file

This file contains the base test case setup for external resources e.g. database.
"""

import shutil

from django.test import TestCase, override_settings

from utils import test_utils
from utils.test_utils import MEDIA_ROOT


@override_settings(MEDIA_ROOT=MEDIA_ROOT)
class BaseTestCase(TestCase):
    """Base test case

    Defines the  base test case set up which needs
    to communicate with the database.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        test_utils.setup_database()

    @classmethod
    def tearDownClass(cls):
        """Teat down class

        Deletes the generated files after running the tests.
        """
        shutil.rmtree(MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()
