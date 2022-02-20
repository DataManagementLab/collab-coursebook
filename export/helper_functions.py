"""Purpose of this file

This file contains utility functions related to exporting and rendering files.
"""

import os
import re
import tempfile
import pdfkit
from markdown_it import MarkdownIt
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.footnote import footnote_plugin
from django.utils.translation import gettext
from subprocess import Popen, PIPE

from django.template.loader import get_template

from django.utils.translation import gettext_lazy as _

from export.templatetags.cc_export_tags import export_template, tex_escape, ret_path
from content.static.yt_api import *


class Markdown:
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
        md = (
            MarkdownIt()
            .use(front_matter_plugin)
            .use(footnote_plugin)
            .enable('table')
            .enable('strikethrough')
            .enable('linkify')
        )
        return md.render(text)


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
        if 'preview_data' not in context:
            for content in context['contents']:
                rendered_tpl += Latex.pre_render(content, context['export_pdf'])
            rendered_tpl += r"\end{document}".encode(Latex.encoding)

        with tempfile.TemporaryDirectory() as tempdir:
            if 'preview_data' in context:
                formset = context['image_formset']
                rendered_tpl += Latex.preview_prerender(context['preview_data'], formset)
                # This part can maybe be optimized because the same loop is used in preview_prerender
                # But then we would have to put tempdir as a parameter, which would make it unclear which
                # temporary directory is used?
                # formset should already be valid at this point so this check might not be necessary
                if formset.is_valid():
                    for idx, form in enumerate(formset):
                        used_form = form.save(commit=False)
                        attachment = used_form.image
                        # If the attachment is already saved in the server no need to write it in tempdir
                        if '/' not in attachment.name:
                            # Make each attachment's name unique to prevent files from being accidentally overwritten
                            name = f'{idx}_{os.path.basename(attachment.name)}'
                            temp_path = os.path.join(tempdir, name)
                            with open(temp_path, 'wb') as temp_attachment:
                                # Save the attachment to tempdir in chunks so that memory is not overloaded.
                                for chunk in attachment.chunks():
                                    temp_attachment.write(chunk)
                                temp_attachment.close()
            options = {
                '--enable-local-file-access': '',
                'margin-top': '2cm',
                'margin-right': '1cm',
                'margin-bottom': '2cm',
                'margin-left': '1cm'
            }
            for content in context['contents']:
                if content.type == 'MD':
                    md = ''
                    if context['export_pdf']:
                        md += f"<meta charset='UTF-8'>" \
                             f"<hr><h2><span style=\"font-weight:bold\">{content.topic.title}</span></h2><i>" \
                             + gettext("Description") + f":</i> {tex_escape(content.description)}"
                    md += Markdown.render(content, True)
                    pdf = pdfkit.from_string(md, options=options)
                    name = f'MD_{content.pk}.pdf'
                    path = os.path.join(tempdir, name)
                    with open(path, 'wb') as temp_pdf:
                        temp_pdf.write(pdf)
                        temp_pdf.close()

            # Use shell-escape to allow the package 'markdown' to access shell
            process = Popen(['pdflatex', '--shell-escape'], stdin=PIPE, stdout=PIPE, cwd=tempdir, )

            # Output is a byte tuple of stdout and stderr
            pdflatex_output = process.communicate(rendered_tpl)

            # Filter error messages in log (stdout)
            error_log = Latex.errors(pdflatex_output[0])
            print(error_log)
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
        # remove any temporary files
        md_dir = os.path.dirname(os.path.abspath(__file__))[:-7] + '/media/uploads/temp'
        if os.path.exists(md_dir):
            for temp in os.listdir(md_dir):
                os.remove(os.path.join(md_dir, temp))
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

        # for markdown files parse them to html, then create a temporary file with pdfkit and add the path to the context, remove all temporary files after
        '''
        if (no_error and content.type == 'MD'):
            # parse markdown to html
            if content.ImageAttachments.count() > 0:
                attachments = content.ImageAttachments.all()
                for idx, attachment in enumerate(attachments):
                    absolute = ret_path(attachment.image.url)
                    text = re.sub(rf"!\[(.*?)]\(Image-{idx}(.*?)\)",
                                  rf"![\1]({absolute}\2)",
                                  text)
            latex = md_to_html(content.mdcontent.textfield, content)
            context['mdtext'] = latex
        '''

        if no_error and content.type == 'YouTubeVideo':

            seconds_total = content.ytvideocontent.startTime
            context['start_hours'], context['start_minutes'], context['start_seconds'] = seconds_to_time(seconds_total)

            total_hours, total_minutes, total_seconds = seconds_to_time(get_video_length(content.ytvideocontent.id))

            seconds_total = content.ytvideocontent.endTime
            if (seconds_total == 0):
                context['end_hours'], context['end_minutes'], context[
                    'end_seconds'] = total_hours, total_minutes, total_seconds
            else:
                context['end_hours'], context['end_minutes'], context['end_seconds'] = seconds_to_time(seconds_total)

            len = ""
            if (total_hours > 0):
                len += f"{total_hours} " + _("Hours")
                if (total_minutes or total_seconds > 0): len += ", "
            if (total_minutes > 0):
                len += f"{total_minutes} " + _("Minutes")
                if (total_seconds > 0): len += ", "
            if ((total_seconds > 0) or total_hours and total_minutes == 0): len += f"{total_seconds} " + _("Seconds")

            context['length'] = len

        # render the template and use escape for triple braces with escape character ~~
        # this is relevant when using triple braces for file paths in tex data
        context['test'] = ret_path('/media/uploads/temps/test.pdf')
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
                # md = content.mdcontent.textfield
                for idx, attachment in enumerate(attachments):
                    path = ret_path(attachment.image.url)
                    if content.type == 'MD':
                        '''rendered_tpl = re.sub(rf"!\[(.*?)]\(Image-{idx}(.*?)\)",
                                              rf"![\1]({path}\2)",
                                              rendered_tpl)
                        md = re.sub(rf"!\[(.*?)]\(Image-{idx}(.*?)\)",
                                              rf"![\1]({path}\2)",
                                              md)'''
                    else:
                        rendered_tpl = re.sub(rf"\\includegraphics(\[.*])?{{Image-{idx}}}",
                                              rf"\\includegraphics\1{{{path}}}",
                                              rendered_tpl)
                '''md = markdown.markdown(md)
                options = {
                    '--enable-local-file-access': ''
                }
                pdf = pdfkit.from_string(md, options=options)
                with open(ret_path('/media/uploads/temps/test.pdf'),'wb') as f:
                    f.write(pdf)
                    f.close()
                '''

        # Encode the template with Latex Encoding
        return rendered_tpl.encode(Latex.encoding)

    @staticmethod
    def preview_prerender(text, formset, template_type='Latex'):
        """Prerender data for previewing
        Pre renders the given LaTeX data for the purpose of generating a preview data
        of the LaTeX.
        Uses the same template for pre rendering normal LaTeX content (i.e content that will be
        saved to server) but does not use the same context for rendering.
        This method is created with the intention of pre rendering a preview for only LaTeX content.

        :param text: LaTeX data to pre render
        :type text: str
        :param formset: valid special image formset containing all the image attachments of the content
        :type formset: LatexPreviewImageAttachmentFormSet
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
                name = used_form.image.name
                # If the attachment is already saved in the server then just use it.
                if '/' in name:
                    name = ret_path(used_form.image.url)
                else:
                    name = f'{idx}_{used_form.image.name}'
                rendered_tpl = re.sub(rf"\\includegraphics(\[.*])?{{Image-{idx}}}",
                                      rf"\\includegraphics\1{{{name}}}",
                                      rendered_tpl)
        rendered_tpl += r"\end{document}"
        return rendered_tpl.encode(Latex.encoding)
