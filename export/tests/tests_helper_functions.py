"""Purpose of this file

This file contains the test cases for /export/helper_functions.py
"""
import os

from django.test import TestCase

from export.templatetags.cc_export_tags import tex_escape
from export.helper_functions import LaTeX
from utility import test_utility
from base.models import Content
from content.models import Latex


class HelperFunctionsTest(TestCase):
    def setUp(self):
        """
        Sets up the test database
        """
        test_utility.setup_database()

    def test_errors(self):
        path = os.path.dirname(__file__) + '/resources/log'
        log = open(path, mode='rb').read()
        errors = LaTeX.errors(log)
        self.assertEqual(2, len(errors))
        error1 = tex_escape(r'! LaTeX Error: \begin{itemize} on input line 67 ended by \end{document}.')
        self.assertEqual(errors[1], error1)
        self.assertEqual(errors[0], '! Undefined control sequence.')

    def test_prerender_errors(self):
        x = LaTeX.pre_render(42, False, LaTeX.error_template)
        self.assertIn('42 errors were found during compilation.', x.decode(LaTeX.encoding))

    def test_prerender_Latex_export(self):
        content = Content.objects.first()
        latex_content = Latex.objects.first()
        x = LaTeX.pre_render(content, True)
        self.assertIn(latex_content.textfield, x.decode(LaTeX.encoding))
        self.assertIn(content.description, x.decode(LaTeX.encoding))

    def test_prerender_Latex_no_export(self):
        content = Content.objects.first()
        latex_content = Latex.objects.first()
        x = LaTeX.pre_render(content, False)
        self.assertIn(latex_content.textfield, x.decode(LaTeX.encoding))
        self.assertNotIn(content.description, x.decode(LaTeX.encoding))
