"""
CountryForm is a Django ModelForm for the Country model. It includes custom widgets and a method to render the form using a specified template.

Attributes:
    template (Template): The template used to render the form.

Meta:
    model (Model): The model associated with this form.
    fields (list): The fields to include in the form.
    widgets (dict): Custom widgets for the form fields.

Methods:
    save(commit=True) -> Country:
        Saves the form instance.
    render_form() -> str:
        Renders the form using the associated template and returns it as a string.
"""

from django.forms import ModelForm
from django.template import loader

from common.components.form import FormTextInput
from common.models import Country


class CountryForm(ModelForm):
    """
    CountryForm is a Django ModelForm for the Country model. It includes custom widgets and a method to render the form using a specified template.
    Attributes:
        template (Template): The template used to render the form.
    Meta:
        model (Model): The model associated with this form.
        fields (list): The fields to include in the form.
        widgets (dict): Custom widgets for the form fields.
    Methods:
        save(commit=True) -> Country:
            Saves the form instance.
        render_form() -> str:
            Renders the form using the associated template and returns it as a string.
    """

    template = loader.get_template("form.html")

    class Meta:
        """
        Meta class for the Country form.

        Attributes:
            model (Model): The model associated with the form.
            fields (list): List of fields to include in the form.
            widgets (dict): Dictionary specifying custom widgets for form fields.
        """
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
        """
        Renders the form using the associated template.

        Returns:
            str: The rendered form as a string.
        """
        return self.template.render({"form": self})
