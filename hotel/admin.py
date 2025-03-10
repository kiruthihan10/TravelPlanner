from django.contrib import admin

"""
This module registers the Hotel and Room models with the Django admin site.
Imports:
    from django.contrib import admin: Imports the Django admin module.
    from common.models import Hotel, Room: Imports the Hotel and Room models from the common.models module.
Functionality:
    admin.site.register(Hotel): Registers the Hotel model with the Django admin site.
    admin.site.register(Room): Registers the Room model with the Django admin site.
"""

from common.models import Hotel, Room

admin.site.register(Hotel)
admin.site.register(Room)

# Register your models here.
