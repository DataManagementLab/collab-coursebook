"""Purpose of this file

This file contains the test cases for /export/helper_functions.py.
"""

import os

from test import utils

from django.test import TestCase

import content.models as model

import export.helper_functions as helper
from content.attachment.forms import LatexPreviewImageAttachmentFormSet
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
        self.assertIn(latex_content.pdf.url, pre_render.decode(helper.Latex.encoding))
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

    def test_prerender_latex_preview(self):
        """Prerender test case - LaTeX preview

        Tests that the function preview_prerender renders the latex code correctly and replaces
        all the attachment embedding codes with their corresponding modified file names.
        """
        latex_code = "Lorem ipsum " \
                     "\\includegraphics[width=\\textwidth]{Image-0}" \
                     "\\includegraphics[width=\\textwidth]{Image-1}"
        test_files = [utils.generate_image_file(0), utils.generate_image_file(1)]
        data = {
            'form-TOTAL_FORMS': '2',
            'form-INITIAL_FORMS': '0',
        }
        files = {
            'form-0-image': test_files[0],
            'form-1-image': test_files[1],
        }
        formset = LatexPreviewImageAttachmentFormSet(data, files)
        pre_render = helper.Latex.preview_prerender(latex_code, formset)
        latex_code = "Lorem ipsum " \
                     f"\\includegraphics[width=\\textwidth]{{0_{test_files[0].name}}}" \
                     f"\\includegraphics[width=\\textwidth]{{1_{test_files[1].name}}}"
        self.assertIn(latex_code, pre_render.decode(helper.Latex.encoding))


class MarkdownTestCase(TestCase):
    """Markdown test case

    Defines the test cases for the class Markdown.
    """
    def setUp(self):
        """
        Sets up the test database
        """
        utils.setup_database()

    def test_markdown_render(self):
        """Markdown render test case

        Tests if the Markdown compiler renders the Markdown text correctly with extended Markdown
        syntax.
        """
        text1 = "| Option | Description | \n" \
                "| ------ | ----------- | \n" \
                "| text   | text |"
        res1 = "<table>\n" \
               "<thead>\n" \
               "<tr>\n" \
               "<th>Option</th>\n" \
               "<th>Description</th>\n" \
               "</tr>\n" \
               "</thead>\n" \
               "<tbody>\n" \
               "<tr>\n" \
               "<td>text</td>\n" \
               "<td>text</td>\n" \
               "</tr>\n" \
               "</tbody>\n" \
               "</table>\n"
        text2 = "~~Strikethrough~~"
        res2 = "<p><s>Strikethrough</s></p>\n"
        content1 = utils.create_content(model.MDContent.TYPE)
        content2 = utils.create_content(model.MDContent.TYPE)
        model.MDContent.objects.create(textfield=text1, content=content1)
        model.MDContent.objects.create(textfield=text2, content=content2)
        md1 = helper.Markdown.render(content1, False)
        self.assertEqual(md1, res1)
        md2 = helper.Markdown.render(content2, False)
        self.assertEqual(md2, res2)
