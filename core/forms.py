from django.forms import ModelForm
from django.forms.models import inlineformset_factory
from core.models import Race, Event, Location, Contact


LocationFormSet = inlineformset_factory(Location, Race)
EventFormSet = inlineformset_factory(Event, Race)
ContactFormSet = inlineformset_factory(Contact, Race)


class RaceForm(ModelForm):

    class Meta:
        model = Race
