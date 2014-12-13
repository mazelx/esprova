from django.test import TestCase
from core.models import Race, Sport, Event, Contact, DistanceCategory
from datetime import datetime
from django.core import serializers

# Create your tests here.
class RaceTest(TestCase):
    """
    Create an event and a single race
    """
    fixtures = ['triathlon.json']

    r = Race

    def setUp(self):
        # initTriathlon()
        sport = Sport.objects.get(name="Triathlon")
        distance_cat = DistanceCategory.objects.get(name="M")

        e = Event(name="Triathlon des Gorges de l'Ardèche")
        e.save()
        c = Contact(name="Bruno Damiens")
        c.save()

        r = Race(
            sport=sport,
            event=e,
            edition=1,
            date=datetime(2015, 6, 6, 12, 30),
            distance_cat=distance_cat,
            price=40,
            contact=c
            )
        r.save()

    def test_db_has_one_race(self):
        print(Race.objects.all()[0])
        self.assertIsNotNone(Race.objects.all()[0])
