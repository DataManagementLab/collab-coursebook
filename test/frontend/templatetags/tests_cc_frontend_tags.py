"""Purpose of this file

This file contains the test cases for /export/templatetags/cc_export_tags.py
"""

from frontend.templatetags.cc_frontend_tags import js_escape, format_seconds, check_approve_content_permission
from datetime import timedelta
from django.test import TestCase

from django.contrib.auth.models import User
from django.test.client import RequestFactory

from base.models import Course, Topic, Category


class JSEscapeTestCase(TestCase):
    """Export template test case

    Defines the test cases for the function js_escape.

    """
    def test_js_escape(self):
        """Test js_escape

        Tests that js_escape escapes the string correctly
        """
        escaped = js_escape('Hello\nWorld')
        self.assertEqual('Hello\\nWorld', escaped)
        escaped = js_escape('\\Hello World')
        self.assertEqual('\\\\Hello World', escaped)
        escaped = js_escape('\\Hello\nWorld')
        self.assertEqual('\\\\Hello\\nWorld', escaped)



class FormatSecondsTestCase(TestCase):
    def test_format_seconds_numeric(self):
        # Test converting seconds as a simple numeric string
        seconds = "3600"  # 1 hour
        expected_result = "1:00:00"
        result = format_seconds(seconds)
        self.assertEqual(result, expected_result)

    def test_format_seconds_format(self):
        # Test when seconds are already in the format "0:00:00"
        seconds = "1:30:00"  # 1 hour and 30 minutes
        expected_result = "1:30:00"
        result = format_seconds(seconds)
        self.assertEqual(result, expected_result)

    def test_format_seconds_invalid(self):
        # Test when seconds cannot be converted to an integer
        seconds = "invalid"
        expected_result = "invalid"
        result = format_seconds(seconds)
        self.assertEqual(result, expected_result)

class CheckApproveContentPermissionTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create()
        self.cat = Category.objects.create(title="Category")
        self.course = Course.objects.create(title='Course', description='desc', category=self.cat)
        Topic.objects.create(title="Topic", category=self.cat)

    def test_check_approve_content_permission(self):
        request = self.factory.get('/')
        request.user = self.user
        
        result = check_approve_content_permission(request.user, self.course)

        self.assertFalse(result)  # Modify this assertion based on your expected behavior