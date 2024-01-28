"""Purpose of this file

This file contains the test cases for /export/templatetags/cc_export_tags.py
"""

from frontend.templatetags.cc_frontend_tags import js_escape
from datetime import timedelta
from django.test import TestCase
from frontend.templatetags.cc_frontend_tags import format_seconds


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