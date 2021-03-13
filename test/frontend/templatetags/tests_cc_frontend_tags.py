"""Purpose of this file

This file contains the test cases for /export/templatetags/cc_export_tags.py
"""

from django.test import TestCase

from frontend.templatetags.cc_frontend_tags import js_escape


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
