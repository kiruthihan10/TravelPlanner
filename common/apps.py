from django.apps import AppConfig

"""
Django application configuration for the 'common' app.
This class defines the configuration for the 'common' app, including the
default auto field type and the app name.
Attributes:
    default_auto_field (str): Specifies the type of auto-incrementing primary key field to use by default.
    name (str): The name of the app.
"""


class CommonConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "common"
