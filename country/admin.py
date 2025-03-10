from django.contrib import admin

"""
This module registers the Country model with the Django admin site.
Modules:
    admin (django.contrib.admin): The Django admin module.
    Country (common.models): The Country model from the common app.
Functions:
    None
Classes:
    None
Usage:
    This module is used to make the Country model manageable through the Django admin interface.
"""

from common.models import Country, City

admin.site.register(Country)
admin.site.register(City)
