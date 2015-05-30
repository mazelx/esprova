from django.http import Http404
from django.views.generic import ListView, DetailView, TemplateView
from core.models import Race, Sport, Event
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from json import dumps
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render_to_response, render
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.forms import EventForm

import datetime

import logging


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


# Ajax calls
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


# @login_required
# def ajx_validate_all(request):
#     if (request.is_ajax() or settings.DEBUG) and request.method == 'GET':
#         for r in Race.validated_objects.all():
#             r.validated = True
#             r.save()
#         return HttpResponse('')
#     return HttpResponseBadRequest


# @login_required
# def ajx_validate_race(request, pk):
#     if (request.is_ajax() or settings.DEBUG) and request.method == 'PUT':
#         race = get_object_or_404(Race, pk=pk)
#         logging.debug('validate ' + str(race))  
#         race.validated = True
#         race.save()
#         return HttpResponse('')
#     return HttpResponseBadRequest


@login_required
def ajx_delete_race(request, pk):
    logging.debug(str(request.is_ajax()) + '-' + str(settings.DEBUG) + '-' + str(request.method))
    if (request.is_ajax() or settings.DEBUG) and request.method == 'DELETE':
        race = get_object_or_404(Race, pk=pk)
        race.delete()
        return HttpResponse('')
    return HttpResponseBadRequest


def ajx_get_races(request):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'GET':

        sqs = SearchQuerySet()
        # sqs = sqs.filter(validated="true")

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
            result_html = render_to_string('core/search_no_result_alert.html', { 'search_expr' : search_expr})

        response = {'count': sqs.count(),
                    'races': races,
                    'html': result_html,
                    'facet': facet,
                    }

        return HttpResponse(dumps(response), content_type="application/json")

    raise Http404


class FacetTest(LoginRequiredMixin, ListView):
    model = Race
    context_object_name = "race_listp"
    template_name = "core/test_facet.html"


# Should be heriting View ... or function not based on a class
class RaceList(LoginRequiredMixin, TemplateView):
    # model = Race
    context_object_name = "race_list"
    template_name = "core/racesearch.html"

    def get_context_data(self, **kwargs):
        context = super(RaceList, self).get_context_data(**kwargs)

        # GET parameters and convert directly to dict for better handling in the templates
        context['params'] = self.request.GET.dict()

        # TODO : get from season model
        if not self.request.GET.get('start_date'):
            context['params']['start_date'] = "2015-01-01"
        if not self.request.GET.get('end_date'):
            context['params']['end_date'] = "2015-12-31"

        # Loop through distances parameters as it is a list of values
        context['params']['distances'] = {}
        for dist in self.request.GET.getlist('distances'):
            # directly assign into params.distances.XS for example
            context['params']['distances'][dist] = True


        return context


def update_event(request, pk):
    event = Event.objects.get(pk=pk)
    eventForm = EventForm(request.POST or None, instance=event)

    # eventRef = eventEdition.event_ref
    # eventRefForm = EventReferenceForm(request.POST or None, instance=eventRef)

    race_list = event.get_races()
    

    if request.method == 'POST':
        if eventForm.is_valid():
            event = event.clone()
            eventForm = EventForm(request.POST or None, instance=event)
            eventForm.save()
            messages.success(request, (
                "L'évènement {0} a bien été modifié et sera publié "
                "après validation par nos services".format(event.name))
            )

            return HttpResponseRedirect(reverse('list_race'))


    return render(request, 'core/update_event.html', {'eventForm': eventForm,
                                                      'pk': pk, 
                                                      'race_list': race_list})
    

# def update_race(request, slug, pk):
#     race = Race.objects.get(pk=pk)
#     raceForm = RaceForm(request.POST or None, instance=race)
#     location = race.location
#     locationForm = LocationForm(request.POST or None, instance=location)
#     contact = race.contact
#     contactForm = ContactForm(request.POST or None, instance=contact)


#     if request.method == 'POST':
#         if raceForm.is_valid():
#             raceForm.save()
#         return HttpResponseRedirect(reverse('update_event'))
#     return render(request, 'core/update_race.html', {'raceForm': raceForm, 
#                                                      'locationForm': locationForm,
#                                                      'contactForm': contactForm })


class RaceView(LoginRequiredMixin, DetailView):
    model = Race
    context_object_name = "race"
    template_name = "core/race.html"


class RaceEdit(SessionWizardView):

    TEMPLATES = {"race": "core/create_race.html",
                 "location": "core/create_race.html",
                 "contact": "core/create_race.html"}

    # template_name = 'core/create_race.html'

    # Define template files trough TEMPLATES dict
    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def get_form_initial(self, step):
        if 'pk' in self.kwargs:
            return {}
        else:
            return self.initial_dict.get(step, {})

    def get_form_instance(self, step):
        event_pk = self.kwargs['event']
        self.event = Event.objects.get(pk=event_pk)
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            race = Race.objects.get(pk=pk)

            if (step == "race"):
                instance = race
            elif (step == "location"):
                instance = race.location
            elif (step == "contact"):
                instance = race.contact

            logging.debug("instance {0}".format(instance))
            return instance

        else:
            return self.instance_dict.get(step, None)

    # This method is called when every forms has been submitted and validated
    def done(self, form_list, form_dict, **kwargs):
        location = form_dict['location'].save()
        logging.debug("location {0}".format(location))
        contact = form_dict['contact'].save()
        logging.debug("contact {0}".format(contact))
        race = form_dict['race'].save(commit=False)
        race.location = location
        race.contact = contact

        if not hasattr(race, 'event'):
            race.event = self.event

        race.save()

        if race.pk:
            messages.success(self.request, (
                "La course {0} a bien été créée et sera publiée "
                "après validation par nos services".format(race.event.name))
            )

            changed_fields = []
            for form in form_list:
                if form.has_changed():
                    changed_fields.append(form.changed_data)

            return HttpResponseRedirect(reverse('update_event', kwargs={'pk': race.event.pk}))

        messages.error(self.request, ("Il y a eu un problème lors de la création de la course"))
        return HttpResponseRedirect(reverse('create_race'))


class IntroView(LoginRequiredMixin, TemplateView):
    template_name = 'core/introduction.html'


class RaceDelete(DeleteView):
    model = Race
    template_name = 'core/confirm_delete.html'
    # success_url = reverse_lazy('list_race')
    context_object_name = "race"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        self.instance = get_object_or_404(Race, pk=pk)
        return self.instance

    def get_success_url(self):
        return reverse('update_event', kwargs={'pk': self.instance.event.pk})


class RaceValidationList(ListView):
    model = Race
    # queryset = Race.objects.filter(validated=False)
    queryset = Race.objects.all()
    template_name = 'core/tovalidate.html'
    context_object_name = "race_list"


