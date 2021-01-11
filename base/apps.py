"""Purpose of this file

This file configures the application.
"""

from django.apps import AppConfig


class BaseConfig(AppConfig):
    """ Content types configuration

    Configures the pluggable application for the base.

    Attributes:
        ContenttypesConfig.name (str): Defines which application the configuration applies to
    """
    name = 'base'
