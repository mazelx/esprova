import requests
import json
import re
from operator import itemgetter
import pytz
from datetime import datetime
import warnings

from core.models import Race, Event, Location, Contact, DistanceCategory, Sport, Organizer, Federation


class RaceDoubleException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


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

    def save_events(self, geocode=True):
        event_re = re.compile('.+(?=\s-\s)')
        address_re = re.compile('(.+)(?=\s-\s\D)')
        locality_re = re.compile('(?<=\s-\s)(.+)(?=\s-\s\w)')
        federation_name = "FFTri"

        for race_src in self.race_list:
            e, s, c, l, dc, r, o, f = ({} for i in range(8))
            distance_cat, sport, event, contact, location, race, organizer, federation = (None for i in range(8))

            race_src_id = race_src.get('id', None)

            f['name'] = federation_name

            e['name'] = event_re.search(race_src.get('nom', None)).group(0)
            e['edition'] = 1
            e['website'] = race_src.get('site')
            # event = Event(**e)

            s['name'] = race_src.get('discipline', None)
            # sport = Sport(**s)

            dc['name'] = race_src.get('format', None)
            # distance_cat = DistanceCategory(**dc)

            r['title'] = race_src.get('nom', None)

            d = race_src.get('date') 
            r['date'] = pytz.utc.localize(datetime.strptime(d, '%d/%m/%Y'))

            r['price'] = None
            o['name'] = race_src.get('nom_orga', None)
            c['name'] = race_src.get('nom_orga', None)
            c['email'] = race_src.get('email', None)
            c['phone'] = race_src.get('telephone', None)
            r['description'] = None
            l['raw'] = race_src.get('adresse', None) + ', FR'
            l['postal_code'] = race_src.get('cp', None)
            l['lat'] = race_src.get('latitude', None)
            l['lng'] = race_src.get('longitude', None)

            try:
                has_error = False
                distance_cat = DistanceCategory.objects.get(**dc)
                sport = Sport.objects.get(**s)
                organizer, organizer_created = Organizer.objects.get_or_create(**o)
                event, event_created = Event.objects.get_or_create(organizer=organizer, **e)
                contact, contact_created = Contact.objects.get_or_create(**c)
                federation, federation_created = Federation.objects.get_or_create(**f)

                location = Location()
                if geocode:
                    location.geocode_raw_address(l['raw'])
                else:
                    location.lat = l['lat']
                    location.lng = l['lng']
                    location.postal_code = l['postal_code']
                    address = race_src.get('adresse', None)
                    if not address:
                        raise Exception("no address provided")

                    if address_re.search(race_src.get('adresse', None)):
                        location.route = address_re.search(address).group(0)
                    if locality_re.search(race_src.get('adresse', None)):
                        location.locality = locality_re.search(address).group(0)

                # check that location is near lat/lng provided
                location.save()

                race = Race(**r)
                race.event = event

                race.distance_cat = distance_cat
                race.federation = federation
                race.sport = sport
                race.contact = contact
                race.location = location

                if race.get_potential_doubles():
                    raise RaceDoubleException("Double detected")

                race.save()

            except Sport.DoesNotExist:
                has_error = True
                print ("[ERR][REF] [{0}] : Sport {1} does not exist".format(race_src_id, s['name']))
            except DistanceCategory.DoesNotExist:
                has_error = True
                print ("[ERR][REF] [{0}] : Distance {1} does not exist".format(race_src_id, dc['name']))
            except RaceDoubleException:
                has_error = True
                print ("[WAR][DBL] [{0}] : Race already exists in DB".format(race_src_id))

            except Exception as e:
                has_error = True
                print ("[ERR][UNK] [{0}] : {1}".format(race_src_id, str(e)))

            finally:
                if has_error:
                    # NO ! Cannot just delete event if a race is not ok...
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
                else:
                    print ("[INF][OK] [{0}] : Race event successfully created".format(race_src_id))






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
