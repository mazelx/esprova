import requests
import json
import re
from operator import itemgetter
from datetime import datetime
import pytz
import warnings

from core.models import *


class FFTri:
    race_list = []

    def __init__(self, *args, **kwargs):
        self.race_list = self.__get_race_list_from_provider()

    def __get_race_list_from_provider(self):
        post_param = {
            'epreuve_id': '',
            'search_type': 'epreuve',
            'discipline': '',
            'periode_1': 'undefined',
            'periode_2': 'undefined',
            'code_postal': '',
            'annee': '2015',
            'mois': '',
            'nbr_checkbox': '0',
            'format_courte_dist': 'false',
            'format_longue_dist': 'false',
            'format_sprint': 'false',
            'format_super_sprint': 'false',
            'format_decouverte': 'false',
            'format_trail': 'false',
            'format_animation': 'false',
            'format_avenir': 'false',
            'field_club_localite': '',
            'field_club_ligue': '',
        }

        url = 'http://www.fftri.com/sites/all/themes/fftri_artev/templates/pages/includes/carte_epreuve/data.php'

        response = requests.post(url, data=post_param)
        resp_formatted = response.text

        # Replace response stupid encoding ... blame them !
        resp_formatted = resp_formatted.replace("'data'", '"data"')
        resp_formatted = resp_formatted.replace("'count'", '"count"')

        json_data = json.loads(resp_formatted)

        race_list = json_data['data']['photos']
        sorted_list = sorted(race_list, key=itemgetter('nom'))

        return sorted_list

    def save_events(self):
        event_regexp = re.compile('.+(?=\s-\s)')

        for race_src in self.race_list:
            e, s, c, l, dc, r = ({} for i in range(6))
            distance_cat, sport, event, contact, location, race = (None for i in range(6))

            e['name'] = event_regexp.match(race_src.get('nom', None)).group(0)
            e['edition'] = 1
            e['website'] = race_src.get('site')
            # event = Event(**e)

            s['name'] = race_src.get('discipline', None)
            # sport = Sport(**s)

            dc['name'] = race_src.get('format', None)
            # distance_cat = DistanceCategory(**dc)

            r['title'] = race_src.get('nom', None)

            d = race_src.get('date')  # need converting
            r['date'] = pytz.utc.localize(datetime.strptime(d, '%d/%m/%Y'))

            r['price'] = None
            c['name'] = race_src.get('nom_orga', None)
            c['email'] = race_src.get('email', None)
            c['phone'] = race_src.get('telephone', None)
            r['description'] = None
            l['raw'] = race_src.get('adresse', None) + ', FR'
            l['lat'] = race_src.get('latitude', None)
            l['lng'] = race_src.get('longitude', None)

            try:
                distance_cat = DistanceCategory.objects.get(**dc)
                sport = Sport.objects.get(**s)
                event, event_created = Event.objects.get_or_create(**e)
                contact, contact_created = Contact.objects.get_or_create(**c)

                location = Location()
                location.geocode_raw_address(l['raw'])
                # check that location is near lat/lng provided
                location.save()

                race = Race(**r)
                race.distance_cat = distance_cat
                race.event = event
                race.sport = sport
                race.contact = contact
                race.location = location
                race.save()
            except:
                if event:
                    if event.pk:
                        event.delete()
                if contact:
                    if contact.pk:
                        contact.delete()
                if location:
                    if location.pk:
                        location.delete()
                if race:
                    if race.pk:
                        race.delete()

                warnings.warn('cannot save race : {0}'.format(e['name']))






#
        #     event_found = None
        #     # may be replaced by a list comprehension ?? generator ??
        #     for event in event_list:
        #         if event.get('name', None) == event_name:
        #             event_found = event

        #     if event_found:
                
        #     else:
        #         race_fmt = {'sport': {
        #                         "name": sport_name
        #                     },
        #                     'distance_cat': {
        #                         "name": distance_cat_name
        #                     }


        #              'name': event_name, 'races': [race]})

        # return event_list

    def get_event_dict_by_name(self, event_list, event_name):
        return [race for race in event_list if race['name'] == event_name][0]
        # .+(?=\s-\s)
