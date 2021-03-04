"""Purpose of this file

This file contains the custom test cases used to reduce redundant code..
"""
import shutil

import reversion
from reversion import set_comment

from base.models import Category, Course, Topic, CourseStructureEntry
from test import utils

from django.contrib.auth.models import User  # pylint: disable=imported-auth-user

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
        self.client.force_login(User.objects.first())

    @classmethod
    def tearDownClass(cls):
        """Tear down class

        Deletes the generated files after running the tests.
        """
        shutil.rmtree(utils.MEDIA_ROOT, ignore_errors=True)
        super().tearDownClass()

    def assertContainsHtml(self, response, *args):
        for html in args:
            try:
                self.assertContains(response, html, html=True)
            except AssertionError as e:
                print(e)
                raise


class BaseCourseViewTestCase(MediaTestCase):
    """ Base test cases for CourseView and EditCourseStructureView

    Defines the test cases for view  CourseView and EditCourseStructureView
    """
    def setUp(self):
        """Setup

        Sets up the test database.
        """
        super().setUp()

        self.user = User.objects.get(pk=1)

        self.cat = Category.objects.create(title="Category")
        # set up a course item to test
        with reversion.create_revision():
            self.course1 = Course.objects.create(title='Course Test', description='desc', category=self.cat)
            self.course1.owners.add(self.user.profile)

            self.topic1 = Topic.objects.create(title="Topic1", category=self.cat)
            self.topic2 = Topic.objects.create(title="Topic2", category=self.cat)
            self.topic3 = Topic.objects.create(title="Topic3", category=self.cat)

            course_struc_entry_1 = CourseStructureEntry(course=self.course1, index=1, topic=self.topic1)
            course_struc_entry_2 = CourseStructureEntry(course=self.course1, index=2, topic=self.topic2)
            course_struc_entry_3 = CourseStructureEntry(course=self.course1, index="2/1", topic=self.topic3)
            course_struc_entry_1.save(), course_struc_entry_2.save(), course_struc_entry_3.save()
            set_comment('initial version')
