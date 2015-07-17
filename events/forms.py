from django import forms
from events.models import Event, Race, Location, Contact, Organizer
import pycountry
import autocomplete_light

autocomplete_light.autodiscover()


class EventForm(autocomplete_light.ModelForm):
    class Meta:
        model = Event
        fields = [
            'name',
            'website',
            'edition',
            'organizer',
        ]
        # organizer = autocomplete_light.GenericModelChoiceField('OrganizerAutocomplete')

        # autocomplete_names = {'organizer': 'OrganizerAutocomplete'}
        # autocomplete_fields = ('organizer')


class OrganizerForm(forms.ModelForm):
    class Meta:
        model = Organizer


class RaceForm(forms.ModelForm):
    class Meta:
        model = Race
        fields = [
            'sport',
            'distance_cat',
            'date',
            'time',
            'description',
            'relay',
            'timetrial'
        ]
        widgets = {
            'date': forms.DateInput(attrs={'class': 'input-group datepicker', 'placeholder': 'aaaa-mm-jj'},
                                    format='%Y-%m-%d'),
            'time': forms.TimeInput(format='%H:%M', attrs={'placeholder': 'hh:mm'}),
            'description': forms.Textarea(attrs={'placeholder': 'Décrivez la course en quelques mots'})
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