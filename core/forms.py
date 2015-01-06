from django.forms import ModelForm
from core.models import Race, Event, Location, Contact


class EventForm(ModelForm):

    class Meta:
        model = Event


class RaceForm(ModelForm):

    class Meta:
        model = Race
        fields = ['sport', 'distance_cat']


class LocationForm(ModelForm):

    class Meta:
        model = Location
        fields = ['address1', 'address2', 'zipcode', 'city', 'state', 'country']


class ContactForm(ModelForm):

    class Meta:
        model = Contact

