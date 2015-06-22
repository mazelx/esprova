from django.http import HttpResponse, HttpResponseBadRequest
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from rest_framework import viewsets

from api.serializers import *
from api.serializers import RaceSerializer

from haystack.query import SearchQuerySet
from haystack.utils.geo import Point
from haystack.management.commands import update_index

from core.models import Sport, DistanceCategory
from events.models import Race, Location, Event, Contact

import datetime
from json import dumps


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


# simple Ajax calls
def ajx_sport_session(request):
    # if this is a POST request we need to process the form data
    if (request.is_ajax() or settings.DEBUG):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            sport = request.POST.get("sport")
            if Sport.objects.filter(name__iexact=sport).count():
                request.session['selected_sport'] = sport
                return HttpResponse('')
        elif request.method == 'GET':
            sport = request.session['selected_sport']
            return HttpResponse(dumps(sport), content_type="application/json")

    return HttpResponseBadRequest


def ajx_get_distances(request, name):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'GET':

        # first cap to match name case
        sport = get_object_or_404(Sport, name__iexact=name)

        if sport:
            distances = [d.get('name') for d in sport.distances]

        helper_html = render_to_string('core/distance_helper.html', {'sport': sport})
        response = {'helper_html': helper_html,
                    'distances': distances,
                    }

        return HttpResponse(dumps(response), content_type="application/json")


@login_required
def ajx_validate_event(request, pk):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'PUT':
        event = get_object_or_404(Event, pk=pk)
        event.validate()

        # update haystack index to display changes
        update_index.Command().handle(interactive=False)

        messages.success(request, ("Evenement {0} validé").format(event.name))

        return HttpResponse('')
    return HttpResponseBadRequest


@login_required
def ajx_delete_race(request, pk):
    logging.debug(str(request.is_ajax()) + '-' + str(settings.DEBUG) + '-' + str(request.method))
    if (request.is_ajax() or settings.DEBUG) and request.method == 'DELETE':
        race = get_object_or_404(Race, pk=pk)
        race.delete()
        messages.success(request, ("Evenement {0} supprimé").format(event.name))
        return HttpResponse('')
    return HttpResponseBadRequest


def ajx_get_races(request):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'GET':

        sqs = SearchQuerySet()
        sqs = sqs.filter(validated="true")

        # search from quick search form
        sport = request.GET.get('sport')
        if not sport:
            return HttpResponseBadRequest

        sqs = sqs.filter(sport=sport)

        # search from map bounds
        param_viewport = request.GET.get('viewport')
        if param_viewport:
            viewport = [x.strip() for x in param_viewport.split(',')]
            lat_lo = viewport[0]
            lng_lo = viewport[1]
            lat_hi = viewport[2]
            lng_hi = viewport[3]

            if lat_lo and lng_lo and lat_hi and lng_hi:
                downtown_bottom_left = Point(float(lng_lo), float(lat_lo))
                downtown_top_right = Point(float(lng_hi), float(lat_hi))

                sqs = sqs.within('location', downtown_bottom_left, downtown_top_right)

        # search from search form
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        if not start_date:
            start_date = "2015-01-07"
        sqs = sqs.filter(date__gte=start_date)

        if not end_date:
            end_date = "2016-01-06"
        sqs = sqs.filter(date__lte=end_date)

        param_distances = request.GET.get('distances')
        if param_distances:
            distances = [x.strip() for x in param_distances.split(',')]
            sqs = sqs.filter(distance_cat__in=distances)

        # search from quick search form
        search_expr = request.GET.get('q')

        if search_expr:
            sqs = sqs.filter(content=search_expr)

        # sqs.order_by('score')
        sqs = sqs.order_by('date')

        sqs = sqs.facet('distance_cat').facet('administrative_area_level_1').facet('administrative_area_level_2')

        # facet for dates if defined
        sqs = sqs.date_facet(field='date',
                             start_date=datetime.datetime.strptime(start_date, '%Y-%m-%d'),
                             end_date=datetime.datetime.strptime(end_date, '%Y-%m-%d'),
                             gap_by='month')

        facet = sqs.facet_counts()

        # convert datetime into serializable isoformat
        facet_dates = []
        for f in facet['dates']['date']:
            facet_dates.append((f[0].isoformat(), f[1]))
        facet['dates']['date'] = facet_dates

        # build the JSON response
        races = []
        result_html = []

        # Uniqfy the event list (multiple races from an event)
        seen = {}
        rank = 1
        prev_month = cur_month = 0
        month_iterator = 0

        for sr in sqs:
            cur_month = sr.date.strftime('%m%Y')
            event_id = sr.get_stored_fields()['event_id']
            location = sr.get_stored_fields()['location']
            rendered = sr.get_stored_fields()['rendered']

            if event_id in seen:
                continue

            seen[event_id] = 1
            race_data = {'id': int(event_id),
                         'score': str(sr.score),
                         # 'rankClass': "primary" if (rank <= 10) else "secondary",
                         'rankClass': "secondary",
                         'lat': str(location.get_coords()[1]),
                         'lng': str(location.get_coords()[0])
                         }

            races.append(race_data)

            if prev_month != cur_month:
                result_html.append(render_to_string('core/result_month_spacer.html',
                                                    {'last_date': sr.date,
                                                     'count': facet['dates']['date'][month_iterator][1]}))
                month_iterator += 1

            result_html.append(rendered)

            prev_month = cur_month
            rank += 1

        if not races:
            result_html = render_to_string('core/search_no_result_alert.html', {'search_expr': search_expr})

        response = {'count': sqs.count(),
                    'races': races,
                    'html': result_html,
                    'facet': facet,
                    }

        return HttpResponse(dumps(response), content_type="application/json")

    raise Http404
