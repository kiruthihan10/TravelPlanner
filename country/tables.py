from typing import List, Sequence
from common.models import Country
from common.tables import ModelTable


class CountryTable(ModelTable):

    def __init__(self, countries: Sequence[Country], columns: List[str] = ["name","number of cities"]):
        super().__init__(countries, columns)

    def default_row_func(self, instance: Country) -> List:
        return [instance.name, instance.cities.count()]
