"""Purpose of this file

This file contains functions related to generating views.
"""

from django.http import HttpResponse
from django.shortcuts import render

from base.models import Course, Favorite

from export.helper_functions import LaTeX


def generate_coursebook(request, primary_key, template="content/export/base.tex", context=None):
    """Generate course book

    Generates a PDF file with name tags for students in the queryset.

    :param request: The given request
    :type request: WSGIRequest
    :param primary_key: The primary key of the course
    :type primary_key: int
    :param template: The template latex path
    :type template: str
    :param context: The context of the content
    :type context: dict:

    :return: the PDF, PDF LaTeX output and the rendered template
    :rtype: Tuple[bytes, Tuple[bytes, bytes], str]
    """

    if context is None:
        context = {}
    user = request.user
    course = Course.objects.get(pk=primary_key)

    # Set Context
    context['user'] = user
    context['course'] = course
    context['contents'] = [
        favorite.content for favorite in Favorite.objects.filter(user=user.profile, course=course)]
    context['export_pdf'] = True

    # Perform compilation given context and template
    (pdf, pdflatex_output, tex_template) = LaTeX.render(context, template, [])
    return pdf, pdflatex_output, tex_template


def generate_coursebook_response(request, primary_key, file_name='coursebook.pdf'):
    """Generate course book response

    Generates a PDF file with name tags for students in the queryset and sends it to the browser.

    :param request: The given request
    :type request: WSGIRequest
    :param primary_key: The primary key of the course
    :type primary_key: int
    :param file_name: The name of the file
    :type file_name: str

    :return: the http response of the generated PDF file
    :rtype: HttpResponse
    """

    # Call the method for coursebook generation and write the output afterwards
    (pdf, pdflatex_output, tex_template) = generate_coursebook(request, primary_key)
    return write_response(request, (pdf, pdflatex_output, tex_template), file_name)


def write_response(request, pdf, filename,
                   content_type='application/pdf'):
    """Write response

    Renders a pdf and sends it to the browser.

    :param request: The given request
    :type request: WSGIRequest
    :param pdf : The PDF, PDF LaTeX output and the rendered template
    :type pdf: Tuple[bytes, Tuple[bytes, bytes], str]
    :param filename: The name of the file
    :type filename: str
    :param content_type: The type of the content
    :type content_type: str

    :return: the http response of the written file
    :rtype: HttpResponse
    """
    pdflatex_output = pdf[1]
    tex_template = pdf[2]
    if not pdf:
        return render(request,
                      "frontend/coursebook/rendering-error.html",
                      {"content": pdflatex_output[0].decode("utf-8"),
                       "tex_template": tex_template.decode("utf-8")})
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; file_name=' + filename
    response.write(pdf)
    return response


def generate_pdf(user, topic, content, template="content/export/base.tex", context=None):
    """Generate PDF

    Generates a PDF file with name tags for students in the queryset.

    :param user: The user of the content
    :type user: User
    :param topic: The topic the content belongs to
    :type topic: Topic
    :param content: The content
    :type content: dict
    :param template: The path of the LaTeX template
    :type template: str
    :param context: The context of the content
    :type context: dict

    :return: the PDF, PDF LaTeX output and the rendered template
    :rtype: Tuple[bytes, Tuple[bytes, bytes], str]
    """
    if context is None:
        context = {}

    # Set Context
    context['user'] = user
    context['topic'] = topic
    context['contents'] = [content]
    context['export_pdf'] = False

    # Performs compilation given context and template
    (pdf, pdflatex_output, tex_template) = LaTeX.render(context, template, [])
    return pdf, pdflatex_output, tex_template


def generate_pdf_response(user, topic, content):
    """Generate pdf response

    Generates a PDF file with name tags for students in the queryset.

    :param user: The user of the content
    :type user: User
    :param topic: The topic the content belongs to
    :type topic: Topic
    :param content: The content
    :type content: dict

    :return: the generated PDF
    :rtype: bytes
    """

    # Calls the function for generating the pdf and return the pdf
    pdf = generate_pdf(user, topic, content)[0]
    return pdf
