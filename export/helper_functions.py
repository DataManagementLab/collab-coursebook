"""Purpose of this file

This file contains utility functions related to exporting and rendering files.
"""

import os
import re
import tempfile
from subprocess import Popen, PIPE
import pdfkit
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from django.utils.translation import gettext

from django.template.loader import get_template

from export.templatetags.cc_export_tags import export_template, tex_escape, ret_path
from content.static.yt_api import seconds_to_time, get_video_length, time_to_string


class Markdown: # pylint: disable=too-few-public-methods
    """Markdown

    This class provides the function for rendering Markdown into HTML.
    """
    @staticmethod
    def render(content, is_absolute):
        """Render

        Replaces all attachment embedding code in the Markdown content with the path of
        the corresponding attachment, either relative or absolute,
        then compiles and returns the HTML from the Markdown content.

        :param content: Markdown content to compile HTML from
        :type content: MDContent
        :param is_absolute: decides whether absolute or relative path will be used
        :type is_absolute: bool
        """
        text = content.mdcontent.textfield
        if content.ImageAttachments.count() > 0:
            attachments = content.ImageAttachments.all()
            for idx, attachment in enumerate(attachments):
                if is_absolute:
                    path = ret_path(attachment.image.url)
                else:
                    path = attachment.image.url
                text = re.sub(rf"!\[(.*?)]\(Image-{idx}(.*?)\)",
                              rf"![\1]({path}\2)",
                              text)
        md_instance = (
            MarkdownIt()
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .enable('table')
            .enable('strikethrough')
            .enable('linkify')
        )
        return md_instance.render(text)


