"""Purpose of this file

This file describes the validators needed for the views.
"""
from django.core.files.base import ContentFile

from export.views import generate_pdf_response


class Validator:
    """Validator

    Handles all validation related operation related to views.
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
        pdf = generate_pdf_response(user, content)
        latex_content.pdf.save(f"{content.topic}" + ".pdf", ContentFile(pdf))
        latex_content.save()

    @staticmethod
    def validate_attachment(view, attachment_form, image_formset, content_obj):
        """Validate attachment

        Validates the image attachments and stores them into the database.

        :param view: The view that wants to validate the data
        :type view: View
        :param attachment_form: The attachment form
        :type attachment_form: ModelForm
        :param image_formset: The image form set
        :type image_formset: BaseModelFormSet
        :param content_obj: The content
        :type content_obj: Content

        :return: the redirection to the invalid page if the image form set or
        the attachment form is not valid
        :rtype: None | HttpResponseRedirect
        """
        if attachment_form.is_valid():
            # Evaluates the attachment form
            content_attachment = attachment_form.save(commit=False)
            content_attachment.save()
            content_obj.attachment = content_attachment
            images = []
            # Evaluates all forms of the formset and append to image set
            if image_formset.is_valid():
                for form in image_formset:
                    used_form = form.save(commit=False)
                    used_form.save()
                    images.append(used_form)
            else:
                return view.form_invalid(image_formset)

            # Stores the attached images in DB
            content_obj.attachment.images.set(images)
            return None

        return view.form_invalid(attachment_form)
