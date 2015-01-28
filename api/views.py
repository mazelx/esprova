from core.models import Sport, Race, Location, EventReference, Contact, DistanceCategory
from rest_framework import viewsets
from api.serializers import *
from api.serializers import RaceSerializer



class RaceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Race.objects.all()
    serializer_class = RaceSerializer


class SportViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Sport.objects.all()
    serializer_class = SportSerializer


class EventReferenceViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = EventReference.objects.all()
    serializer_class = EventSerializer


class ContactViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer


class LocationViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Location.objects.all()
    serializer_class = LocationSerializer


class DistanceCategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = DistanceCategory.objects.all()
    serializer_class = DistanceCategorySerializer

