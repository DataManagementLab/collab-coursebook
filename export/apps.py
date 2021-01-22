"""Purpose of this file

This file configures the application.
"""

from django.apps import AppConfig


class ExportConfig(AppConfig):
    """ Export configuration

    Configures the pluggable application for the export.

    :attr ContenttypesConfig.name: Defines which application the configuration applies to
    :type ContenttypesConfig.name: str
    """
    name = 'export'
