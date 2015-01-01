from django.test import TestCase
from core.models import Race, Sport, Event, Contact, DistanceCategory
from datetime import datetime
from django.test.client import RequestFactory
from core.forms import RaceSearchForm

# Create your tests here.
class RaceTest(TestCase):
    """
    Create an event and a single race
    """
    fixtures = ['triathlon.json']
    race = Race

    def setUp(self):
        # initTriathlon()
        self.race = self.createSimpleRace(sport="Triathlon", distance="M", name="Triathlon des Gorges de l'Ardèche")
        self.race = self.createSimpleRace(sport="Triathlon", distance="S", name="Triathlon des Gorges de l'Ardèche")
        self.race = self.createSimpleRace(sport="Triathlon", distance="XS", name="Triathlon des Gorges de l'Ardèche")

    def createSimpleRace(self, sport, distance, name):
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

        e = Event(name=name)
        e.save()

        c = Contact(name="Pierre Dupont")
        c.save()

        r = Race(
            sport=s,
            event=e,
            edition=1,
            date=datetime(2015, 6, 6, 12, 30),
            distance_cat=dc,
            price=40,
            contact=c
            )
        r.save()

        return r

    def test_db_has_one_race(self):
        print(Race.objects.all()[0])
        self.assertIsNotNone(Race.objects.all()[0])

    def test_search_triathlon(self):
        rf = RequestFactory()
        req = rf.get('http://localhost:8000/cherche/?q=triathlon+gorges')
        form = RaceSearchForm(req.GET)
        form.search()
        # Todo: assert is empty
