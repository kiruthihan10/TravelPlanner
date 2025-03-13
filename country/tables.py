from typing import List
from common.models import Country
from common.tables import ModelTable
from django.core.paginator import Page


class CountryTable(ModelTable):

    def __init__(self, countries: Page, columns: List[str] = ["name","number of cities"]):
        super().__init__(countries, columns)
        if not all(isinstance(country, Country) for country in countries):
            raise ValueError("All items in countries must be instances of Country model")

    def default_row_func(self, instance: Country) -> List:
        return [instance.name, instance.cities.count()]
