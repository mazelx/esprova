from django.shortcuts import get_list_or_404, render
from django.views.generic import ListView, DetailView
from core.models import Race
from django.http import HttpResponse
from django.conf import settings
from django.core import serializers
from django.template import Context
from core.utils import render_block_to_string
from json import dumps
from core.forms import RaceSearchForm
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point


class RaceList(ListView):
    model = Race
    context_object_name = "race_list"
    template_name = "core/race_list.html'"

    def getRacesFromMapBounds(request):

        if request.is_ajax() or settings.DEBUG:
            _lat_lo = request.GET.get('lat_lo')
            _lng_lo = request.GET.get('lng_lo')
            _lat_hi = request.GET.get('lat_hi')
            _lng_hi = request.GET.get('lng_hi')

            downtown_bottom_left = Point(float(_lng_lo), float(_lat_lo))
            downtown_top_right = Point(float(_lng_hi), float(_lat_hi))

            sqs = SearchQuerySet().within('location', downtown_bottom_left, downtown_top_right)

            races = []
            result_html = []
            for sr in sqs:
                race_data = {'id': int(sr.pk),
                             'lat': str(sr.get_stored_fields()["location"].get_coords()[0]),
                             'lng': str(sr.get_stored_fields()["location"].get_coords()[1])
                             }

                races.append(race_data)
                result_html.append(sr.get_stored_fields()["rendered"])

            response = {"html": result_html,
                        "races": races
                        }

            return HttpResponse(dumps(response), content_type="application/json")

        return HttpResponse('404')

    def getRacesFromSearch(request):
         # we retrieve the query to display it in the template
        form = RaceSearchForm(request.GET)

        # we call the search method from the NotesSearchForm. Haystack do the work!
        sqs = form.search()

        return render(request, 'search/search.html', {
            # 'search_query' : search_query,
            'races': sqs,
            })



class RaceView(DetailView):
    context_object_name = "race"
    model = Race
    template_name = "core/race.html"

