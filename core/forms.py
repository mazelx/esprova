from django import forms
from core.models import Sport, DistanceCategory, Event, Race, Location, Contact
from django_countries import countries


# model forms ????

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name', 
            'edition',
            'website',
        ]


class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = [
            'date',
            'sport',
            'distance_cat'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input-group datepicker'}),
        }
    # # TODO : cascading select box to choose distances corresponding to a sport


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'street_number',
            'route',
            'locality',
            'administrative_area_level_1',
            'administrative_area_level_1_short_name',
            'administrative_area_level_2',
            'administrative_area_level_2_short_name',
            'postal_code',
            'country',
            'lat',
            'lng',
        ]


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'phone',
        ]
