"""
This module defines the configuration for the 'plane' application.
Classes:
    PlaneConfig(AppConfig): Configuration class for the 'plane' application.
"""

from django.apps import AppConfig


class PlaneConfig(AppConfig):
    """
    Configuration class for the 'plane' application.

    This class inherits from Django's AppConfig and sets the default
    auto field to BigAutoField. It also specifies the name of the app
    as 'plane'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "plane"
