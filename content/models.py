"""Purpose of this file

This file describes or defines the basic structure of the content type. A class
that extends the models.Model class represents a content type and can be
registered in admin.py.
"""

import os
import re

import reversion
from django.conf import settings
from django.db import models
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import FileExtensionValidator

from pdf2image import convert_from_path

from base.models import Content

from content.mixin import GeneratePreviewMixin
from content.validator import Validator
from content.static.yt_api import get_video_length, timestamp_to_seconds, seconds_to_timestamp


class BaseContentModel(models.Model, GeneratePreviewMixin):
    """Base content model

    This abstract class forms a basic skeleton for the models that are related to the content.
    Each model extended from this model contains a relation to a content. The extended models
    defines the specific content types with their own presentation of the content.


    :attr BaseContentModel.content: The content of this model
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

    @staticmethod
    def filter_by_own_type(contents):
        """
        Filter the given contents: Restrict to own type only

        :param contents: contents to filter
        :type contents: QuerySet[Content]
        :return: filtered contents queryset
        :rtype: QuerySet[Content]
        """
        return contents.all()


class BasePDFModel(models.Model):
    """Base content model

    This abstract class forms a basic skeleton for the models that are related to PDF.
    Each model extended from this model contains a relation to pd file.

    :attr BasePDFModel.pdf: Describes the PDF file of this model
    :type BasePDFModel.pdf: FileField
    """
    pdf = models.FileField(verbose_name=_("PDF"),
                           upload_to='uploads/contents/%Y/%m/%d/',
                           blank=True,
                           validators=(Validator.validate_pdf,))

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


class BaseSourceModel(models.Model):
    """Base content model

    This abstract class forms a basic skeleton for the models that are related to source.
    Each model extended from this model contains a relation to a source. A source contains further
    a license.

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
    DESC = _("Image")

    image = models.ImageField(verbose_name=_("Image"),
                              upload_to='uploads/contents/%Y/%m/%d/',
                              validators=
                              [FileExtensionValidator(settings.ALLOWED_IMAGE_EXTENSIONS)],
                              help_text=_("Allowed extensions are: ")
                                        + ", ".join(settings.ALLOWED_IMAGE_EXTENSIONS) + "."
                              )

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
        return f"{self.content}: {self.image}"

    @staticmethod
    def filter_by_own_type(contents):
        return contents.filter(imagecontent__isnull=False)


class Latex(BaseContentModel, BasePDFModel):
    """LaTeX text field

    This model represents a LaTeX based content.

    :attr Latex.TYPE: Describes the content type of this model
    :type Latex.TYPE: str
    :attr Latex.DESC: Describes the name of this model
    :type Latex.DESC: __proxy__
    :attr Latex.textfield: The Latex code of the content
    :type Latex.textfield: TextField
    :attr Latex.source: The source of this content
    :type Latex.source: TextField
    """
    TYPE = "Latex"
    DESC = _("Text (LaTeX)")

    textfield = models.TextField(verbose_name=_("Latex Code"),
                                 help_text=_("Please insert only valid LaTeX code. The packages "
                                             "and \\begin{document} "
                                             "and \\end{document} will be inserted automatically."))
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
        return f"{self.content}: {self.pk}"

    @staticmethod
    def filter_by_own_type(contents):
        return contents.filter(latex__isnull=False)


