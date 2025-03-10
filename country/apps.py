from django.apps import AppConfig

"""
App configuration for the 'country' application.
This configuration class sets the default auto field to 'BigAutoField' 
and specifies the name of the application as 'country'.
"""


class CountryConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "country"
