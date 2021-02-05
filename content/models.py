"""Purpose of this file

This file describes or defines the basic structure of the content type. A class
that extends the models.Model class represents a content type and can be
registered in admin.py.
"""

import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from pdf2image import convert_from_path

from base.models import Content

from content.mixin import GeneratePreviewMixin

from content.validator import validate_pdf


class BaseModel(models.Model, GeneratePreviewMixin):
    """Base model

    This abstract class forms a basic skeleton for the models from which content
    types can be created.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True


class BaseContentModel(BaseModel):
    """Base content model

    This abstract class forms a basic skeleton for the models that are related to the content.


    :attr BaseContentModel.content: Describes the content of this model
    :type BaseContentModel.content: OneToOneField - Content
    """

    content = models.OneToOneField(Content,
                                   verbose_name=_("Content"),
                                   on_delete=models.CASCADE,
                                   primary_key=True)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True


class BasePDFModel(BaseModel):
    """Base content model

    This abstract class forms a basic skeleton for the models that are related to PDF.

    :attr BasePDFModel.pdf: Describes the PDF file of this model
    :type BasePDFModel.pdf: FileField
    """

    pdf = models.FileField(verbose_name=_("PDF"),
                           upload_to='uploads/contents/%Y/%m/%d/',
                           blank=True,
                           validators=(validate_pdf,))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True

    def generate_preview(self):
        """Generate preview

        Generates a preview of this model, more precisely the PDF is generated as a preview.

        :return: the string which represents the concatenated path components.
        :rtype: str
        """
        # Path of the preview folder
        preview_folder = 'uploads/previews/'
        # Checks if Folder exists
        if not os.path.exists(os.path.join(settings.MEDIA_ROOT, preview_folder)):
            os.makedirs(os.path.join(settings.MEDIA_ROOT, preview_folder))
        base_filename = os.path.splitext(os.path.basename(self.pdf.name))[0] + '.jpg'
        # Get images for every page
        pages = convert_from_path(self.pdf.path, last_page=2)
        # Save first page to disk
        pages[0].save(os.path.join(settings.MEDIA_ROOT, preview_folder, base_filename))
        return os.path.join(preview_folder, base_filename)


class BaseSourceModel(BaseModel):
    """Base content model

    This abstract class forms a basic skeleton for the models that are related to source.

    :attr BaseSourceModel.source: Describes the source of this model
    :type BaseSourceModel.source: TextField
    :attr BaseSourceModel.license: Describes the license of the source
    :type BaseSourceModel.license: CharField
    """

    source = models.TextField(verbose_name=_("Source"))
    license = models.CharField(verbose_name=_("License"),
                               blank=True,
                               max_length=200)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.abstract: Describes whether this model is an abstract model (class)
        :type Meta.abstract: bool
        """
        abstract = True


class ImageContent(BaseContentModel, BaseSourceModel):
    """Image content

    This model represents a content with an image.

    :attr ImageContent.TYPE: Describes the content type of this model
    :type ImageContent.TYPE: str
    :attr ImageContent.DESC: Describes the name of this model
    :type ImageContent.DESC: __proxy__
    :attr ImageContent.image: The image file of this model
    :type ImageContent.image: ImageField
    """
    TYPE = "Image"
    DESC = _("Single Image")

    image = models.ImageField(verbose_name=_("Image"),
                              upload_to='uploads/contents/%Y/%m/%d/')

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Image Content")
        verbose_name_plural = _("Image Contents")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.content}: {self.DESC} - {self.image}"


class Latex(BaseContentModel, BasePDFModel):
    """LaTeX text field

    This model represents a LaTeX based content.

    :attr Latex.TYPE: Describes the content type of this model
    :type Latex.TYPE: str
    :attr Latex.DESC: Describes the name of this model
    :type Latex.DESC: __proxy__
    :attr Latex.textfield: The LaTeX code of the content
    :type Latex.textfield: TextField
    :attr Latex.source: The source of this content
    :type Latex.source: TextField
    """
    TYPE = "Latex"
    DESC = _("Latex Textfield")

    textfield = models.TextField(verbose_name=_("Latex Code"))
    source = models.TextField(verbose_name=_("Source"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Latex Content")
        verbose_name_plural = _("Latex Contents")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.content}: {self.DESC} - {self.pdf}"


class PDFContent(BaseContentModel, BasePDFModel, BaseSourceModel):
    """LaTeX text field

    This model represents a PDF based content.

    :attr PDFContent.TYPE: Describes the content type of this model
    :type PDFContent.TYPE: str
    :attr PDFContent.DESC: Describes the name of this model
    :type PDFContent.DESC: __proxy__
    """
    TYPE = "PDF"
    DESC = _("PDF")

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("PDF Content")
        verbose_name_plural = _("PDF Contents")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.content}: {self.DESC} - {self.pdf}"


