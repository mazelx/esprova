import autocomplete_light
from events.models import Organizer, Label, Challenge
from django.conf import settings


class AutocompleteCustom(autocomplete_light.AutocompleteModelBase):
    choice_html_format = '''<span class="div" data-value="%s">
                                <a href="%s" target="_blank">%s</a>
                            </span>
                             '''

    def choice_html(self, choice):
        """
        Return a choice formated according to self.choice_html_format.
        """
        choice_format = '<span class="div" data-value="%s">%s</span>'
        try:
            return self.choice_html_format % (self.choice_value(choice),
                                              choice.get_absolute_url(),
                                              self.choice_label(choice)
                                              )
        except:
            return choice_format % (self.choice_value(choice), self.choice_label(choice))


class OrganizerAutocomplete(AutocompleteCustom):
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


class LabelAutocomplete(AutocompleteCustom):
    search_fields = ['name']
    model = Label
    attrs = {
        # This will set the input placeholder attribute:
        'placeholder': "ex. Ironman, ...",
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        'class': 'modern-style',
    }
autocomplete_light.register(LabelAutocomplete, add_another_url_name='add_another_label_create')


class ChallengeAutocomplete(AutocompleteCustom):
    search_fields = ['name']
    model = Challenge
    attrs = {
        # This will set the input placeholder attribute:
        'placeholder': "ex. Championnat D1, ...",
        # This will set the yourlabs.Autocomplete.minimumCharacters
        # options, the naming conversion is handled by jQuery
        'data-autocomplete-minimum-characters': 1,
    }
    widget_attrs = {
        'data-widget-maximum-values': 4,
        # Enable modern-style widget !
        'class': 'modern-style',
    }
autocomplete_light.register(ChallengeAutocomplete, add_another_url_name='add_another_challenge_create')
