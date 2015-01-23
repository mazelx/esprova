from rest_framework import serializers
from core.models import Sport, Race, Location, Event, Contact, DistanceCategory, StageDistanceSpecific, SportStage
from rest_framework.exceptions import ParseError

import logging


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('name',
                  'combinedSport',
                  )
        read_only_fields = ('combinedSport',)


class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ('name',
                  'edition',
                  'website',
                  )


class DistanceCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DistanceCategory
        fields = ('sport',
                  'name',
                  'long_name',
                  'order',
                  )
        read_only_fields = ('sport',
                            'long_name',
                            'order',
                            )


class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('name',
                  'email',
                  'phone',
                  )


class LocationSerializer(serializers.ModelSerializer):
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


class StageSerializer(serializers.ModelSerializer):

    class Meta:
        model = SportStage
        fields = ('name')


class DistanceSerializer(serializers.ModelSerializer):
    stage = serializers.StringRelatedField()

    class Meta:
        model = StageDistanceSpecific
        fields = ('order',
                  'stage',
                  'distance'
                  )


class RaceSerializer(serializers.ModelSerializer):
    sport = SportSerializer()
    event = serializers.StringRelatedField()
    distance_cat = DistanceCategorySerializer()

    # distances = DistanceSerializer()
    contact = ContactSerializer()
    location = LocationSerializer()

    class Meta:
        model = Race
        fields = ('event',
                  'sport',
                  'distance_cat',
                  'title',
                  'date',
                  # 'distances',
                  'price',
                  'contact',
                  'description',
                  'location',
                  'validated',
                  )

        read_only_fields = ('validated', 'distances')

    def create(self, validated_data):
        event = Event.objects.all()[0]
        sport_data = validated_data.pop('sport')
        try:
            sport = Sport.objects.get(**sport_data)
        except Sport.DoesNotExist:
            raise ParseError(
                '{0} is not a known sport, please refer to the API documentation'.format(sport_data['name'])
                )
        distance_cat_data = validated_data.pop('distance_cat')
        try:
            distance_cat = DistanceCategory.objects.get(**distance_cat_data)
        except DistanceCategory.DoesNotExist:
            raise ParseError(
                '{0} is not a known distance category, please refer to the API documentation'.format(
                    distance_cat_data['name']
                    )
                )

        contact_data = validated_data.pop('contact')
        contact, contact_created = Contact.objects.get_or_create(**contact_data)
        location_data = validated_data.pop('location')
        location = Location.objects.create(**location_data)
        race = Race.objects.create(event=event,
                                   contact=contact,
                                   sport=sport,
                                   location=location,
                                   distance_cat=distance_cat,
                                   **validated_data)
        return race
