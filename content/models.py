import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import Content

from content.mixin import GeneratePreviewMixin

from pdf2image import convert_from_path


class BaseModel(models.Model):
    class Meta:
        abstract = True

    def generate_preview(self):
        return


class BaseContentModel(BaseModel):
    class Meta:
        abstract = True

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)


class BasePDFModel(BaseModel, GeneratePreviewMixin):
    class Meta:
        abstract = True

    pdf = models.FileField(verbose_name=_("Pdf"), upload_to='uploads/contents/%Y/%m/%d/', blank=True)

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


class BaseSourceModel(BaseModel):
    class Meta:
        abstract = True

    source = models.TextField(verbose_name=_("Source"))
    license = models.CharField(verbose_name=_("License"), blank=True, max_length=200)


class YTVideoContent(BaseContentModel):
    TYPE = "YouTubeVideo"
    DESC = _("YouTube Video")

    class Meta:
        verbose_name = _("YouTube Video Content")
        verbose_name_plural = _("YouTube Video Contents")

    url = models.URLField(verbose_name=_("Video URL"))

    @property
    def id(self):
        return self.url.split("=")[1]

    def __str__(self):
        return f"{self.DESC}: {self.url}"


class ImageContent(BaseContentModel, BaseSourceModel):
    TYPE = "Image"
    DESC = _("Single Image")

    class Meta:
        verbose_name = _("Image Content")
        verbose_name_plural = _("Image Contents")

    image = models.ImageField(verbose_name=_("Image"), upload_to='uploads/contents/%Y/%m/%d/')

    def __str__(self):
        return f"{self.content}: {self.image}"


class SingleImage(BaseModel):
    TYPE = "SingleImage"
    DESC = _("Single Image")

    class Meta:
        verbose_name = _("Single Image")
        verbose_name_plural = _("Single Images")

    image = models.ImageField(verbose_name=_("Attached Image"), upload_to='uploads/contents/%Y/%m/%d/')

    def __str__(self):
        return f"{self.image}"



class ImageAttachment(BaseSourceModel):
    TYPE = "ImageAttachment"
    DESC = _("Single Image Attachment")

    class Meta:
        verbose_name = _("Image Attachment")
        verbose_name_plural = _("Image Attachments")

    images = models.ManyToManyField(SingleImage, verbose_name=_("Images"), related_name='images', blank=True, default=None)

    def __str__(self):
        return f"{self.images}"


class TextField(BaseContentModel):
    TYPE = "Textfield"
    DESC = _("Textfield")

    class Meta:
        verbose_name = _("Textfield Content")
        verbose_name_plural = _("Textfield Contents")

    textfield = models.TextField(verbose_name=_("Textfield"))
    source = models.TextField(verbose_name=_("Source"))

    def __str__(self):
        return f"{self.content}"


class Latex(BaseContentModel, BasePDFModel):
    TYPE = "Latex"
    DESC = _("Latex")

    class Meta:
        verbose_name = _("Latex Content")
        verbose_name_plural = _("Latex Contents")

    textfield = models.TextField(verbose_name=_("Code Body"))
    source = models.TextField(verbose_name=_("Source"))

    def __str__(self):
        return f"{self.content}:{self.pdf}"


class PdfContent(BaseContentModel, BasePDFModel, BaseSourceModel):
    TYPE = "Pdf"
    DESC = _("Pdf")

    class Meta:
        verbose_name = _("Pdf Content")
        verbose_name_plural = _("Pdf Contents")

    def __str__(self):
        return f"{self.content}: {self.pdf}"


# All Content Types
CONTENT_TYPES = {
    YTVideoContent.TYPE: YTVideoContent,
    ImageContent.TYPE: ImageContent,
    PdfContent.TYPE: PdfContent,
    ImageAttachment.TYPE: ImageAttachment,
    TextField.TYPE: TextField,
    Latex.TYPE: Latex,
    SingleImage.TYPE: SingleImage
}

# Content Types which are not directly accessible via the topics, but embedded into other content types
EMBEDDED_CONTENT_TYPES = {
    ImageAttachment.TYPE,
    SingleImage.TYPE
}

# Content Types which allow attachments
ATTACHMENT_TYPES = {
    TextField.TYPE,
    Latex.TYPE
}
