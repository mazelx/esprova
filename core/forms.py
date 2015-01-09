from django import forms
from core.models import Sport, DistanceCategory
from django_countries import countries


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
    address1 = forms.CharField(max_length=200, required=False)
    address2 = forms.CharField(max_length=200, required=False)
    zipcode = forms.CharField(max_length=16, required=False)
    city = forms.CharField(max_length=100)
    state = forms.CharField(max_length=100, required=False)
    country = forms.ChoiceField(list(countries))


class ContactForm(forms.Form):
    name = forms.CharField(max_length=100)
    email = forms.EmailField(required=False)
    phone = forms.CharField(max_length=10, required=False)
