from django.forms import ModelForm
from core.models import Race, Event, Location, Contact


class EventForm(ModelForm):

    class Meta:
        model = Event
        exclude = []


class RaceForm(ModelForm):

    class Meta:
        model = Race
        fields = ['sport', 'distance_cat', 'date']


class LocationForm(ModelForm):

    class Meta:
        model = Location
        exclude = ['lat', 'lng']


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        exclude = []

