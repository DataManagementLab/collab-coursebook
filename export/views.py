"""Purpose of this file

This file contains functions related to generating views.
"""

from django.http import HttpResponse
from django.shortcuts import render

from base.models import Course, Favorite
from export.helper_functions import LaTeX


def generate_coursebook(request, pk, template="content/export/base.tex", context=None):
    """Generate course book

    Generates a PDF file with name tags for students in the queryset.

    Parameters:
        request (WSGIRequest): TODO
        pk (TODO):
        template (str): The template latex path
        context (dict): The context of the content

    return: the PDF, PDF LaTeX output and the rendered template
    rtype: Tuple[bytes, Tuple[bytes, bytes], str]
    """

    if context is None:
        context = {}
    user = request.user
    course = Course.objects.get(pk=pk)

    # Set Context
    context['user'] = user
    context['course'] = course
    context['contents'] = [
        favorite.content for favorite in Favorite.objects.filter(user=user.profile, course=course)]
    context['export_pdf'] = True

    # Perform compilation given context and template
    (pdf, pdflatex_output, tex_template) = LaTeX.render(context, template, [])
    return pdf, pdflatex_output, tex_template


def generate_coursebook_response(request, pk, filename='coursebook.pdf'):
    """Generate course book response

    Generates a PDF file with name tags for students in the queryset and sends it to the browser.

    Parameters:
        request (WSGIRequest): TODO
        pk (TODO):
        filename (str): The name of the file

    return: the http response of the generated PDF file
    rtype: HttpResponse
    """

    # Call the method for coursebook generation and write the output afterwards
    (pdf, pdflatex_output, tex_template) = generate_coursebook(request, pk)
    return write_response(request, pdf, pdflatex_output, tex_template, filename)


def write_response(request, pdf, pdflatex_output, tex_template, filename,
                   content_type='application/pdf'):
    """Write response

    Renders a pdf and sends it to the browser.

    Parameters:
        request (WSGIRequest): TODO
        pdf : The PDF
        pdflatex_output : PDF LaTeX output
        tex_template (str): The rendered template
        filename (str): The name of the file
        content_type (str): The type of the content
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


def generate_pdf(user, topic, content, template="content/export/base.tex", context=None):
    """Generate PDF

    Generates a PDF file with name tags for students in the queryset.

    Parameters:
        user (User): The user of the content
        topic (Topic): The topic the content belongs to
        content (dict): The content
        template (str): The path of the LaTeX template
        context (dict): The context of the content

    return: the PDF, PDF LaTeX output and the rendered template
    rtype: Tuple[bytes, Tuple[bytes, bytes], str]
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

    Parameters:
        user (User): The user of the content
        topic (Topic): The topic the content belongs to
        content (dict): The content

    return: the generated PDF
    rtype: bytes
    """

    # Calls the function for generating the pdf and return the pdf
    (pdf, pdflatex_output, tex_template) = generate_pdf(user, topic, content)
    return pdf
