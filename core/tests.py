from django.test import TestCase
from core.models import Race, Sport, Event, Contact, DistanceCategory, Location
from django.utils import timezone
from django.test.client import Client
from django.core.urlresolvers import reverse
import json
from nose.tools import *


# Create your tests here.
class RaceTest(TestCase):

    """
    Create an event and a single race
    """
    # fixtures = ['live_test_20140116.yaml']
    fixtures = ['full_example.yaml']
    race = Race

    # def createSimpleRace(self, sport, distance, name, city):
    #     s = Sport
    #     try:
    #         s = Sport.objects.get(name=sport)
    #     except Sport.DoesNotExist:
    #         print("Sport {0} does not exist".format(sport))

    #     dc = DistanceCategory
    #     try:
    #         dc = DistanceCategory.objects.get(name=distance)
    #     except DistanceCategory.DoesNotExist:
    #         print("Distance {0} does not exist".format(distance))

    #     e = Event(name=name, edition=1)
    #     e.save()

    #     c = Contact(name="Pierre Dupont")
    #     c.save()

    #     l = Location(city=city, country="FR")
    #     l.save()

    #     r = Race(
    #         sport=s,
    #         event=e,
    #         date=timezone.now(),
    #         distance_cat=dc,
    #         price=40,
    #         contact=c,
    #         location=l,
    #         )
    #     r.save()

    #     return r

    # def setUp(self):
    #     self.race = self.createSimpleRace(sport="Triathlon",
    #                                       distance="M",
    #                                       name="Triathlon des Gorges de l'ArdÃ¨che",
    #                                       city="Saint-Martin-d'ArdÃ¨che")
    #     self.race = self.createSimpleRace(sport="Triathlon",
    #                                       distance="S",
    #                                       name="Triathlon des Gorges de l'ArdÃ¨che",
    #                                       city="Saint-Martin-d'ArdÃ¨che")
    #     self.race = self.createSimpleRace(sport="Triathlon",
    #                                       distance="XS",
    #                                       name="Triathlon des Gorges de l'ArdÃ¨che",
    #                                       city="Saint-Martin-d'ArdÃ¨che")

    # # MODELS
    # def test_create_race(self):
    #     r = self.createSimpleRace(sport="Triathlon",
    #                               distance="S",
    #                               name="Triathlon Test de Thionville",
    #                               city="Thionville")
    #     self.assertIsNotNone(r)

    # @raises(Exception)
    # def test_create_race_bad_city(self):
    #     r = self.createSimpleRace(sport="Triathlon",
    #                               distance="S",
    #                               name="Triathlon Test de Thionville",
    #                               city="ZZZZZZZ"
    #                               )
    #     self.assertIsNone(r)    


    # MODELS
    def test_sport_model(self):
        s = Sport(name="Trail", combinedSport=False)
        s.save()
        self.assertIsNotNone(s.pk)

    def test_location_model(self):
        l1 = Location(street_number="3",
                      route="impasse des argelas",
                      locality="Le Teil",
                      postal_code="07400",
                      coutry="FR",
                      lat=44.5523379,
                      lng=4.6755323)
        l1.save()

        l2 = Location().geocode_raw_address()
        self.assertEquals(l1.getPoint(), l2.getPoint())


    # VIEWS
    def test_basic_quick_search(self):
        " Test if a basic quick search return something "

        # change the header in order to simulate ajax call
        res = Client().get(reverse('search_race'),
                           {'q': 'montélimar'},
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        
        self.assertIsNotNone(res.content)
        data = json.loads(res.content.decode('utf-8'))
        self.assertGreater(data['count'], 0)

    def test_date_search(self):
        res = Client().get(reverse('search_race'),
                           {'start_date': timezone.now().strftime('%Y-%m-%d')},
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(res.content.decode('utf-8'))
        self.assertGreater(data['count'], 0)

    def test_location_search(self):
        res = Client().get(reverse('search_race'),
                           {'lat_lo': 0.024653,
                            'lng_lo': 0.933466,
                            'lat_hi': 50.298241,
                            'lng_hi': 50.10351},
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(res.content.decode('utf-8'))
        self.assertGreater(data['count'], 0)