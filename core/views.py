from django.views.generic import ListView, DetailView, CreateView
from core.models import Race, Contact, Location, Event
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.conf import settings
from json import dumps
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point
from core.forms import RaceForm, ContactForm, EventForm, LocationForm
from django.shortcuts import render, render_to_response
from django.contrib.formtools.wizard.views import NamedUrlSessionWizardView
from django.contrib import messages
from django.template import RequestContext


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
        Handles GET requests and instantiates blank versions of the forms
        """
        self.object = None
        race_form = RaceForm(prefix='race')
        event_form = EventForm(prefix='event')
        location_form = LocationForm(prefix='location')
        contact_form = ContactForm(prefix='contact')

        return self.render_to_response(
            self.get_context_data(race_form=race_form,
                                  contact_form=contact_form,
                                  event_form=event_form,
                                  location_form=location_form))

    def post(self, request, *args, **kwargs):
        """
        Handles POST requests, instantiating the form instances with the passed
        POST variables and then checking them for validity.
        """
        race_form = RaceForm(self.request.POST, prefix='race')
        event_form = EventForm(self.request.POST, prefix='event')
        location_form = LocationForm(self.request.POST, prefix='location')
        contact_form = ContactForm(self.request.POST, prefix='contact')

        if race_form.is_valid() and event_form.is_valid() and location_form.is_valid() and contact_form.is_valid():
            race = Race()
            race.date = race_form.cleaned_data["date"]
            race.distance_cat = race_form.cleaned_data["distance_cat"]
            race.sport = race_form.cleaned_data["sport"]


            contact = Contact()
            contact.name = contact_form.cleaned_data["name"]
            contact.email = contact_form.cleaned_data["email"]
            contact.phone = contact_form.cleaned_data["phone"]
            contact.save()



            race.location = location
            race.event = event
            race.contact = contact
            race.save()

            return HttpResponseRedirect(reverse('list_race'))
        else:
            return render(request, 'contact_form.html', {'race': race_form.error})


class RaceWizard(NamedUrlSessionWizardView):
    template_name = 'core/create_race_wizard.html'

    # TEMPLATES = [("event", 'core/create_race_wizard.html'),
    #              ("race", 'core/create_race_wizard.html'),
    #              ("location", 'core/create_race_wizard.html'),
    #              ("contact", 'core/create_race_wizard.html')]

    def create_event(self, event_form):
        event = Event()
        event.name = event_form.cleaned_data["name"]
        event.website = event_form.cleaned_data["website"]
        event.edition = event_form.cleaned_data["edition"]
        event.save()
        return event

    def create_location(self, location_form):
        location = Location()
        location.address1 = location_form.cleaned_data["address1"]
        location.address2 = location_form.cleaned_data["address2"]
        location.zipcode = location_form.cleaned_data["zipcode"]
        location.city = location_form.cleaned_data["city"]
        location.state = location_form.cleaned_data["state"]
        location.country = location_form.cleaned_data["country"]
        location.save()
        return location

    def create_contact(self, contact_form):
        contact = Contact()
        contact.name = contact_form.cleaned_data["name"]
        contact.email = contact_form.cleaned_data["email"]
        contact.phone = contact_form.cleaned_data["phone"]
        contact.save()
        return contact

    def create_race(self, race_form, event, location, contact):
        race = Race()
        race.date = race_form.cleaned_data["date"]
        race.distance_cat = race_form.cleaned_data["distance_cat"]
        race.sport = race_form.cleaned_data["sport"]
        race.location = location
        race.event = event
        race.contact = contact
        race.save()
        return race

    def done(self, form_list, form_dict, **kwargs):
        event_form = form_dict['event']
        race_form = form_dict['race']
        location_form = form_dict['location']
        contact_form = form_dict['contact']

        if all([event_form, race_form, location_form, contact_form]):
            event = self.create_event(event_form)
            location = self.create_location(location_form)
            contact = self.create_contact(contact_form)
            race = self.create_race(race_form=race_form, event=event, contact=contact, location=location)
            if race:
                messages.success(self.request, ("La course {0} a bien été créée".format(event.name)))
                return HttpResponseRedirect(reverse('list_race'))

        messages.error(self.request, ("Something went wrong creating your product."))
        return HttpResponseRedirect(reverse('race_wizard'))
