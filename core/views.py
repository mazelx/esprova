from django.views.generic import ListView, DetailView
from core.models import Race
from django.http import HttpResponse
from django.conf import settings
from json import dumps
from core.forms import RaceQuickSearchForm, RaceSearchForm
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

    response = {"html": result_html,
                "races": races
                }

    return HttpResponse(dumps(response), content_type="application/json")


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

            return render_search_result(sqs)

        return HttpResponse('404')

    def getRacesFromQuickSearch(request):
        if request.is_ajax() or settings.DEBUG:
             # we retrieve the query to display it in the template
            form = RaceQuickSearchForm(request.GET)

            # we call the search method from the NotesSearchForm. Haystack do the work!
            sqs = form.search()

            return render_search_result(sqs)

        return HttpResponse('404')

    def getRacesFromSearch(request):
        if request.method == 'GET':
            form = RaceSearchForm(request.GET)

            if form.is_valid():
                sqs = SearchQuerySet()
                if form.cleaned_data['start_date']:
                    sqs = sqs.filter(date__gte=form.cleaned_data['start_date'])

                # Check to see if an end_date was chosen.
                if form.cleaned_data['end_date']:
                    sqs = sqs.filter(date__lte=form.cleaned_data['end_date'])

            return render_search_result(sqs)

        return HttpResponse('404')


class RaceView(DetailView):
    context_object_name = "race"
    model = Race
    template_name = "core/race.html"

