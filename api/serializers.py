from django.contrib.auth.models import User, Group
from rest_framework import serializers
from core.models import Sport, Race, Location, Event, Contact, DistanceCategory


class RaceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Race
        fields = ('sport',
                  'event',
                  'title',
                  'date',
                  'distance_cat',
                  'price',
                  'contact',
                  'description',
                  'location',
                  'validated',
                  )


class SportSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Sport
        fields = ('name',
                  'combinedSport',
                  )


class EventSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Event
        fields = ('name',
                  'edition',
                  'website',
                  )


class DistanceCategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = DistanceCategory
        fields = ('sport',
                  'name',
                  'long_name',
                  'order',
                  )


class ContactSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Contact
        fields = ('name',
                  'email',
                  'phone',
                  )


class LocationSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Location
        fields = ('street_number',
                  'route',
                  'locality',
                  'administrative_area_level_1',
                  'administrative_area_level_1_short_name',
                  'administrative_area_level_2',
                  'administrative_area_level_2_short_name',
                  'postal_code',
                  'country',
                  'lat',
                  'lng',
                  )