class Latex:
    """LaTeX Export

    This class takes care of the export and rendering of LaTeX code. The encoding of the LaTeX
    file will be defined next to the error template name and the prefix of the error in the
    logs which can be extracted by finding the prefix.

    :attr Latex.encoding: The file encoding
    :type Latex.encoding: str
    :attr Latex.error_prefix: The error prefix character to find the error message in the logs
    :type Latex.error_prefix: str
    :attr Latex.error_template: The name of the error template
    :type Latex.error_template: str
    """
    encoding = 'utf-8'
    error_prefix = '!'
    error_template = 'error'

    @staticmethod
    def render(context, template_name):
        # pylint: disable=too-many-locals
        # pylint: disable=consider-using-with
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
        :rtype: tuple[bytes, tuple[bytes, bytes], str]
        """
        template = get_template(template_name)
        rendered_tpl = template.render(context).encode(Latex.encoding)

        with tempfile.TemporaryDirectory() as tempdir:
            if 'preview_data' in context:
                formset = context['image_formset']
                rendered_tpl += Latex.preview_prerender(context['preview_data'], formset, tempdir)
            else:
                # Options for wkhtmltopdf
                options = {
                    '--enable-local-file-access': '',
                    'margin-top': '2cm',
                    'margin-right': '1cm',
                    'margin-bottom': '2cm',
                    'margin-left': '1cm'
                }
                # Prerender content templates
                for content in context['contents']:
                    rendered_tpl += Latex.pre_render(content, context['export_pdf'])
                    if content.type == 'MD':
                        # Convert Markdown to HTML to PDF to put into export file
                        md_string = ''
                        if context['export_pdf']:
                            # File header
                            md_string += f"<meta charset='UTF-8'>" \
                                  f"<h2><span style=\"font-weight:bold\">{content.topic.title}" \
                                  + "</span></h2><i>" \
                                  + gettext("Description") \
                                  + f":</i> {tex_escape(content.description)}"
                        md_string += Markdown.render(content, True)
                        pdf = pdfkit.from_string(md_string, options=options)
                        name = f'MD_{content.pk}.pdf'
                        md_path = os.path.join(tempdir, name)
                        with open(md_path, 'wb') as temp_pdf:
                            temp_pdf.write(pdf)
                            temp_pdf.close()
                rendered_tpl += r"\end{document}".encode(Latex.encoding)
            # Have to compile 2 times for table of contents to work
            for i in range(0, 2 if context['export_pdf'] else 1):
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
                                                 Latex.error_template, False)
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

        Checks the given log (stdout) if there are error messages and returns the
        messages. If there are none, an empty list will be returned.

        :param lob: The bytes representing the LaTeX compile log
        :type lob: bytes

        :return: the error messages from the log
        :rtype: list[str]
        """
        # Decode bytes to string and split the string by the delimiter '\n'
        lines = lob.decode(Latex.encoding, errors='ignore').splitlines()
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
    def pre_render(content, export_flag, template_type=None, no_error=True):
        """Pre render

        Pre renders the given content and its corresponding template. If there
        is no template specified, the template will associated with the type
        of the content. Additional there are two flags, which indicates if
        a course or a content should be exported and if there exists errors
        while rendering the LaTeX code.

        If there are no errors, we can include the attachments to the pdf and
        replace the placeholders with the actual path to the images. Else
        we will render the error (log).

        :param content: The content to be rendered
        :type content: any
        :param export_flag: True if export, False if simple content compilation
        :type export_flag: bool
        :param template_type: The type of the template to use
        :type template_type: str
        :param no_error: Indicator if we are rendering a non error content
        :type no_error: bool

        :return: the rendered template
        :rtype: bytes
        """
        if template_type is None:
            template = get_template(export_template(content.type))
        else:
            template = get_template(export_template(template_type))

        # Set context for rendering
        # Set value for preview_flag to avoid error when rendering template for LaTeX
        context = {'content': content, 'export_pdf': export_flag, 'preview_flag': False}
        if no_error:
            if content.description == '':
                context['no_desc'] = True
            else:
                context['no_desc'] = False
        if no_error and content.type == 'YouTubeVideo':

            context['startTime'] = content.ytvideocontent.start_time
            context['endTime'] = content.ytvideocontent.end_time

            total_hours, total_minutes, total_seconds = \
                seconds_to_time(get_video_length(content.ytvideocontent.id))

            context['length'] = time_to_string(total_hours, total_minutes, total_seconds)

        # render the template and use escape for triple braces with escape character ~~
        # this is relevant when using triple braces for file paths in tex data
        if no_error and content.type == 'MD':
            context['md_path'] = f'MD_{content.pk}.pdf'
        rendered_tpl = template.render(context)
        rendered_tpl = re.sub('{~~', '{', rendered_tpl)
        # Check that we are not compiling an error template (otherwise the content would be an int)
        if no_error:
            # If there exists an attachment, replace all placeholders in the tex file with
            # image path
            if content.ImageAttachments.count() > 0:
                attachments = content.ImageAttachments.all()
                for idx, attachment in enumerate(attachments):
                    path = ret_path(attachment.image.url)
                    rendered_tpl = re.sub(rf"\\includegraphics(\[.*])?{{Image-{idx}}}",
                                          rf"\\includegraphics\1{{{path}}}",
                                          rendered_tpl)
        # Encode the template with Latex Encoding
        return rendered_tpl.encode(Latex.encoding)

    @staticmethod
    def preview_prerender(text, formset, directory=None, template_type='Latex'):
        """Prerender data for previewing
        Pre renders the given LaTeX data for the purpose of generating a preview data
        of the LaTeX.
        Also prepares all the attachments needed for the LaTeX content and saves them in the
        provided (optional) directory. Usually this directory is the one where the LaTeX
        compiling process is run. If the directory is not provided, the attachments won't be
        saved into the directory; the code will still be pre rendered.
        Uses the same template for pre rendering normal LaTeX content (i.e. content that will
        be saved to server) but does not use the same context for rendering.
        This method is created with the intention of pre rendering a preview for only LaTeX
        content.

        :param text: LaTeX data to pre render
        :type text: str
        :param formset: valid special image formset containing all the image attachments
                        of the content
        :type formset: LatexPreviewImageAttachmentFormSet
        :param directory: directory to save the attachments to
        :type directory: str or None
        :param template_type: type of the template to use
        :type template_type: str
        """
        template = get_template(export_template(template_type))
        # Set context for rendering
        context = {'preview_flag': True, 'latex_data': text, 'export_pdf': False}
        # render the template and use escape for triple braces with escape character ~~
        # this is relevant when using triple braces for file paths in tex data
        rendered_tpl = template.render(context)
        rendered_tpl = re.sub('{~~', '{', rendered_tpl)
        # formset should already be valid at this point so this check might not be necessary
        if formset.is_valid():
            # Replace all placeholders with image path
            # The images are all located inside the temporary directory where the PDF is compiled
            # so the image path only needs to contain image name
            for idx, form in enumerate(formset):
                used_form = form.save(commit=False)
                attachment = used_form.image
                # If the attachment is already saved in the server then just use it
                if '/' in attachment.name:
                    name = ret_path(attachment.url)
                else:
                    name = f'{idx}_{os.path.basename(attachment.name)}'
                    if directory is not None:
                        # Temporarily save attachment in directory
                        temp_path = os.path.join(directory, name)
                        with open(temp_path, 'wb') as temp_attachment:
                            # Save the attachment to tempdir in chunks
                            # so that memory is not overloaded
                            for chunk in attachment.chunks():
                                temp_attachment.write(chunk)
                            temp_attachment.close()
                rendered_tpl = re.sub(rf"\\includegraphics(\[.*])?{{Image-{idx}}}",
                                      rf"\\includegraphics\1{{{name}}}",
                                      rendered_tpl)
        rendered_tpl += r"\end{document}"
        return rendered_tpl.encode(Latex.encoding)
