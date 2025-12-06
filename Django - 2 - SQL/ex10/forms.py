from django import forms
from .models import People


class SearchForm(forms.Form):
    min_release_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=True
    )
    max_release_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=True
    )
    planet_diameter = forms.IntegerField(required=True)
    gender = forms.ChoiceField(choices=[], required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        genders = People.objects.values_list("gender", flat=True).distinct()
        self.fields["gender"].choices = [(g, g) for g in genders if g]
