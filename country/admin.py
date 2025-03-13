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

from django.contrib import admin


from common.models import Country, City, Sightseeing

admin.site.register(Country)
admin.site.register(City)
admin.site.register(Sightseeing)
