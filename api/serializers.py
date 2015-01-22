from rest_framework import serializers
from core.models import Sport, Race, Location, Event, Contact, DistanceCategory, StageDistanceSpecific, SportStage


class SportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sport
        fields = ('name',
                  'combinedSport',
                  )


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
    stage = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = StageDistanceSpecific
        fields = ('order',
                  'stage',
                  'distance'
                  )


class RaceSerializer(serializers.ModelSerializer):
    sport = serializers.StringRelatedField(read_only=True)
    event = serializers.StringRelatedField(read_only=True)
    distance_cat = serializers.StringRelatedField(read_only=True)

    distances = DistanceSerializer(many=True)
    contact = ContactSerializer()
    location = LocationSerializer()

    class Meta:
        model = Race
        fields = ('sport',
                  'event',
                  'title',
                  'date',
                  'distance_cat',
                  'distances',
                  'price',
                  'contact',
                  'description',
                  'location',
                  'validated',
                  )

        read_only_fields = ('validated',)

