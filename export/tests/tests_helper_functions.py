"""Purpose of this file

This file contains the test cases for /export/helper_functions.py
"""
import os

from django.test import TestCase

from export.templatetags.cc_export_tags import tex_escape
from export.helper_functions import LaTeX

from base.models import Content

from content.models import Latex

from utils import test_utility


class HelperFunctionsTest(TestCase):
    """Export tags test case

    Defines the test cases for the helper functions.
    """

    def setUp(self):
        """
        Sets up the test database
        """
        test_utility.setup_database()

    def test_errors(self):
        """Test error()

        Tests that error() returns the correct errors.
        """
        path = os.path.dirname(__file__) + '/resources/log'
        log = open(path, mode='rb').read()
        errors = LaTeX.errors(log)
        self.assertEqual(2, len(errors))
        error1 = \
            tex_escape(r'! LaTeX Error: \begin{itemize} on input line 67 ended by \end{document}.')
        self.assertEqual(errors[1], error1)
        self.assertEqual(errors[0], '! Undefined control sequence.')

    def test_prerender_errors(self):
        """Test pre_render with a template type argument

        Tests that pre_render pre renders the content of the error_template correctly
        """
        pre_render = LaTeX.pre_render(42, False, LaTeX.error_template)
        self.assertIn('42 errors were found during compilation.', pre_render.decode(LaTeX.encoding))

    def test_prerender_latex_export(self):
        """Test pre_render without a template and with the export_flag set

        Tests that pre_render renders a Latex Content correctly for export.
        """
        content = Content.objects.first()
        latex_content = Latex.objects.first()
        pre_render = LaTeX.pre_render(content, True)
        self.assertIn(latex_content.textfield, pre_render.decode(LaTeX.encoding))
        self.assertIn(content.description, pre_render.decode(LaTeX.encoding))

    def test_prerender_latex_no_export(self):
        """Test pre_render without a template and with the export_flag not set

        Tests that pre_render renders a Latex Content correctly without the data used for export.
        """
        content = Content.objects.first()
        latex_content = Latex.objects.first()
        pre_render = LaTeX.pre_render(content, False)
        self.assertIn(latex_content.textfield, pre_render.decode(LaTeX.encoding))
        self.assertNotIn(content.description, pre_render.decode(LaTeX.encoding))
