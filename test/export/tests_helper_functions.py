"""Purpose of this file

This file contains the test cases for /export/helper_functions.py.
"""

import os

from test import utils

from django.test import TestCase

import content.models as model

import export.helper_functions as helper

from export.templatetags.cc_export_tags import tex_escape


class LaTeXTestCase(TestCase):
    """LaTeX test case

    Defines the test cases for the class Latex.
    """

    def setUp(self):
        """
        Sets up the test database
        """
        utils.setup_database()

    def test_error_successful(self):
        """Error test case - successful

        Tests that the function error returns the correct errors.
        """
        path = os.path.dirname(__file__) + '/resources/log'
        log = open(path, mode='rb').read()
        errors = helper.Latex.errors(log)
        self.assertEqual(2, len(errors))
        error1 = \
            tex_escape(r'! Latex Error: \begin{itemize} on input line 67 ended by \end{document}.')
        self.assertEqual(errors[1], error1)
        self.assertEqual(errors[0], '! Undefined control sequence.')

    def test_prerender_errors_template(self):
        """Prerender test case - error template

        Tests that the function prerender pre renders the content of the error template correctly.
        """
        pre_render = helper.Latex.pre_render(content=42,
                                             export_flag=False,
                                             template_type=helper.Latex.error_template,
                                             no_error=False)
        self.assertIn('42 errors were found during compilation.',
                      pre_render.decode(helper.Latex.encoding))

    def test_prerender_latex_export(self):
        """Prerender test case -  LaTeX export

        Tests that the function prerender renders a LaTeX content correctly for export.
        """
        content = model.Content.objects.first()
        latex_content = model.Latex.objects.first()
        pre_render = helper.Latex.pre_render(content, True)
        self.assertIn(latex_content.textfield, pre_render.decode(helper.Latex.encoding))
        self.assertIn(content.description, pre_render.decode(helper.Latex.encoding))

    def test_prerender_latex_no_export(self):
        """Prerender test case - LaTeX no export

        Tests that the function prerender renders a LaTeX content correctly without the data used
        for export.
        """
        content = model.Content.objects.first()
        latex_content = model.Latex.objects.first()
        pre_render = helper.Latex.pre_render(content, False)
        self.assertIn(latex_content.textfield, pre_render.decode(helper.Latex.encoding))
        self.assertNotIn(content.description, pre_render.decode(helper.Latex.encoding))
