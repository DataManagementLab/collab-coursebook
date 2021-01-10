from django.http import HttpResponse
from django.shortcuts import render

from base.models import Course, Favorite
from export.helper_functions import LaTeX


def generate_coursebook(request, pk, template="content/export/base.tex", context=None):
    """ Generates a PDF file with nametags for students in the queryset"""

    if context is None:
        context = {}
    user = request.user
    course = Course.objects.get(pk=pk)

    # Set Context
    context['user'] = user
    context['course'] = course
    context['contents'] = [favorite.content for favorite in Favorite.objects.filter(user=user.profile, course=course)]

    # Perform compilation given context and template
    (pdf, pdflatex_output, tex_template) = LaTeX.render(context, template, [])
    return pdf, pdflatex_output, tex_template


def generate_coursebook_response(request, pk, filename='coursebook.pdf'):
    """ Generates a PDF file with nametags for students in the queryset and sends it to the browser"""

    # Call the method for coursebook generation and write the output afterwards
    (pdf, pdflatex_output, tex_template) = generate_coursebook(request, pk)
    return write_response(request, pdf, pdflatex_output, tex_template, filename)


def write_response(request, pdf, pdflatex_output, tex_template, filename, content_type='application/pdf'):
    if not pdf:
        return render(request, "frontend/coursebook/rendering-error.html", {"content": pdflatex_output[0].decode("utf-8"), "tex_template": tex_template.decode("utf-8")})
    response = HttpResponse(content_type=content_type)
    response['Content-Disposition'] = 'attachment; filename=' + filename
    response.write(pdf)
    return response


def generate_pdf(user, course, content, template="content/export/base.tex", context=None):
    """ Generates a PDF file with nametags for students in the queryset"""

    if context is None:
        context = {}

    # Set Context
    context['user'] = user
    context['course'] = course
    context['contents'] = [content]

    # Perform compilation given context and template
    (pdf, pdflatex_output, tex_template) = LaTeX.render(context, template, [])
    return pdf, pdflatex_output, tex_template


def generate_pdf_response(user, course, content):
    """ Generates a PDF file with nametags for students in the queryset """

    # call the method for generating the pdf and return the pdf
    (pdf, pdflatex_output, tex_template) = generate_pdf(user, course, content)
    return pdf
