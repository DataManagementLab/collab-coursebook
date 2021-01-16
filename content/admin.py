"""Purpose of this file

This file describes the available content type in the admin panel. The contents are ordered alphabetically. This can
be found in the Content section of the admin panel. Contents can be added to or modified for the various content
types.
"""

from django.contrib import admin

from content.models import ImageAttachment, ImageContent, Latex, PDFContent, SingleImageAttachment, TextField, YTVideoContent


@admin.register(ImageAttachment)
class ImageAttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageContent)
class ImageContentAdmin(admin.ModelAdmin):
    pass


@admin.register(Latex)
class LatexAdmin(admin.ModelAdmin):
    pass


@admin.register(PDFContent)
class PdfContentAdmin(admin.ModelAdmin):
    pass


@admin.register(SingleImageAttachment)
class SingleImageAttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(TextField)
class TextFieldAdmin(admin.ModelAdmin):
    pass


@admin.register(YTVideoContent)
class YTVideoContentAdmin(admin.ModelAdmin):
    pass
