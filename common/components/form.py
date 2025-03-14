from typing import Any, Union
from django.forms import TextInput


class FormTextInput(TextInput):
    """
    Text Input
    """

    def __init__(self, attrs: Union[dict[str, Any], None] = None, **kwargs) -> None:
        super().__init__(attrs, **kwargs)
        self.attrs["class"] = "input is-rounded"
