import requests
import json
import re
from operator import itemgetter
from pytz import timezone
from datetime import datetime
import sys
import traceback


from core.models import Race, Event, Location, Contact, DistanceCategory, Sport, Organizer, Federation


class RaceDoubleException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return self.msg


class FFTri:
    """
        Interface with the FFTri.com race data
        The data DOES NOT come from a public API, therefore the data structure will probably change over time

    """
    race_list = []
    url = 'http://www.fftri.com/sites/all/themes/fftri_artev/templates/pages/includes/carte_epreuve/data.php'
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

    def __init__(self, *args, **kwargs):
        self.race_list = self.__get_race_list_from_provider()
        self.__clean_race_list()


    def __get_race_list_from_provider(self):
        

        response = requests.post(self.url, data=self.post_param)
        resp_formatted = response.text

        # Replace response stupid encoding ... blame them !
        resp_formatted = resp_formatted.replace("'data'", '"data"')
        resp_formatted = resp_formatted.replace("'count'", '"count"')

        json_data = json.loads(resp_formatted)

        race_list = json_data['data']['photos']
        race_list = [race for key, race in race_list.items()]

        sorted_list = sorted(race_list, key=itemgetter('nom'))

        return sorted_list

    def __clean_race_list(self):
        for x in self.race_list:
            if('Jeunes' in x['format']):
                x['discipline'] += ' Jeunes'
                sport = Sport.objects.filter(name=x['discipline'])
                dc = DistanceCategory.objects.filter(sport=sport, long_name__contains=x['format'])
                if dc.count():
                    x['format'] = dc[0].name
                else:
                    x['format'] = ''
            if('XXL' in x['format']):
                x['format'] = 'XL'
            if('XXS' in x['format']):
                x['format'] = 'XS'


    def import_events_in_app(self, sport_restrict, geocode=True, limit=0):
        nb_created, nb_failed = 0, 0
        event_re = re.compile('.+(?=\s-\s)')
        address_re = re.compile('(.+)(?=\s-\s\D)')
        locality_re = re.compile('(?<=\s-\s)(.+)(?=\s-\s\w)')
        federation_name = "FFTri"
        edition_no = 1

        restricted_race_list = self.race_list
        if sport_restrict:
            restricted_race_list = [x for x in restricted_race_list
                                    if x['discipline'].lower() == sport_restrict.lower()]

        for race_src in restricted_race_list:
            e, s, c, l, dc, r, o, f = ({} for i in range(8))
            distance_cat, sport, event, contact, location, race, organizer, federation = (None for i in range(8))

            race_src_id = race_src.get('id', None)

            f['name'] = federation_name

            e['name'] = event_re.search(race_src.get('nom', None)).group(0)
            e['website'] = race_src.get('site')
            e['edition'] = edition_no
            # event = Event(**e)

            s['name'] = race_src.get('discipline', None)
            # sport = Sport(**s)

            dc['name'] = race_src.get('format', None)
            # distance_cat = DistanceCategory(**dc)

            r['title'] = race_src.get('nom', None)

            d = race_src.get('date')
            r['date'] = datetime.strptime(d, '%d/%m/%Y')
            r['date'] = r['date'].replace(tzinfo=timezone('Europe/Paris'))

            r['price'] = None

            # edition info
            r['created_by'] = "FFTri"
            r['import_source'] = "FFTri"
            r['import_source_id'] = race_src_id

            o['name'] = race_src.get('nom_orga', None)
            c['name'] = race_src.get('nom_orga', None)
            c['email'] = race_src.get('email', None)
            c['phone'] = race_src.get('telephone', None)
            r['description'] = None
            l['raw'] = race_src.get('adresse', None)
            l['postal_code'] = race_src.get('cp', None)
            l['lat'] = race_src.get('latitude', None)
            l['lng'] = race_src.get('longitude', None)

            try:

                # check if the race is already in the db to avoid useless treatment
                has_error = False
                sport = Sport.objects.get(**s)
                distance_cat = DistanceCategory.objects.get(sport=sport, **dc)
                organizer, organizer_created = Organizer.objects.get_or_create(**o)
                # event_ref, event_created = EventReference.objects.get_or_create(organizer=organizer, **eref)
                event, event_created = Event.objects.get_or_create(organizer=organizer, **e)
                contact = Contact.objects.create(**c)
                federation, federation_created = Federation.objects.get_or_create(**f)

                location = Location()

                geocoded = False

                if geocode:
                    country = 'FR'
                    adm2_short = l['postal_code'][:2]

                    if l['postal_code'][:3] == '971':
                        # guadeloupe
                        country = 'GP'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '972':
                        # martinique
                        country = 'MQ'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '973':
                        # guyane
                        country = 'GF'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '974':
                        # réunion
                        country = 'RE'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '975':
                        # saint pierre et miquelon
                        country = 'PM'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '976':
                        # mayotte
                        country = 'YT'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '984':
                        # terres australes ... on sait jamais
                        country = 'TF'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '986':
                        # wallis et futuna
                        country = 'WF'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '987':
                        # polynesie francaise
                        country = 'PF'
                        adm2_short = l['postal_code'][:3]
                    elif l['postal_code'][:3] == '988':
                        # nouvellae caledonie
                        country = 'NC'
                        adm2_short = l['postal_code'][:3]

                    geocoded = location.geocode_raw_address(raw_address=l['raw'], postal_code=l['postal_code'], country=country)

                    # fix for google geocoder bug for some french departments
                    # replace postal code and departement with API value
                    location.postal_code = l['postal_code']
                    location.administrative_area_level_2_short_name = adm2_short

                    # in case the geocode did not find location, switch back to given infos
                
                if not geocoded:
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
                nb_created += 1

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
                exc_type, exc_value, exc_traceback = sys.exc_info()
                lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
                print ("[ERR][UNK] [{0}] :".format(race_src_id))
                print (''.join('!! ' + line for line in lines))

            finally:
                if has_error:
                    nb_failed += 1
                    if event:
                        if event.pk:
                            if len(event.get_races()) == 0:
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
                # else:
                    # print ("[INF][OK] [{0}] : Race event successfully created".format(race_src_id))

                if limit == 1:
                    break
                limit -= 1



        print ('finished !  created: {0}, failed: {1}'.format(nb_created, nb_failed))


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

    def get_race_from_id(self, id):
        return [r for r in self.race_list if r['id'] == id]

    def get_race_from_name(self, name):
        return [r for r in self.race_list if name.lower() in r['nom'].lower()]

