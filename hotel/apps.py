from django.apps import AppConfig

"""
This module defines the configuration for the 'hotel' application.
Classes:
    HotelConfig(AppConfig): Configuration class for the 'hotel' application.
"""


class HotelConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "hotel"
