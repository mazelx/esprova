from django.views.generic import ListView, DetailView, CreateView
from core.models import Race
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from json import dumps
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point
from core.forms import RaceForm, ContactForm, EventForm, LocationForm


def getRacesAjax(request):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'GET':

        sqs = SearchQuerySet()

        # search from map bounds
        lat_lo = request.GET.get('lat_lo')
        lng_lo = request.GET.get('lng_lo')
        lat_hi = request.GET.get('lat_hi')
        lng_hi = request.GET.get('lng_hi')

        if lat_lo and lng_lo and lat_hi and lng_hi:
            downtown_bottom_left = Point(float(lng_lo), float(lat_lo))
            downtown_top_right = Point(float(lng_hi), float(lat_hi))

            sqs = sqs.within('location', downtown_bottom_left, downtown_top_right)

        # search from search form
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        distances = request.GET.getlist('distances')

        if start_date:
            sqs = sqs.filter(date__gte=start_date)

        if end_date:
            sqs = sqs.filter(date__lte=end_date)

        if distances:
            sqs = sqs.filter(distance_cat__in=distances)

        # search from quick search form
        q = request.GET.get('q')

        if q:
            sqs = sqs.filter(content=q)

        # build the JSON response
        races = []
        result_html = []
        for sr in sqs:
            race_data = {'id': int(sr.pk),
                         'lat': str(sr.get_stored_fields()['location'].get_coords()[1]),
                         'lng': str(sr.get_stored_fields()['location'].get_coords()[0])
                         }

            races.append(race_data)
            result_html.append(sr.get_stored_fields()['rendered'])

        response = {'count': sqs.count(),
                    'races': races,
                    'html': result_html
                    }

        return HttpResponse(dumps(response), content_type="application/json")

    return HttpResponse('404')


# Should be heriting View ... or function not based on a class
class RaceList(ListView):
    model = Race
    context_object_name = "race_list"
    template_name = "core/race_list.html'"


class RaceView(DetailView):
    model = Race
    context_object_name = "race"
    template_name = "core/race.html"


class RaceCreate(CreateView):
    model = Race
    template_name = 'core/create_race.html'
    form_class = RaceForm

    def get(self, request, *args, **kwargs):
        """
        Handles GET requests and instantiates blank versions of the form
        and its inline formsets.
        """
        self.object = None
        form = RaceForm(prefix='race')
        event_form = EventForm(prefix='event')
        location_form = LocationForm(prefix='location')
        contact_form = ContactForm(prefix='contact')

        return self.render_to_response(
            self.get_context_data(form=form,
                                  contact_form=contact_form,
                                  event_form=event_form,
                                  location_form=location_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating a form instance and its inline
        formsets with the passed POST variables and then checking them for
        validity.
        """
        self.object = None
        form = RaceForm(self.request.POST, prefix='race')
        event_form = EventForm(self.request.POST, prefix='event')
        location_form = LocationForm(self.request.POST, prefix='location')
        contact_form = ContactForm(self.request.POST, prefix='contact')
        if(form.is_valid() and event_form.is_valid() and
           location_form.is_valid() and contact_form.is_valid()):
            return self.form_valid(form, event_form, location_form, contact_form)
        else:
            return self.form_invalid(form, event_form, location_form, contact_form)

    def form_valid(self, form, event_form, location_form, contact_form):
        """
        Called if all forms are valid. Creates a Recipe instance along with
        associated Ingredients and Instructions and then redirects to a
        success page.
        """
        rl = location_form.save()
        re = event_form.save()
        rc = contact_form.save()

        self.object = form.save(commit=False)

        self.object.contact = rc
        self.object.event = re
        self.object.location = rl
        self.object.save()

        return HttpResponseRedirect(reverse('list_race'))

    def form_invalid(self, form, event_form, location_form, contact_form):
        """
        Called if a form is invalid. Re-renders the context data with the
        data-filled forms and errors.
        """
        return self.render_to_response(
            self.get_context_data(form=form,
                                  location_form=location_form,
                                  event_form=event_form,
                                  contact_form=contact_form))
