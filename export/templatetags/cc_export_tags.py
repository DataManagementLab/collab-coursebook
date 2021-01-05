import os
import re

from django import template
from django.template.defaultfilters import stringfilter
from content.models import CONTENT_TYPES
import content

register = template.Library()


@register.filter
def export_template(type):
    base_path = os.path.dirname(content.__file__)
    path = base_path + f"/templates/content/export"
    # Error check for latex
    if type in CONTENT_TYPES.keys() or type == 'error':
        return path + f"/{type}.tex"
    return path + "/invalid.tex"


@register.filter
@stringfilter
def tex_escape(value):
    """Escape characters with special meaning in LaTeX.
    https://github.com/d120/pyophase/blob/master/ophasebase/templatetags/tex_escape.py
    retrieved: 10.08.2020
    """
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
