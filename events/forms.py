from django import forms
from events.models import Event, Race, Location, Contact
import pycountry


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
            'extra_info',
        ]
        widgets = {
            'lat': forms.HiddenInput(),
            'lng': forms.HiddenInput(),
            # 'street_number': forms.HiddenInput(),
            # 'locality': forms.HiddenInput(),
            # 'route': forms.HiddenInput(),
            # 'localsity': forms.HiddenInput(),
            # 'postal_code': forms.HiddenInput(),
            # 'country': forms.HiddenInput(),
        }

    def save(self, force_insert=False, force_update=False, commit=True):
        l = super(LocationForm, self).save(commit=False)

        # get admin level 1 and 2 data from postal code (at least for France)
        dpt = self.cleaned_data['postal_code'][:2]
        try:
            sub = pycountry.subdivisions.get(code=('FR-' + dpt))
            l.administrative_area_level_2_short_name = dpt
            l.administrative_area_level_2 = sub.name
            l.administrative_area_level_1_short_name = sub.parent.code
            l.administrative_area_level_1 = sub.parent.name
        except KeyError:
            l.administrative_area_level_2_short_name = l.country.code
            l.administrative_area_level_2 = l.country.name.title()
            l.administrative_area_level_1_short_name = l.country.code
            l.administrative_area_level_1 = l.country.name.title()

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