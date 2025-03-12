"""
This module defines the configuration for the 'hotel' application.
Classes:
    HotelConfig(AppConfig): Configuration class for the 'hotel' application.
"""

from django.apps import AppConfig


class HotelConfig(AppConfig):
    """
    Configuration for the Hotel app.

    This class defines the configuration for the Hotel application within the TravelPlanner project.
    It sets the default auto field type to BigAutoField and specifies the name of the app as 'hotel'.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "hotel"
