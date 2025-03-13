"""
Module to contain all Country App URLs
"""

from django.urls import path

from . import views

urlpatterns = [
    path("", views.country_list, name="country_list"),
]
