from django.http import Http404
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from core.models import Race, Sport
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
from django.shortcuts import get_object_or_404, render
# from core.forms import SportForm

import datetime

import logging


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


# Ajax calls
@login_required
def ajx_set_sport_session(request):
    # if this is a POST request we need to process the form data
    if (request.is_ajax() or settings.DEBUG) and request.method == 'POST':
        # create a form instance and populate it with data from the request:
        sport = request.POST.get("sport").lower()
        if sport in [s.name.lower() for s in Sport.objects.all()]:
            request.session['selected_sport'] = sport
            return HttpResponse('')
    return Http404


@login_required
def ajx_validate_all(request):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'GET':
        for r in Race.validated_objects.all():
            r.validated = True
            r.save()
        return HttpResponse('')
    return Http404


@login_required
def ajx_validate_race(request, pk):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'PUT':
        race = get_object_or_404(Race, pk=pk)
        logging.debug('validate ' + str(race))
        race.validated = True
        race.save()
        return HttpResponse('')
    return Http404


@login_required
def ajx_delete_race(request, pk):
    logging.debug(str(request.is_ajax()) + '-' + str(settings.DEBUG) + '-' + str(request.method))
    if (request.is_ajax() or settings.DEBUG) and request.method == 'DELETE':
        race = get_object_or_404(Race, pk=pk)
        race.delete()
        return HttpResponse('')
    return HttpResponseBadRequest


@login_required
def ajx_get_races(request):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'GET':

        sqs = SearchQuerySet()
        sqs = sqs.filter(validated="true")

        # search from quick search form
        sport = request.GET.get('sport')
        if not sport:
            raise Http404
        sqs = sqs.filter(sport=sport)

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

        if not start_date:
            start_date = "2015-01-07"
        sqs = sqs.filter(date__gte=start_date)

        if not end_date:
            end_date = "2016-01-06"
        sqs = sqs.filter(date__lte=end_date)

        if distances:
            sqs = sqs.filter(distance_cat__in=distances)

        # search from quick search form
        search_expr = request.GET.get('search_expr')

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
            result_html = render_to_string('core/search_no_result_alert.html')

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


class RaceView(LoginRequiredMixin, DetailView):
    model = Race
    context_object_name = "race"
    template_name = "core/race.html"


class RaceWizard(SessionWizardView):

    TEMPLATES = {"eventReference": "core/create_race.html",
                 "eventEdition": "core/create_race.html",
                 "race": "core/create_race.html",
                 "location": "core/create_race_location.html",
                 "contact": "core/create_race.html"}

    # template_name = 'core/create_race.html'

    # Define template files trough TEMPLATES dict
    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def get_form_initial(self, step):
        if 'slug' in self.kwargs:
            return {}
        else:
            return self.initial_dict.get(step, {})

    def get_form_instance(self, step):
        if 'slug' in self.kwargs:
            slug = self.kwargs['slug']
            race = Race.objects.get(slug=slug)

            if (step == "eventReference"):
                instance = race.event.event_ref
            elif (step == "eventEdition"):
                instance = race.event
            elif (step == "race"):
                instance = race
            elif (step == "location"):
                instance = race.location
            elif (step == "contact"):
                instance = race.contact

            logging.debug("instance {0}".format(instance))
            return instance

        else:
            return self.instance_dict.get(step, None)

    def done(self, form_list, form_dict, **kwargs):
        eventReference = form_dict['eventReference'].save()
        logging.debug("event reference {0} saved , pk:{1}".format(eventReference, eventReference.pk))
        eventEdition = form_dict['eventEdition'].save(commit=False)
        eventEdition.event_ref = eventReference
        eventEdition.save()
        logging.debug("event {0}".format(eventReference))
        location = form_dict['location'].save()
        logging.debug("event {0}".format(location))
        contact = form_dict['contact'].save()
        logging.debug("event {0}".format(contact))
        race = form_dict['race'].save(commit=False)
        race.location = location
        race.event = eventEdition
        race.contact = contact
        logging.debug("race {0}".format(race))
        race.save()

        if race.pk:
            messages.success(self.request, (
                "La course {0} a bien été créée et sera publiée "
                "après validation par nos services".format(race.event.name))
            )
            return HttpResponseRedirect(reverse('list_race'))

        messages.error(self.request, ("Il y a eu un problème lors de la création de la course"))
        return HttpResponseRedirect(reverse('create_race'))


class IntroView(TemplateView):
    template_name = 'core/introduction.html'


class RaceDelete(DeleteView):
    model = Race
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('validate_racelist')
    context_object_name = "race"

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug', None)
        return get_object_or_404(Race, slug=slug)


class RaceValidationList(ListView):
    model = Race
    queryset = Race.objects.filter(validated=False)
    template_name = 'core/tovalidate.html'
    context_object_name = "race_list"


