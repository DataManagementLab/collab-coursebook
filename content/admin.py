"""Purpose of this file

This file describes the available content type in the admin panel.
The contents are ordered alphabetically. This can be found in the
Content section of the admin panel. Contents can be added to or
modified for the various content types.
"""

from django.contrib import admin

from content.models import ImageAttachment, ImageContent, Latex
from content.models import PDFContent, SingleImageAttachment, TextField
from content.models import YTVideoContent


@admin.register(ImageAttachment)
class ImageAttachmentAdmin(admin.ModelAdmin):
    """Image attachment admin

    Represents the image attachment model in the admin panel.
    """


@admin.register(ImageContent)
class ImageContentAdmin(admin.ModelAdmin):
    """Image content admin

    Represents the image content model in the admin panel.
    """


@admin.register(Latex)
class LatexAdmin(admin.ModelAdmin):
    """LaTeX admin

    Represents the LaTeX model in the admin panel.
    """


@admin.register(PDFContent)
class PDFContentAdmin(admin.ModelAdmin):
    """PDF content admin

    Represents the PDF content model in the admin panel.
    """


@admin.register(SingleImageAttachment)
class SingleImageAttachmentAdmin(admin.ModelAdmin):
    """Singe Image attachment admin

    Represents the single image attachment model in the admin panel.
    """


@admin.register(TextField)
class TextFieldAdmin(admin.ModelAdmin):
    """Text field admin

    Represents the text field model in the admin panel.
    """


@admin.register(YTVideoContent)
class YTVideoContentAdmin(admin.ModelAdmin):
    """YouTube video content

    Represents the YouTube video content model in the admin panel.
    """
