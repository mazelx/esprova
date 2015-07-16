import autocomplete_light
from events.models import Organizer


class OrganizerAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ['name']
    model = Organizer
    attrs = {
        # This will set the input placeholder attribute:
        'placeholder': "Veuillez saisir l'organisateur",
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        'class': 'modern-style',
    }

autocomplete_light.register(OrganizerAutocomplete, add_another_url_name='add_another_organizer_create')
