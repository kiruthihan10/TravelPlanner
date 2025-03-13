"""
This module registers the Plan, FlightPlan, and SightseeingPlan models
with the Django admin site, allowing them to be managed through the
Django admin interface.
Classes:
    None
Functions:
    None
Registers:
    Plan: The main plan model.
    FlightPlan: The model for flight plans.
    SightseeingPlan: The model for sightseeing plans.
"""

from django.contrib import admin


from common.models import Plan, FlightPlan, SightseeingPlan

admin.site.register(Plan)
admin.site.register(FlightPlan)
admin.site.register(SightseeingPlan)
