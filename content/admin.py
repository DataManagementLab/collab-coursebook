from django.contrib import admin

from content.models import YTVideoContent, ImageContent, PdfContent, ImageAttachment, TextField, Latex, SingleImage


@admin.register(YTVideoContent)
class YTVideoContentAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageContent)
class ImageContentAdmin(admin.ModelAdmin):
    pass


@admin.register(PdfContent)
class PdfContentAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageAttachment)
class ImageAttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(TextField)
class TextFieldAdmin(admin.ModelAdmin):
    pass

@admin.register(Latex)
class LatexAdmin(admin.ModelAdmin):
    pass

@admin.register(SingleImage)
class ImageAdmin(admin.ModelAdmin):
    pass

