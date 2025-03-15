"""
Handles the request to list countries with optional search and pagination.

Args:
    request (HttpRequest): The HTTP request object containing GET parameters.

Returns:
    HttpResponse: The HTTP response object with the rendered template.

GET Parameters:
    search_text (str, optional): The text to search for in country names.
    page (int, optional): The page number for pagination.
    size (int, optional): The number of items per page for pagination.

Template:
    countries.html: The template used to render the list of countries.

Context:
    paginator (Paginator): The paginator object for handling pagination.
    countries (Page): The current page of countries.
"""

from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from django.core.paginator import Paginator

from common.components.tables import pagination_handle
from common.models import Country

from .forms import CountryForm
from .tables import CountryTable


def country_list(request):
    """
    Handles the request to list countries with optional search and pagination.

    Args:
        request (HttpRequest): The HTTP request object containing GET parameters.

    Returns:
        HttpResponse: The HTTP response object with the rendered template.

    GET Parameters:
        search_text (str, optional): The text to search for in country names.
        page (int, optional): The page number for pagination.
        size (int, optional): The number of items per page for pagination.

    Template:
        countries.html: The template used to render the list of countries.

    Context:
        paginator (Paginator): The paginator object for handling pagination.
        countries (Page): The current page of countries.
    """
    template = loader.get_template("countries.html")
    size, page_number = pagination_handle(request)
    search_text = request.GET.get("search_text")
    if search_text is None:
        countries = Country.objects.all()
    else:
        countries = Country.objects.filter(name__icontains=search_text)
    p = Paginator(countries, size)
    return HttpResponse(
        template.render(
            {
                "countries": CountryTable(p.page(page_number)).render(),
            },
            request,
        )
    )


def create_country(request):
    """
    Handles the request to create a new country.

    Args:
        request (HttpRequest): The HTTP request object containing the form data.

    Returns:
        HttpResponse: The HTTP response object with the rendered template.

    Template:
        create_country.html: The template used to render the country creation form.

    Context:
        form (CountryForm): The form object for creating a new country.
    """
    template = loader.get_template("create_country.html")
    if request.method == "GET":
        country_form = CountryForm()
    elif request.method == "POST":
        country_form = CountryForm(request.POST)
        if country_form.is_valid():
            country_form.save()
            return redirect("/countries/")
    else:
        return HttpResponse(status=405)
    return HttpResponse(template.render({"form": country_form.render_form()}, request))
