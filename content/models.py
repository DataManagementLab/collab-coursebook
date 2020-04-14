from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import Content


class YTVideoContent(models.Model):
    TYPE = "YouTubeVideo"
    DESC = _("YouTube Video")

    class Meta:
        verbose_name = _("YouTube Video Content")
        verbose_name_plural = _("YouTube Video Contents")

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)
    url = models.URLField(verbose_name=_("Video URL"))

    def __str__(self):
        return f"{self.DESC}: {self.url}"


class ImageContent(models.Model):
    TYPE = "Image"
    DESC = _("Single Image")

    class Meta:
        verbose_name = _("Image Content")
        verbose_name_plural = _("Image Contents")

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(verbose_name=_("Image"), upload_to='uploads/contents/%Y/%m/%d/')
    source = models.TextField(verbose_name=_("Source"))
    license = models.CharField(verbose_name=_("Licence"), blank=True, max_length=200)

    def __str__(self):
        return f"{self.content}: {self.image}"


CONTENT_TYPES = {
    YTVideoContent.TYPE: YTVideoContent,
    ImageContent.TYPE: ImageContent,
}