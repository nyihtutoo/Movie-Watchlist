from django import forms

from .models import Movie


class MovieForm(forms.ModelForm):
    """Form used for both adding and editing a movie."""

    class Meta:
        model = Movie
        fields = ["title", "genre", "release_year", "personal_rating", "watched"]
        widgets = {
            "title": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. Inception"}
            ),
            "genre": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "e.g. Sci-Fi"}
            ),
            "release_year": forms.NumberInput(
                attrs={"class": "form-control", "placeholder": "e.g. 2010"}
            ),
            "personal_rating": forms.NumberInput(
                attrs={"class": "form-control", "min": 1, "max": 5}
            ),
            "watched": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

    def clean_title(self):
        title = self.cleaned_data.get("title", "").strip()
        if not title:
            raise forms.ValidationError("Title is required.")
        return title
