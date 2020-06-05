from django.contrib import admin

from content.models import YTVideoContent, ImageContent


@admin.register(YTVideoContent)
class YTVideoContentAdmin(admin.ModelAdmin):
    pass


@admin.register(ImageContent)
class ImageContentAdmin(admin.ModelAdmin):
    pass
