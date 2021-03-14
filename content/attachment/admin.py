"""Purpose of this file

This file describes the available attachments in the admin panel.
The attachments are ordered alphabetically. This can be found in the
Attachment section of the admin panel. Contents can be added to or
modified for the various attachments.
"""

from django.contrib import admin

from reversion_compare.admin import CompareVersionAdmin

from content.attachment.forms import AdminImageAttachmentForm
from content.attachment.models import ImageAttachment


@admin.register(ImageAttachment)
class ImageAttachmentAdmin(CompareVersionAdmin):  # pylint: disable=too-many-ancestors
    """Image attachment admin

    Represents the image attachment model in the admin panel.

    :attr ImageAttachmentAdmin.form: Defines custom validation of the data
    :type ImageAttachmentAdmin.form: ModelForm
    """
    form = AdminImageAttachmentForm
