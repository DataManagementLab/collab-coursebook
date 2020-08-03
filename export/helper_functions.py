import os
from django.conf import settings
from base.models.coursebook import Favorite
from content.models import CONTENT_TYPES


def generate_coursebook_for(user, course):
    file_directory = os.path.join(settings.BASE_DIR, "media", "coursebooks")
    filename = "Coursebook_" + str(user) + "_" + str(course)
    file_path = os.path.join(file_directory, filename)

    if not os.path.exists(file_directory):
        os.makedirs(file_directory)

    latex_document_string = generate_latex_head(course.title, user)

    # sort contents by topic
    contents = [favorite.content for favorite in Favorite.objects.filter(user=user.profile, course=course)]
    contents = sorted(contents, key=lambda c: c.topic.title)

    # save the last topic to generate a new section for each topic
    last_topic = None
    for content in contents:
        content_type = content.type
        if last_topic != content.topic:
            last_topic = content.topic
            latex_document_string += generate_latex_section(content.topic.title)

        if content_type in CONTENT_TYPES:
            content_type_object = CONTENT_TYPES.get(content_type).objects.get(pk=content.pk)
            latex_document_string += content_type_object.generate_latex_template()
        else:
            latex_document_string += generate_latex_invalid_content_type(content_type)

    latex_document_string += generate_latex_end()

    # write data into tex file
    with open(file_path + '.tex', 'w+') as file:
        file.write(latex_document_string)
        file.close()

    # convert tex file into pdf
    bash_convert = "pdflatex -no-file-line-error -halt-on-error -output-directory='" + \
                   file_directory + "' " \
                   + file_path + ".tex"
    bash_quiet = " > /dev/null"  # Quiet output in the shell
    os.system(bash_convert + bash_quiet)  # run as shell command

    # remove unnecessary files to save space
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


def generate_latex_invalid_content_type(content_type):
    return r"""\textit{This type of content is not supported and cannot be displayed: """ + str(content_type) + """}"""


def generate_latex_section(title):
    return r"\section{" + str(title) + "}"
