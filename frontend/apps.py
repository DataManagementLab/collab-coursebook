"""Purpose of this file

This file configures the application for the frontend.
"""

from django.apps import AppConfig


class FrontendConfig(AppConfig):
    """ Content types configuration

    Configures the pluggable application for the frontend

    :attr ContenttypesConfig.name: Defines which application the configuration applies to
    :type ContenttypesConfig.name: str
    """
    name = 'frontend'
