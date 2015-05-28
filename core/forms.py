from django import forms
from core.models import Event, Race, Location, Contact, Sport


# model forms ????

class ConnexionForm(forms.Form):
    username = forms.CharField(label="Nom d'utilisateur", max_length=30)
    password = forms.CharField(label="Mot de passe", widget=forms.PasswordInput)


class SportForm(forms.ModelForm):
    name = forms.CharField(widget=forms.Select)


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'website',
            'edition',
        ]


class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = [
            'date',
            'time',
            'sport',
            'distance_cat'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input-group datepicker'},
                                    format='%Y-%m-%d'),
            'time': forms.TimeInput(format='%I:%M %p')
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
