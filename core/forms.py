from django import forms
from core.models import Event, Race, Location, Contact, Sport
import pycountry
import pdb

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
            'postal_code',
            'country',

            # hidden
            # 'administrative_area_level_1_short_name',
            # 'administrative_area_level_2_short_name',
            # 'administrative_area_level_1',
            # 'administrative_area_level_2',
            'lat',
            'lng',
        ]
        widgets = {
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        l = super(LocationForm, self).save(commit=False)
        # pdb.set_trace()

        # get admin level 1 and 2 data from postal code (at least for France)
        dpt = self.cleaned_data['postal_code'][:2]
        sub = pycountry.subdivisions.get(code=('FR-' + dpt))
        l.administrative_area_level_2_short_name = dpt
        l.administrative_area_level_2 = sub.name
        l.administrative_area_level_1_short_name = sub.parent.code
        l.administrative_area_level_1 = sub.parent.name
        # l.save(commit=False)  

        if commit:
            l.save()
        return l


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            'name',
            'email',
            'phone',
        ]
