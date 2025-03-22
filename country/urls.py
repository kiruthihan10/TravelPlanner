"""
Module to contain all Country App URLs
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.country_list, name="country_list"),
    path("add", views.create_country, name="create_country"),
    path("<str:country_id>", views.view_country, name="edit_country"),
]
