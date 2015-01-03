from django.views.generic import ListView, DetailView
from core.models import Race
from django.http import HttpResponse
from django.conf import settings
from json import dumps
from core.forms import RaceQuickSearchForm
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point


# Comment mettre cette putain de fonction dans la classe RaceList ???
def render_search_result(sqs):
    races = []
    result_html = []
    for sr in sqs:
        race_data = {'id': int(sr.pk),
                     'lat': str(sr.get_stored_fields()["location"].get_coords()[1]),
                     'lng': str(sr.get_stored_fields()["location"].get_coords()[0])
                     }

        races.append(race_data)
        result_html.append(sr.get_stored_fields()["rendered"])

    response = {"results": sqs.count(),
                "races": races,
                "html": result_html
                }

    return HttpResponse(dumps(response), content_type="application/json")


class RaceList(ListView):
    model = Race
    context_object_name = "race_list"
    template_name = "core/race_list.html'"

    def getRacesFromQuickSearch(request):
        if request.is_ajax() or settings.DEBUG:
            form = RaceQuickSearchForm(request.GET)
            sqs = form.search()

            return render_search_result(sqs)

        return HttpResponse('404')

    def getRacesFromSearch(request):
        if request.method == 'GET':
            sqs = SearchQuerySet()

            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')
            distances = request.GET.getlist('distances')

            if start_date:
                sqs = sqs.filter(date__gte=start_date)

            if end_date:
                sqs = sqs.filter(date__lte=end_date)

            if distances:
                sqs = sqs.filter(distance_cat__in=distances)

            return render_search_result(sqs)

        return HttpResponse('404')

  def getRacesFromMapBounds(request):
        if request.is_ajax() or settings.DEBUG:
            _lat_lo = request.GET.get('lat_lo')
            _lng_lo = request.GET.get('lng_lo')
            _lat_hi = request.GET.get('lat_hi')
            _lng_hi = request.GET.get('lng_hi')

            downtown_bottom_left = Point(float(_lng_lo), float(_lat_lo))
            downtown_top_right = Point(float(_lng_hi), float(_lat_hi))

            sqs = SearchQuerySet().within('location', downtown_bottom_left, downtown_top_right)

            return render_search_result(sqs)

        return HttpResponse('404')

class RaceView(DetailView):
    context_object_name = "race"
    model = Race
    template_name = "core/race.html"

