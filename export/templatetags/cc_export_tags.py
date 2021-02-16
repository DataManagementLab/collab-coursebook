"""Purpose of this file

This file describes the configuration of exports including the templates
and if necessary the escape characters.
"""

import os

import re

from django import template
from django.template.defaultfilters import stringfilter

from collab_coursebook.settings import BASE_DIR

from content.models import CONTENT_TYPES

import content

register = template.Library()


@register.filter
def export_template(content_type):
    """Export template

    Validate the type and retrieve the suitable template.

    :param content_type: The content type or error
    :type content_type: str

    returns: the path of the template
    rtype: str
    """
    base_path = os.path.dirname(content.__file__)
    path = base_path + "/templates/content/export"

    # Type must be a content type or the error type for an invalid latex compilation
    if content_type in CONTENT_TYPES.keys() or content_type == 'error':
        return path + f"/{content_type}.tex"
    return path + "/invalid.tex"


@register.filter
def ret_path(value):
    """Return path to image

    Returns the correct (absolute) path to the image in media directory.

    :param value: The path
    :type value: str

    :return: the absolute path to the image in media directory
    :rtype: str
    """

    # Compute the path to the image and escape \ for LaTeX
    path = os.path.join(os.path.abspath(BASE_DIR), value[1:])
    return path.replace('\\', '/')


@register.filter
@stringfilter
def tex_escape(value):
    """Escape characters

    Defines the escape characters with special meaning in LaTeX and replace them.

    https://github.com/d120/pyophase/blob/master/ophasebase/templatetags/tex_escape.py
    Retrieved: 10.08.2020

    :param value: The LaTeX code to be escaped
    :type value: str

    :return: the escaped LaTeX code
    :rtype: str
    """

    # dict[str, str]: Replacements - Escape characters
    replacements = {
        '&': r'\&',
        '%': r'\%',
        '$': r'\$',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde{}',
        '^': r'\^{}',
        '\\': r'\textbackslash{}',
        '<': r'\textless{}',
        '>': r'\textgreater{}',
        '\n': r'\newline '
    }

    regex = re.compile('|'.join(re.escape(key) for key in replacements))
    return regex.sub(lambda match: replacements[match.group()], value)
