"""
A module for representing a table of Country instances.
Classes:
    CountryTable(ModelTable):

"""

from typing import List, Union

from django.core.paginator import Page

from common.models import Country
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
