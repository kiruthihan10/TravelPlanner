"""
This module contains the application configuration for the 'common' app.
Classes:
    CommonConfig(AppConfig): Configuration class for the 'common' app.
"""

from django.apps import AppConfig


class CommonConfig(AppConfig):
    """
    Django application configuration for the 'common' app.

    Attributes:
        default_auto_field (str): Specifies the type of auto-incrementing primary key to use for models in this app.
        name (str): The name of the app.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "common"
