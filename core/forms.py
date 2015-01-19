from django import forms
from core.models import Sport, DistanceCategory
from django_countries import countries


class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class EventForm(forms.Form):
    name = forms.CharField(max_length=100)
    edition = forms.IntegerField()
    website = forms.URLField(required=False)


class RaceForm(forms.Form):
    date = forms.DateField()
    sport = forms.ModelChoiceField(Sport.objects.all())
    # TODO : cascading select box to choose distances corresponding to a sport
    distance_cat = forms.ModelChoiceField(DistanceCategory.objects.all())


class LocationForm(forms.Form):
    # address1 = forms.CharField(max_length=200, required=False)
    # address2 = forms.CharField(max_length=200, required=False)
    # zipcode = forms.CharField(max_length=16, required=False)
    # city = forms.CharField(max_length=100)
    # state = forms.CharField(max_length=100, required=False)

    street_number = forms.CharField(max_length=10, required=False)
    route = forms.CharField(max_length=200, required=False)
    locality = forms.CharField(max_length=100)
    administrative_area_level_1 = forms.CharField(max_length=100)
    administrative_area_level_1_short_name = forms.CharField(max_length=10)
    administrative_area_level_2 = forms.CharField(max_length=100)
    administrative_area_level_2_short_name = forms.CharField(max_length=10)
    postal_code = forms.CharField(max_length=16)
    country = forms.ChoiceField(list(countries))

    lat = forms.DecimalField(max_digits=8, decimal_places=5)
    lng = forms.DecimalField(max_digits=8, decimal_places=5)


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=10, required=False)
