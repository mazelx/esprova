from django.http import Http404
from django.views.generic import ListView, DetailView, TemplateView, DeleteView
from core.models import Race
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse, reverse_lazy
from django.conf import settings
from json import dumps
from haystack.query import SearchQuerySet
from haystack.utils.geo import Point
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib import messages
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

import logging


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(**initkwargs)
        return login_required(view)


@login_required
def validateRace(request, pk):
    race = get_object_or_404(Race, pk=pk)
    race.validated = True
    race.save()
    return HttpResponseRedirect(reverse('validate_racelist'))



@login_required
def getRacesAjax(request):
    if (request.is_ajax() or settings.DEBUG) and request.method == 'GET':

        sqs = SearchQuerySet()
        sqs = sqs.filter(validated="true")

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

        sqs.order_by('score')
        # build the JSON response
        races = []
        result_html = []

        # Uniqfy the event list (multiple races from an event)
        seen = {}
        rank = 1
        for sr in sqs:
            event_id = sr.get_stored_fields()['event_id']
            location = sr.get_stored_fields()['location']
            rendered = sr.get_stored_fields()['rendered']

            if event_id in seen:
                continue

            seen[event_id] = 1
            race_data = {'id': int(event_id),
                         'score': str(sr.score),
                         'rankClass': "primary" if (rank <= 10) else "secondary",
                         'lat': str(location.get_coords()[1]),
                         'lng': str(location.get_coords()[0])
                         }

            races.append(race_data)
            result_html.append(rendered)

            rank += 1

        if not races:
            result_html = render_to_string('core/search_no_result_alert.html')

        response = {'count': sqs.count(),
                    'races': races,
                    'html': result_html
                    }

        return HttpResponse(dumps(response), content_type="application/json")

    raise Http404


# Should be heriting View ... or function not based on a class
class RaceList(LoginRequiredMixin, ListView):
    model = Race
    context_object_name = "race_list"
    template_name = "core/race_list.html'"


class RaceView(LoginRequiredMixin, DetailView):
    model = Race
    context_object_name = "race"
    template_name = "core/race.html"


class RaceWizard(SessionWizardView):

    TEMPLATES = {"event": "core/create_race.html",
                 "race": "core/create_race.html",
                 "location": "core/create_race_location.html",
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
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            race = Race.objects.get(pk=pk)

            if (step == "event"):
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
        event = form_dict['event'].save()
        logging.debug("event {0}".format(event))
        location = form_dict['location'].save()
        logging.debug("event {0}".format(location))
        contact = form_dict['contact'].save()
        logging.debug("event {0}".format(contact))
        race = form_dict['race'].save(commit=False)
        race.location = location
        race.event = event
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



class IntroView(LoginRequiredMixin, TemplateView):
    template_name = 'core/introduction.html'


class RaceDelete(DeleteView):
    model = Race
    template_name = 'core/confirm_delete.html'
    success_url = reverse_lazy('list_race')
    context_object_name = "race"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        return get_object_or_404(Race, pk=pk)


class RaceValidationList(ListView):

    model = Race
    queryset = Race.objects.filter(validated=False)
    template_name = 'core/tovalidate.html'
    context_object_name = "race_list"

