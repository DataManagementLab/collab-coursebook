"""Purpose of this file

This file contains utility functions related to exporting and rendering files.
"""

import os
import re
import tempfile

from subprocess import Popen, PIPE

from django.template.loader import get_template

from export.templatetags.cc_export_tags import export_template, tex_escape


class Latex:
    """LaTeX Export

    This class takes care of the export and rendering of LaTeX code.

    :attr Latex.encoding: The file encoding
    :type Latex.encoding: str
    :attr Latex.error_prefix: The error prefix character to find the error message in the logs
    :type Latex.error_prefix: str
    :attr Latex.error_template: he name of the error template if the compilation went wrong
    :type Latex.error_template: str
    """
    encoding = 'utf-8'
    error_prefix = '!'
    error_template = 'error'

    # TODO documentation parameters
    @staticmethod
    def render(context, template_name, assets, app='export', external_assets=None):
        """Render

        Renders the LaTeX code with its content and then compiles the code to generate
        a PDF with its log.

        https://github.com/d120/pyophase/blob/master/ophasebase/helper.py
        Retrieved 10.08.2020

        :param context: The context of the content to be rendered
        :type context: dict
        :param template_name: The name of the template to use
        :type template_name: str
        :param assets:
        :type assets:
        :param app:
        :type: str
        :param external_assets:
        :type external_assets:

        :return: the rendered LaTeX code as PDF, PDF LaTeX output and its the rendered template
        :rtype: tuple[bytes, tuple[bytes, bytes], str]
        """
        template = get_template(template_name)
        rendered_tpl = template.render(context).encode(Latex.encoding)
        # Prerender content templates
        for content in context['contents']:
            rendered_tpl += Latex.pre_render(content, context['export_pdf'])
        rendered_tpl += r"\end{document}".encode(Latex.encoding)

        with tempfile.TemporaryDirectory() as tempdir:

            process = Popen(['pdflatex'], stdin=PIPE, stdout=PIPE, cwd=tempdir, )

            # Output is a byte tuple of stdout and stderr
            pdflatex_output = process.communicate(rendered_tpl)

            # Filter error messages in log (stdout)
            error_log = Latex.errors(pdflatex_output[0])
            # Error log
            if len(error_log) != 0:
                rendered_tpl = template.render(context).encode(Latex.encoding)
                # Prerender errors templates
                rendered_tpl += Latex.pre_render(len(error_log), context['export_pdf'],
                                                 Latex.error_template)
                rendered_tpl += r"\end{document}".encode(Latex.encoding)

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
            :type lob: list[byte]

        :return: the error messages from the log (stdout)
        :rtype: list[str]
        """
        # Decode bytes to string and split the string by the delimiter '\n'
        lines = lob.decode(Latex.encoding).splitlines()
        found = []
        for line in lines:
            # LaTeX log errors contains '!'
            index = line.find(Latex.error_prefix)
            if index != -1:
                tmp = line[index:]
                # Do not add duplicates
                if found.__contains__(tmp):
                    continue
                tmp = tex_escape(tmp)
                found.append(tmp)
        return found

    @staticmethod
    def pre_render(content, export_flag, template_type=None):
        """Prerender

        Prerender the given content and its corresponding template. If there
        is no template specified, the template will associated with the type
        of the content.

        Parameters:
            :param content: The content to be rendered
            :type content: any
            :param export_flag: True if export, False if simple content compilation
            :type export_flag: bool
            :param template_type: The type of the template to use
            :type template_type: str

        :return: the rendered template
        :rtype: bytes
        """
        if template_type is None:
            template = get_template(export_template(content.type))
        else:
            template = get_template(export_template(template_type))

        # Set context for rendering
        context = {'content': content, 'export_pdf': export_flag}

        # render the template and use escape for triple braces with escape character ~~
        # this is relevant when using triple braces for file paths in tex data
        rendered_tpl = template.render(context)
        rendered_tpl = re.sub('{~~', '{', rendered_tpl).encode(Latex.encoding)
        return rendered_tpl
