"""Purpose of this file

This file contains functions related to generating views.
"""

from django.http import HttpResponse
from django.shortcuts import render
from django.utils.translation import gettext_lazy as _

from base.models import Course, Favorite, Content
from export.helper_functions import Latex


def pdf_compile(request, pk, exp_all,  # pylint: disable=invalid-name
                        template="content/export/base.tex",
                        context=None):
    """Generate course book

    Generates a PDF file with name tags for students in the queryset. There is also
    a flag which indicates if the whole core or only the coursebook should be
    exported.

    :param request: The given request
    :type request: WSGIRequest
    :param pk: The primary key of the course
    :type pk: int
    :param exp_all: Indicator if the whole course or the course book should be exported
    :type exp_all: bool
    :param template: The path of the LaTeX template to use
    :type template: str
    :param context: The context of the content
    :type context: dict[str, Any]

    :return: the generated coursebook as PDF, PDF LaTeX output and as an rendered template
    :rtype: tuple[bytes, tuple[bytes, bytes], str]
    """

    if context is None:
        context = {}
    user = request.user
    course = Course.objects.get(pk=pk)

    # Set Context
    context['user'] = user
    context['course'] = course
    context['export_pdf'] = True
    context['contents'] = []

    # Check if we want to export the whole course or only the coursebook
    if exp_all:
        for topic in course.topics.all():
            contents = list(Content.objects.filter(topic=topic))
            for content in contents:
                context['contents'].append(content)
    else:
        context['contents'] = [
            favorite.content
            for favorite in
            Favorite.objects.filter(user=user.profile, course=course)
        ]

    # Perform compilation given context and template
    (pdf, pdflatex_output, tex_template) = Latex.render(context, template, [])
    return pdf, pdflatex_output, tex_template


def generate_coursebook_response(request, pk, file_name=_("Coursebook")):  # pylint: disable=invalid-name
    """Generate course book response

    Generates a PDF file with name tags for students in the queryset and sends it to the browser.
    This method generates a pdf file for the coursebook content (coursebook export)

    :param request: The given request
    :type request: WSGIRequest
    :param pk: The primary key of the course
    :type pk: int
    :param file_name: The name of the file
    :type file_name: str

    :return: the http response of the generated PDF file
    :rtype: HttpResponse
    """

    # Call the method for coursebook generation and write the output afterwards
    (pdf, pdflatex_output, tex_template) = pdf_compile(request, pk, False)
    return write_response(request, pdf, pdflatex_output, tex_template, file_name + ".pdf")


def generate_course_export_response(request, pk, file_name=_("Course_Export")):  # pylint: disable=invalid-name
    """
    Generates a PDF file with name tags for students in the queryset and sends it to the browser.
    This method generates a PDF for all contents in a course (course export)

    :param request: The given request
    :type request: WSGIRequest
    :param pk: The primary key of the course
    :type pk: int
    :param file_name: The name of the file
    :type file_name: str

    :return: the http response of the generated PDF file
    :rtype: HttpResponse
    """

    # Call the method for coursebook generation and write the output afterwards
    (pdf, pdflatex_output, tex_template) = pdf_compile(request, pk, True)
    return write_response(request, pdf, pdflatex_output, tex_template, file_name + ".pdf")


def write_response(request, pdf, pdflatex_output, tex_template, filename,
                   content_type='application/pdf'):
    """Write response

    Renders a pdf and sends it to the browser.

    :param request: The given request
    :type request: WSGIRequest
    :param pdf: The PDF
    :type pdf: bytes
    :param pdflatex_output: The PDF LaTeX output
    :type pdflatex_output: tuple[bytes, bytes]
    :param tex_template: The rendered template
    :type tex_template: str
    :param filename: The name of the file
    :type filename: str
    :param content_type: The type of the content (file)
    :type content_type: str

    :return: the http response of the written file
    :rtype: HttpResponse
    """
    if not pdf:
        return render(request,
                      "frontend/coursebook/rendering-error.html",
                      {"content": pdflatex_output[0].decode("utf-8"),
                       "tex_template": tex_template.decode("utf-8")})
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response.write(pdf)
    return response


def generate_pdf_from_latex(user, content, template="content/export/base.tex", context=None):
    """Generate PDF

    Generates a PDF file with name tags for students in the queryset.
    This method is used to compile a specific latex content into a PDF.

    :param user: The user of the content
    :type user: User
    :param content: The content of the PDF
    :type content: Content
    :param template: The path of the LaTeX template to use
    :type template: str
    :param context: The context of the content
    :type context: dict[str, Any]

    :return: the generated PDF as PDF, PDF LaTeX output and its rendered template
    :rtype: tuple[bytes, tuple[bytes, bytes], str]
    """
    if context is None:
        context = {}

        # Set Context
    context['user'] = user
    context['topic'] = content.topic
    context['contents'] = [content]
    context['export_pdf'] = False

    # Performs compilation given context and template
    (pdf, pdflatex_output, tex_template) = Latex.render(context, template, [])
    return pdf, pdflatex_output, tex_template


def generate_pdf_response(user, content):
    """Generate pdf response

    Generates a PDF file with name tags for students in the queryset.
    This method compiles a specific latex content into a PDF.

    :param user: The user of the content
    :type user: User
    :param content: The content of the pdf
    :type content: Content

    return: the generated PDF
    rtype: bytes
    """

    # Calls the function for generating the pdf and return the pdf
    pdf = generate_pdf_from_latex(user, content)
    return pdf[0]
