"""
A module for representing a table of Country instances.
Classes:
    CountryTable(ModelTable):

"""

from typing import List, Union

from django.core.paginator import Page
from django.db.models import Model

from common.models import City, Country
from common.components.tables import ModelTable


class CountryTable(ModelTable):
    """
    A table representation for a collection of Country instances.
    Attributes:
        countries (Page): A paginated collection of Country instances.
        columns (List[str]): A list of column names for the table, defaulting to ["name", "number of cities"].
    Methods:
        __init__(countries: Page, columns: List[str] = ["name", "number of cities"]):
            Initializes the CountryTable with a collection of countries and optional column names.
            Raises a ValueError if any item in countries is not an instance of the Country model.
        default_row_func(instance: Country) -> List:
            Returns a list representing a row in the table for a given Country instance.
            The row contains the country's name and the count of its cities.
    """

    def __init__(self, countries: Page, columns: Union[List[str], None] = None):
        if columns is None:
            columns = ["name", "number of cities"]
        super().__init__(countries, columns)
        if not all(isinstance(country, Country) for country in countries):
            raise ValueError(
                "All items in countries must be instances of Country model"
            )

    def default_row_func(self, instance: Country) -> List:
        """
        Generates a default row representation for a given Country instance.

        Args:
            instance (Country): The Country instance for which to generate the row.

        Returns:
            List: A list containing the country's name and the count of its cities.
        """
        return [instance.name, instance.cities.count()]

    def default_row_link_func(self, country: Model) -> str:
        """
        Generates a default link for a given country.

        Args:
            country (Model): The country model instance.

        Returns:
            str: The primary key of the country as a string.
        """
        return country.pk


class CityTable(ModelTable):
    """
    A table representation for a collection of City instances.
    Attributes:
        cities (Page): A paginated collection of City instances.
        columns (List[str]): A list of column names for the table, defaulting to ["name", "population"].
    Methods:
        __init__(cities: Page, columns: List[str] = ["name", "population"]):
            Initializes the CityTable with a collection of cities and optional column names.
            Raises a ValueError if any item in cities is not an instance of the City model.
        default_row_func(instance: City) -> List:
            Returns a list representing a row in the table for a given City instance.
            The row contains the city's name and population.
    """

    def __init__(self, cities: Page, columns: Union[List[str], None] = None):
        if columns is None:
            columns = ["name", "sightseeings", "hotels", "sightseeing plans", "plans"]
        super().__init__(cities, columns)
        if not all(isinstance(city, City) for city in cities):
            raise ValueError("All items in cities must be instances of City model")

    def default_row_func(self, instance: City) -> List:
        """
        Generates a list of default row values for a given City instance.
        Args:
            instance (City): The City instance for which to generate the row values.
        Returns:
            List: A list containing the city's name, the count of its sightseeings,
                  the count of its hotels, the count of its sightseeing plans, and
                  the count of its plans.
        """
        
        return [
            instance.name,
            instance.sightseeings.count(),
            instance.hotels.count(),
            instance.sightseeing_plans.count(),
            instance.plans.count(),
        ]

    def default_row_link_func(self, city: Model) -> str:
        """
        Generates a default link for a given city.

        Args:
            city (Model): The city model instance.

        Returns:
            str: The primary key of the city as a string.
        """
        return city.pk
