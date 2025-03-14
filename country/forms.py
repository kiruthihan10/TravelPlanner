from django.forms import ModelForm

from common.components.form import FormTextInput
from common.models import Country


class CountryForm(ModelForm):

    class Meta:

        model = Country
        fields = ["name"]
        widgets = {
            "name": FormTextInput(attrs={"placeholder": "Country Name"}),
        }

    def save(self, commit=True) -> Country:
        """
        Save Country Form
        """
        return super().save(commit)