class SingleImageAttachment(BaseSourceModel):
    """Single image attachment

    This model represents a single image.

    :attr SingleImageAttachment.TYPE: Describes the content type of this model
    :type SingleImageAttachment.TYPE: str
    :attr SingleImageAttachment.DESC: Describes the name of this model
    :type SingleImageAttachment.DESC: __proxy__
    :attr SingleImageAttachment.image: The image file of this model
    :type SingleImageAttachment.image: ImageField
    """
    TYPE = "SingleImageAttachment"
    DESC = _("Single Image Attachment")

    image = models.ImageField(verbose_name=_("Image"),
                              upload_to='uploads/contents/%Y/%m/%d/')

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Single Image Attachment")
        verbose_name_plural = _("Single Image Attachments")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.image}"


class TextField(BaseContentModel):
    """Text field

    This model represents a text based content.

    :attr TextField.TYPE: Describes the content type of this model
    :type TextField.TYPE: str
    :attr TextField.DESC: Describes the name of this model
    :type TextField.DESC: __proxy__
    :attr TextField.textfield: The text of the content
    :type TextField.textfield: TextField
    :attr TextField.source: The source of this content
    :type TextField.source: TextField
    """
    TYPE = "Textfield"
    DESC = _("Textfield")

    textfield = models.TextField(verbose_name=_("Text"))
    source = models.TextField(verbose_name=_("Source"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Textfield Content")
        verbose_name_plural = _("Textfield Contents")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.content} : {self.DESC} - {self.pk}"


class YTVideoContent(BaseContentModel):
    """YouTube video model

    This model represents a content with a YouTube video.

    :attr YTVideoContent.TYPE: Describes the content type of this model
    :type YTVideoContent.TYPE: str
    :attr YTVideoContent.DESC: Describes the name of this model
    :type YTVideoContent.DESC: __proxy__
    :attr YTVideoContent.url: The link of the YouTube video
    :type YTVideoContent.url: URLField
    """
    TYPE = "YouTubeVideo"
    DESC = _("YouTube Video")

    url = models.URLField(verbose_name=_("Video URL"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("YouTube Video Content")
        verbose_name_plural = _("YouTube Video Contents")

    @property
    def id(self):
        """ID

        Splits the url by the symbol "=" to get the id of the YouTube url.

        return: The id fo the YouTube video
        rtype: str
        """
        split_url = self.url.split("=")
        if len(split_url) == 2:
            return self.url.split("=")[1]
        return self.url.split("=")[1].split("&")[0]

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.DESC}: {self.url}"


class ImageAttachment(BaseModel):
    """Image attachment

    This model represents the image attachment of a content.

    :attr ImageAttachment.TYPE: Describes the content type of this model
    :type ImageAttachment.TYPE: str
    :attr ImageAttachment.DESC: Describes the name of this model
    :type ImageAttachment.DESC: __proxy__
    :attr ImageAttachment.images: A reference to the single images
    :type ImageAttachment.images: ManyToManyField - SingleImageAttachment
    """
    TYPE = "ImageAttachment"
    DESC = _("Single Image Attachment")

    images = models.ManyToManyField(SingleImageAttachment,
                                    verbose_name=_("Images"),
                                    related_name='images',
                                    blank=True)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Image Attachment")
        verbose_name_plural = _("Image Attachments")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.DESC}: {self.images.creation_counter}"


# Dict: Contains all available content types.
CONTENT_TYPES = {
    YTVideoContent.TYPE: YTVideoContent,
    ImageContent.TYPE: ImageContent,
    PDFContent.TYPE: PDFContent,
    ImageAttachment.TYPE: ImageAttachment,
    TextField.TYPE: TextField,
    Latex.TYPE: Latex,
    SingleImageAttachment.TYPE: SingleImageAttachment
}

# Set: Content types which are not directly accessible via the topics,
# but embedded into other content types
EMBEDDED_CONTENT_TYPES = {
    ImageAttachment.TYPE,
    SingleImageAttachment.TYPE
}

# Set: Content types which allow image attachments
IMAGE_ATTACHMENT_TYPES = {
    TextField.TYPE,
    Latex.TYPE
}
