"""Purpose of this file

This file describes or defines attachments of a content that supports
attachments.
"""

import reversion

from django.db import models
from django.utils.translation import gettext_lazy as _
from django.conf import settings
from django.core.validators import FileExtensionValidator

from base.models import Content

from content.models import BaseSourceModel, Latex, TextField, MDContent


class ImageAttachment(BaseSourceModel):
    """image attachment

    This model represents am imageAttachment. Specific contains may contain
    image attachments.

    :attr ImageAttachment.TYPE: Describes the type of this model
    :type ImageAttachment.TYPE: str
    :attr ImageAttachment.DESC: Describes the name of this model
    :type ImageAttachment.DESC: __proxy__
    :attr ImageAttachment.content: The content of this model
    :type ImageAttachment.image: ForeignKey
    :attr ImageAttachment.image: The image file of this model
    :type ImageAttachment.image: ImageField
    :attr ImageAttachment.source: Describes the source of this model
    :type ImageAttachment.source: TextField
    :attr ImageAttachment.license: Describes the license of the source
    :type ImageAttachment.license: CharField
    """
    TYPE = "ImageAttachment"
    DESC = _("Image Attachment")

    content = models.ForeignKey(Content,
                                verbose_name=_("Content"),
                                related_name='ImageAttachments',
                                on_delete=models.CASCADE)
    image = models.ImageField(verbose_name=_("Image"),
                              upload_to='uploads/contents/%Y/%m/%d/',
                              validators=
                              [FileExtensionValidator(settings.ALLOWED_IMAGE_EXTENSIONS)],
                              help_text=_("Allowed extensions are: ")
                                        + ", ".join(settings.ALLOWED_IMAGE_EXTENSIONS) + ".")

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
        return f"{self.image}"


# Set: Content types which allow image attachments
IMAGE_ATTACHMENT_TYPES = {
    TextField.TYPE,
    Latex.TYPE,
    MDContent.TYPE
}

# Register models for reversion if it is not already done in admin,
# else we can specify configuration
reversion.register(ImageAttachment,
                   fields=['image', 'source', 'license'])
