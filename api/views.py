from core.models import Sport, Race, Location, Event, Contact, DistanceCategory
from rest_framework import viewsets
from api.serializers import *
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializers import RaceSerializer


@api_view(['GET', 'POST'])
def race_list(request):
    """
    List all races, or create a new race.
    """
    if request.method == 'GET':
        races = Race.objects.all()
        serializer = RaceSerializer(races, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = RaceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'PUT', 'DELETE'])
def race_detail(request, pk):
    """
    Retrieve, update or delete a race instance.
    """
    try:
        race = Race.objects.get(pk=pk)
    except race.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = RaceSerializer(race)
        return Response(serializer.data)

    elif request.method == 'PUT':
        serializer = RaceSerializer(race, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == 'DELETE':
        race.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



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


class EventViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Event.objects.all()
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

