from django.apps import AppConfig
"""
This module defines the configuration for the 'plan' application.
Classes:
    PlanConfig: Configures the 'plan' application with default settings.
"""


class PlanConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "plan"
