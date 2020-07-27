import os
from pathlib import Path

from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

from base.models import Course
from base.models.coursebook import Favorite
from content.models import CONTENT_TYPES


def generate_coursebook(request, *args, **kwargs):
    course_id = kwargs['pk']
    course = Course.objects.get(pk=course_id)
    user = request.user

    generated_file_path = generate_coursebook_for(user, course)
    pdf_file_path = generated_file_path + '.pdf'
    if Path(pdf_file_path).exists():
        with open(pdf_file_path, 'rb') as file_handler:
            response = HttpResponse(file_handler.read(), content_type="application/pdf")
            file_handler.close()
        return response
    messages.error(request, 'There was an error while generating your coursebook.')
    return HttpResponseRedirect(reverse('frontend:course', args=(course_id, )))


def generate_coursebook_for(user, course):
    file_directory = os.path.join(settings.BASE_DIR, "media", "coursebooks")
    filename = "Coursebook_" + str(user) + "_" + str(course)
    file_path = os.path.join(file_directory, filename)

    if not os.path.exists(file_directory):
        os.makedirs(file_directory)

    latex_document_string = generate_latex_head(course.title, user)

    # TODO: latex section for each topic

    for favorite in Favorite.objects.filter(user=user.profile, course=course):
        content = favorite.content
        content_type = content.type
        if content_type in CONTENT_TYPES:
            content_type_object = CONTENT_TYPES.get(content_type).objects.get(pk=content.pk)
            latex_document_string += content_type_object.generate_latex_template()
        else:
            latex_document_string += generate_latex_invalid_content_type(content_type)

    latex_document_string += generate_latex_end()

    with open(file_path + '.tex', 'w+') as file:
        file.write(latex_document_string)
        file.close()

    bash_convert = "pdflatex -no-file-line-error -halt-on-error -output-directory='" + \
                   file_directory + "' " \
                   + file_path + ".tex"
    bash_quiet = " > /dev/null"  # Quiet output in the shell
    os.system(bash_convert + bash_quiet)  # run as shell command

    os.remove(file_path + ".tex")
    os.remove(file_path + ".aux")
    os.remove(file_path + ".log")
    os.remove(file_path + ".out")

    return file_path


def generate_latex_head(title, author):
    return r"""\documentclass{article}
        \usepackage[T1]{fontenc}
        \usepackage[utf8]{inputenc}
        \usepackage{graphicx}
        \usepackage{float}
        \usepackage{grffile}
        \usepackage{hyperref}
    
        \title{""" + str(title) + r""" - Coursebook}
        \author{""" + str(author) + r"""}
        \date{\today}
    
        \begin{document}
        \maketitle
        """


def generate_latex_end():
    return r"""\end{document}"""


def generate_latex_invalid_content_type(type):
    return r"""\textit{This type of content is not supported and cannot be displayed: """ + str(type) + """}"""
