"""Purpose of this file

This file contains the test cases for /base/models/content.py.
"""

import shutil
from test import utils

from django.test import TestCase
from django.contrib.auth.models import User  # pylint: disable=imported-auth-user

from base.models import Course
import base.models.profile as Profile

class ModelTestCase(TestCase):
    """Content test case

    Defines the test cases related to the content.
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        utils.setup_database()
        self.client.force_login(User.objects.first())

    @classmethod
    def tearDownClass(cls):
        """Tear down class

        Deletes the generated files after running the tests.
        """
        shutil.rmtree(utils.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()


class CourseModelTestCase(ModelTestCase):
    """ test cases for Course

    Defines the test cases for model Course
    """

    def setUp(self):
        """Setup

        Sets up the test database.
        """
        super().setUp()
        course = Course.objects.first()
        course.moderators.add(Profile.Profile.objects.first())
        course.save()

    # Test the moderator property
    def test_moderator(self):
        """Course moderator test case

        Tests the moderator property of Course.
        """
        self.assertEqual(Course.objects.first().moderators.first(), Profile.Profile.objects.first())
