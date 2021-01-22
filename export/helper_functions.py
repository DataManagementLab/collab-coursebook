"""Purpose of this file

This file contains utility functions related to exporting and rendering files.
"""

import os

import tempfile

from subprocess import Popen, PIPE

from django.template.loader import get_template

from export.templatetags.cc_export_tags import export_template, tex_escape


class LaTeX:
    """LaTeX Export

    This class takes care of the export and rendering of LaTeX code.
    
    Attributes:
        LaTeX.encoding (str): The file encoding
        LaTeX.error_prefix (str): The error prefix character to find the error message in the logs
        LaTeX.error_template (str): The name of the error template if the compilation went wrong
    """
    encoding = 'utf-8'
    error_prefix = '!'
    error_template = 'error'

    @staticmethod
    def render(context, template_name):
        """Render

        Renders the LaTeX code with its content and then compiles the code to generate
        a PDF with its log.

        https://github.com/d120/pyophase/blob/master/ophasebase/helper.py
        Retrieved 10.08.2020

        :param context: The context of the content to be rendered
        :type context: dict
        :param template_name: The name of the template to use
        :type template_name: str

        :return: the rendered LaTeX code as PDF, PDF LaTeX output and its the rendered template
        :rtype: Tuple[bytes, Tuple[bytes, bytes], str]
        """
        template = get_template(template_name)
        rendered_tpl = template.render(context).encode(LaTeX.encoding)
        # Prerender content templates
        for content in context['contents']:
            rendered_tpl += LaTeX.pre_render(content, context['export_pdf'])
        rendered_tpl += r"\end{document}".encode(LaTeX.encoding)

        with tempfile.TemporaryDirectory() as tempdir:

            process = Popen(['pdflatex'], stdin=PIPE, stdout=PIPE, cwd=tempdir, )

            # Output is a byte tuple of stdout and stderr
            pdflatex_output = process.communicate(rendered_tpl)

            # Filter error messages in log (stdout)
            errors = LaTeX.errors(pdflatex_output[0])
            # Error log
            if len(errors) != 0:
                rendered_tpl = template.render(context).encode(LaTeX.encoding)
                # prerender errors templates
                rendered_tpl += LaTeX.pre_render(errors, context['export_pdf'],
                                                 LaTeX.error_template)
                rendered_tpl += r"\end{document}".encode(LaTeX.encoding)

                process = Popen(['pdflatex'], stdin=PIPE, stdout=PIPE, cwd=tempdir, )
                pdflatex_output = process.communicate(rendered_tpl)

            try:
                with open(os.path.join(tempdir, 'texput.pdf'), 'rb') as file:
                    pdf = file.read()
            except FileNotFoundError:
                pdf = None
        return pdf, pdflatex_output, rendered_tpl

    @staticmethod
    def errors(lob):
        """Error log

        Checks the given log if there are error messages and returns the messages.
        If there are none, an empty list will be returned.

        Parameters:
            :param lob: A list of bytes representing the PDF LaTeX compile log
            :type lob: List[byte]

        :return: the error messages from the log (stdout)
        :rtype: List[str]
        """
        # Decode bytes to string and split the string by the delimiter '\n'
        lines = lob.decode(LaTeX.encoding).splitlines()
        errors = []
        for line in lines:
            # LaTeX log errors contains '!'
            index = line.find(LaTeX.error_prefix)
            if index != -1:
                tmp = line[index:]
                # Do not add duplicates
                if errors.__contains__(tmp):
                    continue
                tmp = tex_escape(tmp)
                errors.append(tmp)
        return errors

    @staticmethod
    def pre_render(content, export_flag, template_type=None):
        """Prerender

        Prerender the given content and its corresponding template. If there
        is no template specified, the template will associated with the type
        of the content.

        Parameters:
            :param content: The content to be rendered
            :type content: Content
            :param export_flag: True if export, False if simple content compilation
            :type export_flag: bool
            :param template_type: The type of the template to use
            :type template_type: str

        :return: the rendered template
        :rtype: str
        """
        if template_type is None:
            template = get_template(export_template(content.type))
        else:
            template = get_template(export_template(template_type))

        # Set context for rendering
        context = {'content': content, 'export_pdf': export_flag}

        # Return result of rendering
        return template.render(context).encode(LaTeX.encoding)
