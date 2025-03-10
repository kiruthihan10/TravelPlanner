from django.contrib import admin

"""
Admin configuration for the TravelPlanner application.
This module registers the Airport and Flight models with the Django admin site,
allowing them to be managed through the Django admin interface.
Classes:
    None
Functions:
    None
Modules:
    admin - Django's admin module for registering models.
    common.models - Module containing the Airport and Flight models.
"""

from common.models import Airport, Flight

admin.site.register(Airport)
admin.site.register(Flight)
