""" """

from django.http import HttpResponse
from django.template import loader

from common.models import Country
from common.pagination import pagination_handle
from django.core.paginator import Paginator

from country.tables import CountryTable


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
                "paginator": p,
                "countries": CountryTable(p.page(page_number)),
            },
            request,
        )
    )
