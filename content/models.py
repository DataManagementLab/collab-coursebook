"""Purpose of this file

This file describes or defines the basic structure of the content type. A class that extends the models.Model class
represents a content type and can be registered in admin.py.
"""

import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.models import Content

from content.mixin import GeneratePreviewMixin

from pdf2image import convert_from_path


class BaseModel(models.Model):
    """Base model

    This abstract class forms a basic skeleton for the models from which content types can be created.
    """

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.abstract (bool): Describes whether this model is an abstract model (class)
        """
        abstract = True

    def generate_preview(self):
        """Preview

        Generates a preview of this model.
        """
        return


class BaseContentModel(BaseModel):
    """Base content model

    This abstract class forms a basic skeleton for the models that are related to the content.

    Attributes:
        BaseContentModel.content (OneToOneField - Content): Describes the content of this model
    """

    content = models.OneToOneField(Content, verbose_name=_("Content"), on_delete=models.CASCADE, primary_key=True)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.abstract (bool): Describes whether this model is an abstract model (class)
        """
        abstract = True


class BasePDFModel(BaseModel, GeneratePreviewMixin):
    """Base content model

    This abstract class forms a basic skeleton for the models that are related to PDF.

    Attributes:
        BasePDFModel.pdf (FileField): Describes the PDF of this model
    """

    pdf = models.FileField(verbose_name=_("PDF"), upload_to='uploads/contents/%Y/%m/%d/', blank=True)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.abstract (bool): Describes whether this model is an abstract model (class)
        """
        abstract = True

    def generate_preview(self):
        """Preview

        Generates a preview of this model, more precisely the PDF is generated as a preview.

        return: The string which represents the concatenated path components.
        rtype: str
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

    Attributes:
        BaseSourceModel.source (TextField): Describes the source of this model
        BaseSourceModel.license (CharField): Describes the license of the source
    """

    source = models.TextField(verbose_name=_("Source"))
    license = models.CharField(verbose_name=_("License"), blank=True, max_length=200)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.abstract (bool): Describes whether this model is an abstract model (class)
        """
        abstract = True


class ImageContent(BaseContentModel, BaseSourceModel):
    """Image content

    This model represents a content with an image.

    Attributes:
        BaseSourceModel.TYPE (str): Describes the content type of this model
        BaseSourceModel.DESC (__proxy__): Describes the name of this model
        BaseSourceModel.image (ImageField): The image file to store
    """
    TYPE = "Image"
    DESC = _("Single Image")

    image = models.ImageField(verbose_name=_("Image"), upload_to='uploads/contents/%Y/%m/%d/')

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Image Content")
        verbose_name_plural = _("Image Contents")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.content}: {self.image}"


class Latex(BaseContentModel, BasePDFModel):
    """LaTeX text field

    This model represents a LaTeX based content.

    Attributes:
        BaseSourceModel.TYPE (str): Describes the content type of this model
        BaseSourceModel.DESC (__proxy__): Describes the name of this model
        BaseSourceModel.textfield (TextField): The LaTeX code of the content
        BaseSourceModel.source (TextField): The source of the content
    """
    TYPE = "Latex"
    DESC = _("Latex Textfield")

    textfield = models.TextField(verbose_name=_("Latex Code"))
    source = models.TextField(verbose_name=_("Source"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Latex Content")
        verbose_name_plural = _("Latex Contents")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.content}:{self.pdf}"


class PDFContent(BaseContentModel, BasePDFModel, BaseSourceModel):
    """LaTeX text field

    This model represents a PDF based content.

    Attributes:
        BaseSourceModel.TYPE (str): Describes the content type of this model
        BaseSourceModel.DESC (__proxy__): Describes the name of this model
    """
    TYPE = "PDF"
    DESC = _("PDF")

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("PDF Content")
        verbose_name_plural = _("PDF Contents")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.content}: {self.pdf}"


class SingleImage(BaseSourceModel):
    """Image content

    This model represents a single image.

    Attributes:
        BaseSourceModel.TYPE (str): Describes the content type of this model
        BaseSourceModel.DESC (__proxy__): Describes the name of this model
        BaseSourceModel.image (ImageField): The image file to store
    """
    TYPE = "SingleImage"
    DESC = _("Single Image")

    image = models.ImageField(verbose_name=_("Attached Image"), upload_to='uploads/contents/%Y/%m/%d/')

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Single Image")
        verbose_name_plural = _("Single Images")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.image}"


class TextField(BaseContentModel):
    """Text field

    This model represents a text based content.

    Attributes:
        BaseSourceModel.TYPE (str): Describes the content type of this model
        BaseSourceModel.DESC (__proxy__): Describes the name of this model
        BaseSourceModel.textfield (TextField): The text of the content
        BaseSourceModel.source (TextField): The source of the content
    """
    TYPE = "Textfield"
    DESC = _("Textfield")

    textfield = models.TextField(verbose_name=_("Text"))
    source = models.TextField(verbose_name=_("Source"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Textfield Content")
        verbose_name_plural = _("Textfield Contents")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.content}"


class YTVideoContent(BaseContentModel):
    """YouTube video model

    This model represents a content with a YouTube video.

    Attributes:
        BaseSourceModel.TYPE (str): Describes the content type of this model
        BaseSourceModel.DESC (__proxy__): Describes the name of this model
        BaseSourceModel.url (URLField): The link of the YouTube video
    """
    TYPE = "YouTubeVideo"
    DESC = _("YouTube Video")

    url = models.URLField(verbose_name=_("Video URL"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
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
        return self.url.split("=")[1]

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.DESC}: {self.url}"


class ImageAttachment(BaseModel):
    """Image attachment

    This model represents the image attachment of a content.

    Attributes:
        BaseSourceModel.TYPE (str): Describes the content type of this model
        BaseSourceModel.DESC (__proxy__): Describes the name of this model
        BaseSourceModel.images (ManyToManyField - SingleImage): A reference to the single images
    """
    TYPE = "ImageAttachment"
    DESC = _("Single Image Attachment")

    images = models.ManyToManyField(SingleImage, verbose_name=_("Images"), related_name='images', blank=True)

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        Attributes:
            Meta.verbose_name (__proxy__): A human-readable name for the object in singular
            Meta.verbose_name_plural (__proxy__): A human-readable name for the object in plural
        """
        verbose_name = _("Image Attachment")
        verbose_name_plural = _("Image Attachments")

    def __str__(self):
        """String representation

        return: the string representation of this object.
        rtype: str
        """
        return f"{self.images.creation_counter}"


# Dict: Contains all available content types.
CONTENT_TYPES = {
    YTVideoContent.TYPE: YTVideoContent,
    ImageContent.TYPE: ImageContent,
    PDFContent.TYPE: PDFContent,
    ImageAttachment.TYPE: ImageAttachment,
    TextField.TYPE: TextField,
    Latex.TYPE: Latex,
    SingleImage.TYPE: SingleImage
}

# Set: Content types which are not directly accessible via the topics, but embedded into other content types
EMBEDDED_CONTENT_TYPES = {
    ImageAttachment.TYPE,
    SingleImage.TYPE
}

# Set: Content types which allow image attachments
IMAGE_ATTACHMENT_TYPES = {
    TextField.TYPE,
    Latex.TYPE
}
