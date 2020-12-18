from django.contrib import admin

from content.models import YTVideoContent, ImageContent, PdfContent, ImageAttachment


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
