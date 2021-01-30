"""Purpose of this file

This file configures the application.
"""

from django.apps import AppConfig


class BaseConfig(AppConfig):
    """ Content types configuration

    Configures the pluggable application for the base.

    :attr BaseConfig.name: Defines which application the configuration applies to
    :type BaseConfig.name: str
    """
    name = 'base'
