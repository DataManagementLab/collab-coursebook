"""Purpose of this file

This file configures the application.
"""

from django.apps import AppConfig


class AttachmentConfig(AppConfig):
    """ Content types configuration

    Configures the pluggable application for the content types.

    :attr ContenttypesConfig.name: Defines which application the configuration applies to
    :type ContenttypesConfig.name: str
    """
    name = 'content.attachment'