class PDFContent(BaseContentModel, BasePDFModel, BaseSourceModel):
    """PDF content

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
        return f"{self.content}: {self.pdf}"

    @staticmethod
    def filter_by_own_type(contents):
        return contents.filter(pdfcontent__isnull=False)


class MDContent(BaseContentModel):
    """MD content

    This model represents a MD based content.

    :attr MDContent.TYPE: Describes the content type of this model
    :type MDContent.TYPE: str
    :attr MDContent.DESC: Describes the name of this model
    :type MDContent.DESC: __proxy__
    :attr MDContent.md: The md file for this content
    :type MDContent.md: FileField
    :attr MDContent.textfield: The md code of this content
    :type MDContent.source: TextField
    :attr MDContent.source: The source of this content
    :type MDContent.source: TextField
    """
    TYPE = "MD"
    DESC = _("Markdown")

    md = models.FileField(verbose_name=_("Markdown File"),
                          upload_to='uploads/contents/%Y/%m/%d/',
                          blank=True,
                          validators=[FileExtensionValidator(['md']), Validator.validate_md])

    textfield = models.TextField(verbose_name=_("Markdown Script"),
                                 help_text=_("Insert your Markdown script here:"),
                                 blank=True)
    source = models.TextField(verbose_name=_("Source"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("MD Content")
        verbose_name_plural = _("MD Contents")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.content}; {self.pk} "

    @staticmethod
    def filter_by_own_type(contents):
        return contents.filter(mdcontent__isnull=False)


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
    DESC = _("Text")

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
        return f"{self.content}: {self.pk}"

    @staticmethod
    def filter_by_own_type(contents):
        return contents.filter(textfield__isnull=False)


class AnkiDeck(BaseContentModel):
    """Anki deck

    This model represents a text based content.

    :attr AnkiDeck.TYPE: Describes the content type of this model
    :type AnkiDeck.TYPE: str
    :attr AnkiDeck.DESC: Describes the name of this model
    :type AnkiDeck.DESC: __proxy__
    :attr AnkiDeck.textfield: The text of the content
    :type AnkiDeck.textfield: TextField
    :attr AnkiDeck.source: The source of this content
    :type AnkiDeck.source: TextField
    """
    TYPE = "AnkiDeck"
    DESC = _("Anki Deck")

    file = models.FileField(verbose_name=_("Anki Deck"),
                            upload_to='uploads/contents/%Y/%m/%d/',
                            blank=True,
                            validators=(Validator.validate_anki_file,))
    source = models.TextField(verbose_name=_("Source"))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Anki Deck")
        verbose_name_plural = _("Anki Decks")

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.content}: {self.pk}"

    @staticmethod
    def filter_by_own_type(contents):
        return contents.filter(ankideck__isnull=False)


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

    url = models.URLField(verbose_name=_("Video URL"), validators=(Validator.validate_youtube_url,))

    start_time = models.CharField(verbose_name=_("Video Start Timestamp"), max_length=8,
                                  default="0:00",
                                  help_text=_(
                                      "Type in the time as HH:MM:SS (e.g. 2:05:10, 2:05, 0:50)."))

    end_time = models.CharField(verbose_name=_("Video End Timestamp"), max_length=8, default="0:00",
                                help_text=_(
                                    "Type in the time as HH:MM:SS (e.g. 2:05:10, 2:05, 0:50)."))

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
    def id(self):  # pylint: disable=C0103
        """ID

        Splits the url by the symbol "=" to get the id of the YouTube url.

        return: The id of the YouTube video
        rtype: str
        """
        if 'youtube.com' in self.url:
            split_url = self.url.split("=")
            if len(split_url) == 2:
                return self.url.split("=")[1]
            if len(split_url) > 2:
                return self.url.split("=")[1].split("&")[0]
            return self.url.split("/")[2]
        if 'youtu.be' in self.url:
            return self.url.split("/")[3]
        return self.url.split("/")[4]

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.url}"

    @staticmethod
    def filter_by_own_type(contents):
        return contents.filter(ytvideocontent__isnull=False)

    def clean(self):

        colon_regex = "^((((0?[1-9]|1[0-2]):)?[0-5][0-9]:[0-5][0-9])|[0-9]:[0-5][0-9])$"

        colon_pattern = re.compile(colon_regex)

        if not colon_pattern.match(self.start_time):
            raise ValidationError(_("Please input a correct format for your starting time."))
        if not colon_pattern.match(self.end_time):
            raise ValidationError(_("Please input a correct format for your ending time."))

        seconds = get_video_length(self.id)
        start_time = timestamp_to_seconds(self.start_time)
        end_time = timestamp_to_seconds(self.end_time)
        if end_time == 0:
            end_timestamp = seconds_to_timestamp(seconds)
            self.end_time = end_timestamp
            end_time = timestamp_to_seconds(end_timestamp)

        if start_time == end_time:
            raise ValidationError(
                _('Please make sure that your start and end time are different.'))
        if start_time > end_time:
            raise ValidationError(
                _('Please make sure that your end time is larger than your start time.'))
        if (start_time > seconds and end_time > seconds):
            raise ValidationError(
                _('Please make sure your start and end times are smaller than the videos length.'))
        if start_time > seconds:
            raise ValidationError(
                _('Please make sure your start time is smaller than the videos length.'))
        if end_time > seconds:
            raise ValidationError(
                _('Please make sure your end time is smaller than the videos length.'))


class PanoptoVideoContent(BaseContentModel):
    """Panopto video model

    This model represents a content with a YouTube video.

    :attr PanoptoVideoContent.TYPE: Describes the content type of this model
    :type PanoptoVideoContent.TYPE: str
    :attr PanoptoVideoContent.DESC: Describes the name of this model
    :type PanoptoVideoContent.DESC: __proxy__
    :attr PanoptoVideoContent.url: The link of the Panopto video
    :type PanoptoVideoContent.url: URLField
    """
    TYPE = "PanoptoVideo"
    DESC = _("Panopto Video")

    url = models.URLField(verbose_name=_("Video URL"), validators=(Validator.validate_panopto_url,))

    class Meta:
        """Meta options

        This class handles all possible meta options that you can give to this model.

        :attr Meta.verbose_name: A human-readable name for the object in singular
        :type Meta.verbose_name: __proxy__
        :attr Meta.verbose_name_plural: A human-readable name for the object in plural
        :type Meta.verbose_name_plural: __proxy__
        """
        verbose_name = _("Panopto Video Content")
        verbose_name_plural = _("Panopto Video Contents")

    @property
    def id(self):  # pylint: disable=C0103
        """Panopto Video ID

        Splits the URL by the symbol "=" to get the id of the Panopto URL.

        return: The id of the Panopto video
        rtype: str
        """
        if 'panopto.eu/Panopto/Pages/Viewer.aspx' in self.url:
            split_url = self.url.split("?")[1]
            video_id = [url.split("=")[1] for url in split_url.split("&") if url.startswith("id=")]

            if video_id:
                return video_id[0]

    @property
    def start_time(self):
        """Panopto Video Start Time

        Extracts the Panopto video start time (if available) from the URL.

        Return: str: The Panopto video start time.
                 If start time is not present, it defaults to "0:00:00".
        """
        if 'panopto.eu/Panopto/Pages/Viewer.aspx' in self.url:
            split_url = self.url.split("?")[1]
            start_time_param = [url.split("=")[1] for url in split_url.split("&") if url.startswith("start=")]

            if start_time_param:
                return start_time_param[0]
            else:
                return "0:00:00"

    @property
    def new_url(self):
        """Panopto Video New URL

        Cuts &query part (if available) from the URL.

        Return: str: The Panopto video URL cut at &query.
                 If there is an issue it defaults to regular URL
        """
        if 'panopto.eu/Panopto/Pages/Viewer.aspx' in self.url:
            # Define a regular expression to match the "&query" part
            regex_pattern = r'&query=[^&]*'

            # Use re.sub to remove the "&query" part from the URL
            new_url = re.sub(regex_pattern, '', self.url)

            if new_url:
                return new_url
            else:
                return self.url

    def __str__(self):
        """String representation

        Returns the string representation of this object.

        :return: the string representation of this object
        :rtype: str
        """
        return f"{self.url}"

    @staticmethod
    def filter_by_own_type(contents):
        return contents.filter(panoptovideocontent__isnull=False)


# dict: Contains all available content types.
CONTENT_TYPES = {
    PDFContent.TYPE: PDFContent,
    TextField.TYPE: TextField,
    Latex.TYPE: Latex,
    YTVideoContent.TYPE: YTVideoContent,
    ImageContent.TYPE: ImageContent,
    MDContent.TYPE: MDContent,
    PanoptoVideoContent.TYPE: PanoptoVideoContent,
    AnkiDeck.TYPE: AnkiDeck,
}

# Register models for reversion if it is not already done in admin,
# else we can specify configuration
reversion.register(ImageContent,
                   fields=['content', 'image', 'source', 'license'],
                   follow=['content'])
reversion.register(TextField,
                   fields=['content', 'textfield', 'source'],
                   follow=['content'])
reversion.register(Latex,
                   fields=['content', 'textfield', 'source'],
                   follow=['content'])
reversion.register(PDFContent,
                   fields=['content', 'pdf', 'source', 'license'],
                   follow=['content'])
reversion.register(YTVideoContent,
                   fields=['content', 'url', 'start_time', 'end_time'],
                   follow=['content'])
reversion.register(MDContent,
                   fields=['content', 'md', 'textfield', 'source'],
                   follow=['content'])
reversion.register(PanoptoVideoContent,
                   fields=['content', 'url', 'start_time'],
                   follow=['content'])
reversion.register(AnkiDeck,
                   fields=['content', 'source'],
                   follow=['content'])
