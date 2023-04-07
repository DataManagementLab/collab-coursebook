"""Purpose of this file

This file describes the available content type in the admin panel.
The contents are ordered alphabetically. This can be found in the
Content section of the admin panel. Contents can be added to or
modified for the various content types.
"""

from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from content.models import ImageContent, Latex
from content.models import PDFContent, TextField
from content.models import YTVideoContent
from content.models import MDContent

@admin.register(MDContent)
class MDContentAdmin(CompareVersionAdmin):
    """MD admin

    Represents the Markdown model in the admin panel.

    :attr MDContentAdmin.fields: Including fields into the form
    :type MDContentAdmin.fields: list[str]
    """


@admin.register(ImageContent)
class ImageContentAdmin(CompareVersionAdmin):  # pylint: disable=too-many-ancestors
    """Image content admin

    Represents the image content model in the admin panel.
    """


@admin.register(Latex)
class LatexAdmin(CompareVersionAdmin):  # pylint: disable=too-many-ancestors
    """LaTeX admin

    Represents the Latex model in the admin panel.

    :attr LatexAdmin.fields: Including fields into the form
    :type LatexAdmin.fields: list[str]
    """
    fields = ['content', 'textfield', 'source']


@admin.register(PDFContent)
class PDFContentAdmin(CompareVersionAdmin):  # pylint: disable=too-many-ancestors
    """PDF content admin

    Represents the PDF content model in the admin panel.
    """


@admin.register(TextField)
class TextFieldAdmin(CompareVersionAdmin):  # pylint: disable=too-many-ancestors
    """Text field admin

    Represents the text field model in the admin panel.
    """


@admin.register(YTVideoContent)
class YTVideoContentAdmin(CompareVersionAdmin):  # pylint: disable=too-many-ancestors
    """YouTube video content

    Represents the YouTube video content model in the admin panel.
    """
