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
    fixtures = ['triathlon.json']
    race = Race

    def createSimpleRace(self, sport, distance, name, city):
        s = Sport
        try:
            s = Sport.objects.get(name=sport)
        except Sport.DoesNotExist:
            print("Sport {0} does not exist".format(sport))

        dc = DistanceCategory
        try:
            dc = DistanceCategory.objects.get(name=distance)
        except DistanceCategory.DoesNotExist:
            print("Distance {0} does not exist".format(distance))

        e = Event(name=name, edition=1)
        e.save()

        c = Contact(name="Pierre Dupont")
        c.save()

        l = Location(city=city, country="FR")
        l.save()

        r = Race(
            sport=s,
            event=e,
            date=timezone.now(),
            distance_cat=dc,
            price=40,
            contact=c,
            location=l,
            )
        r.save()

        return r

    def setUp(self):
        self.race = self.createSimpleRace(sport="Triathlon",
                                          distance="M",
                                          name="Triathlon des Gorges de l'Ardèche",
                                          city="Saint-Martin-d'Ardèche")
        self.race = self.createSimpleRace(sport="Triathlon",
                                          distance="S",
                                          name="Triathlon des Gorges de l'Ardèche",
                                          city="Saint-Martin-d'Ardèche")
        self.race = self.createSimpleRace(sport="Triathlon",
                                          distance="XS",
                                          name="Triathlon des Gorges de l'Ardèche",
                                          city="Saint-Martin-d'Ardèche")

    # MODELS
    def test_create_race(self):
        r = self.createSimpleRace(sport="Triathlon",
                                  distance="S",
                                  name="Triathlon Test de Thionville",
                                  city="Thionville")
        self.assertIsNotNone(r)

    @raises(Exception)
    def test_create_race_bad_city(self):
        r = self.createSimpleRace(sport="Triathlon",
                                  distance="S",
                                  name="Triathlon Test de Thionville",
                                  city="ZZZZZZZ"
                                  )
        self.assertIsNone(r)    

    # VIEWS

    def test_basic_quick_search(self):
        " Test if a basic quick search return something "

        # change the header in order to simulate ajax call
        res = Client().get(reverse('search_race'),
                           {'q': 'triathlon'},
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(res.content.decode('utf-8'))
        self.assertGreater(data['count'], 0)

    def test_date_search(self):
        res = Client().get(reverse('search_race'),
                           {'start_date': timezone.now().strftime('%Y-%m-%d')},
                           HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data = json.loads(res.content.decode('utf-8'))
        self.assertGreater(data['count'], 0)
