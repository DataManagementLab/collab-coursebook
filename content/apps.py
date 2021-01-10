"""Purpose of this file

This file configures the application.
"""
from django.apps import AppConfig


class ContenttypesConfig(AppConfig):
    """ Content types configuration

    Configures the pluggable application content types.

    Attributes:
        ContenttypesConfig.name (str): Defines which application the configuration applies to
    """
    name = 'text'
