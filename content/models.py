import os

from django.db import models
from django.utils.translation import gettext_lazy as _
from base.models import Content
from content.mixin import GeneratePreviewMixin
from pdf2image import convert_from_path, convert_from_bytes
from PIL import Image
from pdf2image.exceptions import (
    PDFInfoNotInstalledError,
    PDFPageCountError,
    PDFSyntaxError
)

from django.conf import settings


class YTVideoContent(models.Model):
    TYPE = "YouTubeVideo"
    DESC = _("YouTube Video")

    class Meta:
        verbose_name = _("YouTube Video Content")
        verbose_name_plural = _("YouTube Video Contents")

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)
    url = models.URLField(verbose_name=_("Video URL"))

    def generate_preview(self):
        return

    @property
    def id(self):
        return self.url.split("=")[1]

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
    license = models.CharField(verbose_name=_("License"), blank=True, max_length=200)

    def __str__(self):
        return f"{self.content}: {self.image}"

    def generate_preview(self):
        # TODO generate small image previews
        return


class ImageAttachment(models.Model):
    TYPE = "Image Attachment"
    DESC = _("Single Image Attachment")

    class Meta:
        verbose_name = _("Image Attachment in Content")
        verbose_name_plural = _("Image Attachments in Content")

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)
    image = models.ImageField(verbose_name=_("Image Attachment"), upload_to='uploads/contents/%Y/%m/%d/')

    def __str__(self):
        return f"{self.content}: {self.image}"


class PdfContent(models.Model, GeneratePreviewMixin):
    TYPE = "Pdf"
    DESC = _("Pdf")

    class Meta:
        verbose_name = _("Pdf Content")
        verbose_name_plural = _("Pdf Contents")

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)
    content = None
    pdf = models.FileField(verbose_name=_("Pdf"), upload_to='uploads/contents/%Y/%m/%d/')
    source = models.TextField(verbose_name=_("Source"))
    license = models.CharField(verbose_name=_("License"), blank=True, max_length=200)

    def generate_preview(self):
        preview_folder = 'uploads/previews/'
        # Check if Folder exists
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, preview_folder)):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, preview_folder))
        base_filename = os.path.splitext(os.path.basename(self.pdf.name))[0] + '.jpg'
        # get images for every page
        pages = convert_from_path(self.pdf.path, last_page=2)
        # save first page to disk
        pages[0].save(os.path.join(settings.MEDIA_ROOT, preview_folder, base_filename))
        return os.path.join(preview_folder, base_filename)

    def __str__(self):
        return f"{self.content}: {self.pdf}"


CONTENT_TYPES = {
    YTVideoContent.TYPE: YTVideoContent,
    ImageContent.TYPE: ImageContent,
    PdfContent.TYPE: PdfContent,
    ImageAttachment.TYPE: ImageAttachment
}
