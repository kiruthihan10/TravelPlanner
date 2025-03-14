from abc import ABC
from typing import List
from django.db.models import Model
from django.core.paginator import Page
from django.http import HttpRequest
from django.template import loader


def pagination_handle(request: HttpRequest, default_size=10, default_page_number=1):
    """
    Handle Pagination Size and page Number Parameter
    """
    size = request.GET.get("size", str(default_size))
    if size.isnumeric():
        size = int(size)
    else:
        size = default_size
    page_number = request.GET.get("page", str(default_page_number))
    if page_number.isnumeric():
        page_number = int(page_number)
    else:
        page_number = default_page_number
    return size, page_number


class ModelTable(ABC):

    def __init__(self, instances: Page, columns: List[str], row_func=None) -> None:
        self.instances = instances
        self._columns = columns
        if row_func is None:
            self.row_func = self.default_row_func
        else:
            self.row_func = row_func
        self.template = loader.get_template("table.html")

    def default_row_func(self, instance: Model) -> List:
        return [getattr(instance, column) for column in self._columns]

    @property
    def rows(self):
        for instance in self.instances:
            row = self.row_func(instance)
            if len(row) != len(self._columns):
                raise ValueError(
                    "Row function does not return the correct number of columns."
                )
            yield row

    @property
    def columns(self):
        return [column.capitalize() for column in self._columns]

    @property
    def has_previous(self):
        return self.instances.has_previous()

    @property
    def has_next(self):
        return self.instances.has_next()

    @property
    def previous_page_number(self):
        return self.instances.previous_page_number()

    @property
    def next_page_number(self):
        return self.instances.next_page_number()

    @property
    def page_number(self):
        return self.instances.number

    @property
    def page_size(self):
        return self.instances.paginator.per_page

    def render(self):
        return self.template.render({"table": self})
