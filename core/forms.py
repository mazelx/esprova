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
            'sport',
            'distance_cat',
            'date',
            'time',
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input-group datepicker'},
                                    format='%Y-%m-%d'),
            'time': forms.TimeInput(format='%H:%M')
        }
    # # TODO : cascading select box to choo se distances corresponding to a sport


class LocationForm(forms.ModelForm):
    class Meta:
        model = Location
        fields = [
            'street_number',
            'route',
            'locality',
            'administrative_area_level_1',
            'administrative_area_level_2',
            'postal_code',
            'country',

            # hidden
            'administrative_area_level_1_short_name', 
            'administrative_area_level_2_short_name',
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
