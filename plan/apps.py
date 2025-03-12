"""
This module defines the configuration for the 'plan' application.
Classes:
    PlanConfig: Configures the 'plan' application with default settings.
"""

from django.apps import AppConfig


class PlanConfig(AppConfig):
    """
    Configuration for the Plan application.

    This class sets the default auto field to BigAutoField and specifies
    the name of the application as 'plan'.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "plan"
