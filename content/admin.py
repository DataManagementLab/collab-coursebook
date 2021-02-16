"""Purpose of this file

This file describes the available content type in the admin panel.
The contents are ordered alphabetically. This can be found in the
Content section of the admin panel. Contents can be added to or
modified for the various content types.
"""

from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from content.models import ImageAttachment, ImageContent, Latex
from content.models import PDFContent, SingleImageAttachment, TextField
from content.models import YTVideoContent


# pylint: disable=too-many-ancestors
@admin.register(ImageAttachment)
class ImageAttachmentAdmin(CompareVersionAdmin):
    """Image attachment admin

    Represents the image attachment model in the admin panel.
    """


# pylint: disable=too-many-ancestors
@admin.register(ImageContent)
class ImageContentAdmin(CompareVersionAdmin):
    """Image content admin

    Represents the image content model in the admin panel.
    """


# pylint: disable=too-many-ancestors
@admin.register(Latex)
class LatexAdmin(CompareVersionAdmin):
    """LaTeX admin

    Represents the Latex model in the admin panel.

    :attr LatexAdmin.fields: Including fields into the form
    :type LatexAdmin.fields: list[str]
    """
    fields = ['content', 'textfield', 'source']


# pylint: disable=too-many-ancestors
@admin.register(PDFContent)
class PDFContentAdmin(CompareVersionAdmin):
    """PDF content admin

    Represents the PDF content model in the admin panel.
    """


# pylint: disable=too-many-ancestors
@admin.register(SingleImageAttachment)
class SingleImageAttachmentAdmin(admin.ModelAdmin):
    """Singe Image attachment admin

    Represents the single image attachment model in the admin panel.
    """


# pylint: disable=too-many-ancestors
@admin.register(TextField)
class TextFieldAdmin(CompareVersionAdmin):
    """Text field admin

    Represents the text field model in the admin panel.
    """


# pylint: disable=too-many-ancestors
@admin.register(YTVideoContent)
class YTVideoContentAdmin(CompareVersionAdmin):
    """YouTube video content

    Represents the YouTube video content model in the admin panel.
    """
