from abc import ABC
from typing import List, Sequence
from django.db.models import Model


class ModelTable(ABC):

    def __init__(
        self, model: Sequence[Model], columns: List[str], row_func=None
    ) -> None:
        self.model = model
        self._columns = columns
        if row_func is None:
            self.row_func = self.default_row_func
        else:
            self.row_func = row_func

    def default_row_func(self, instance: Model) -> List:
        return [getattr(instance, column) for column in self._columns]

    @property
    def rows(self):
        for instance in self.model:
            row = self.row_func(instance)
            if len(row) != len(self._columns):
                raise ValueError(
                    "Row function does not return the correct number of columns."
                )
            yield row

    @property
    def columns(self):
        return [column.capitalize() for column in self._columns]
