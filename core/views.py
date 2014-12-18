from django.shortcuts import get_list_or_404
from django.views.generic import ListView, DetailView
from core.models import Race
from django.http import HttpResponse
from django.conf import settings
from django.core import serializers
from django.template import Context
from core.utils import render_block_to_string
from json import dumps


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
            raceset = Race.objects.filter(location__lat__gte=_lat_lo,
                                          location__lng__gte=_lng_lo,
                                          location__lat__lte=_lat_hi,
                                          location__lng__lte=_lng_hi)
            context = Context({"race_list": raceset})
            race_html = render_block_to_string('core/race_list.html', 'racelist', context)

            races = []
            for race in raceset:
                race_data = {'id': race.pk,
                             'lat': str(race.location.lat),
                             'lng': str(race.location.lng)
                             }

                races.append(race_data)

            response = {"html": race_html,
                        "races": races
                        }

            return HttpResponse(dumps(response), content_type="application/json")

        return HttpResponse('404')


class RaceView(DetailView):
    context_object_name = "race"
    model = Race
    template_name = "core/race.html"

