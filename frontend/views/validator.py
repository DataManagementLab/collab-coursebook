"""Purpose of this file

This file describes the validators needed for the views.
"""

from django.core.files.base import ContentFile

from export.views import generate_pdf_from_latex

import markdown


class Validator:
    """Validator

    This class handles all validation related operation related to views.
    """

    @staticmethod
    def validate_latex(user, content, latex_content):
        """Validate LaTeX

        Validates LateX and compiles the Latex code and stores its pdf into the database.

        :param user: The current user
        :type user: User
        :param content: The content of the pdf
        :type content: Content
        :param latex_content: The data of the content type
        :type latex_content: Latex
        """
        pdf = generate_pdf_from_latex(user, content)
        latex_content.pdf.save(f"{content.topic}" + ".pdf", ContentFile(pdf))
        latex_content.save()


#TODO outsource this to views and helper functions like the LaTeX function for reuseability
    @staticmethod
    def validate_md(user, content, md_content):
        """Validate Markdown

        Validates Markdown and compiles the Markdown Code and stores its html into the database.

        :param user: The current user
        :type user: User
        :param content: The content of the html
        :type content: Content
        :param md_content: The data of the content type
        :type md_content: MD
        """
        md_code = md_content.textfield
        html = markdown.markdown(md_code)
        md_content.html.save(f"{content.topic}"+ ".html", ContentFile(html))
        md_content.md.save(f"{content.topic}"+ ".md", ContentFile(md_code.encode('utf-8')))
        md_content.save()

    @staticmethod
    def validate_attachment(content, image_formset):
        """Validate attachment

        Validates the image attachments and stores them into the database.

        :param content: The view that wants to validate the data
        :type content: View
        :param image_formset: The image form set
        :type image_formset: BaseModelFormSet

        :return: the redirection to the invalid page if the image form set or
        the attachment form is not valid
        :rtype: None or HttpResponseRedirect
        """
        if image_formset.is_valid():
            for form in image_formset:
                used_form = form.save(commit=False)
                used_form.content = content
                used_form.save()
