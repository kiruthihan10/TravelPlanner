from typing import List
from django.forms import ModelForm
from django.template import loader

from common.components.form import FormTextInput
from common.models import Country


class CountryForm(ModelForm):

    template = loader.get_template("form.html")

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

    def render_form(self):
        return self.template.render({"form": self})
            
