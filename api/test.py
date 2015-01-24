from django.test import TestCase
from django.utils import timezone
from django.test.client import Client
from django.core.urlresolvers import reverse
from nose.tools import *

from core.models import *

from api.serializers import *
from api.views import *

from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from django.utils.six import BytesIO





class APITest(TestCase):
    # fixtures = ['live_test_20140116.yaml']
    fixtures = ['full_example.yaml']


    def test_serialize_deserialize_event(self):
        event = Event.objects.all()[0]
        s_in = EventSerializer(event)
        json_data = JSONRenderer().render(s_in.data)

        # ----
        stream = BytesIO(json_data)

        out_data = JSONParser().parse(stream)
        s_out = EventSerializer(data=out_data)

        self.assertTrue(s_out.is_valid())
        # self.assertEquals(s_in, s_out)

    def test_api_post_event(self):
        json_file = open("/www/esprova/api/json_sample/api_event_sample.json", "rb")
        data = JSONParser().parse(json_file)

        s = EventSerializer(data=data)
        self.assertTrue(s.is_valid())

        instance = s.save()
        # is saved
        self.assertIsNotNone(instance.pk)

        # has a race object
        self.assertIsNotNone(instance.races.all()[0].pk)
