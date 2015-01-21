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
    # date = forms.DateField()
    # sport = forms.ModelChoiceField(Sport.objects.all())
    # # TODO : cascading select box to choose distances corresponding to a sport
    # distance_cat = forms.ModelChoiceField(DistanceCategory.objects.all())


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

# class LocationForm(forms.Form):
#     street_number = forms.CharField(max_length=10, required=False)
#     route = forms.CharField(max_length=200, required=False)
#     locality = forms.CharField(max_length=100)
#     administrative_area_level_1 = forms.CharField(max_length=100)
#     administrative_area_level_1_short_name = forms.CharField(max_length=10)
#     administrative_area_level_2 = forms.CharField(max_length=100)
#     administrative_area_level_2_short_name = forms.CharField(max_length=10)
#     postal_code = forms.CharField(max_length=16)
#     country = forms.ChoiceField(list(countries))

#     lat = forms.DecimalField(max_digits=8, decimal_places=5)
#     lng = forms.DecimalField(max_digits=8, decimal_places=5)


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'phone',
        ]
