from django.apps import AppConfig

"""
This module defines the configuration for the 'plane' application.
Classes:
    PlaneConfig(AppConfig): Configuration class for the 'plane' application.
"""


class PlaneConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plane"
