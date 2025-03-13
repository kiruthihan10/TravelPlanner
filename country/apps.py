"""
App configuration for the 'country' application.
This configuration class sets the default auto field to 'BigAutoField'
and specifies the name of the application as 'country'.
"""

from django.apps import AppConfig


class CountryConfig(AppConfig):
    """
    Configuration class for the 'country' application.

    Attributes:
        default_auto_field (str): Specifies the type of auto-incrementing primary key to use for models in this app.
        name (str): The name of the application.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "country"
