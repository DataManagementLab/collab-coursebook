"""Purpose of this file

This file configures the application for the frontend.
"""

from django.apps import AppConfig


class FrontendConfig(AppConfig):
    """ Content types configuration

    Configures the pluggable application for the frontend

    Attributes:
        ContenttypesConfig.name (str): Defines which application the configuration applies to
    """
    name = 'frontend'
