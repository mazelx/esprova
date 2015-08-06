from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404, redirect
from django.core.urlresolvers import reverse

from django.conf import settings

from json import dumps

from core.views import LoginRequiredMixin

from events.forms import EventForm, OrganizerForm
from events.models import Race, Event, Sport

from api.views import races_formatted_search

from planning.models import ShortlistedRace, UserPlanning

import logging


class EventValidationList(LoginRequiredMixin, ListView):
    model = Event
    queryset = Event.objects.filter(event_mod_source=None)
    template_name = "events/event_validation_list.html"
    context_object_name = "event_list"

    def get_queryset(self):
        changed_event_list = []
        qs = super(EventValidationList, self).get_queryset()
        for event in qs:
            nb_changes = event.get_nb_changes()
            # add event to the list :
            # * if event has one or more awaiting validation change OR
            # * if event has just been created (no source_mod and not validated)
            if nb_changes or not event.validated:
                changed_event_list.append((event, nb_changes))
        return changed_event_list


class RaceSearch(TemplateView):
    context_object_name = "race_list"
    template_name = "events/race_search.html"

    def dispatch(self, *args, **kwargs):
        if 'sport' not in self.kwargs:
            default_sport_name = settings.DEFAULT_SPORT
            if 'selected_sport' in self.request.session:
                default_sport_name = self.request.session['selected_sport']

            return HttpResponseRedirect(reverse('list_race_sport', kwargs={'sport': default_sport_name}))
        return super(RaceSearch, self).dispatch(*args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(RaceSearch, self).get_context_data(**kwargs)

        # GET parameters and convert directly to dict for better handling in the templates
        context['params'] = self.request.GET.dict()

        # min date for retreiving data (has an impact on degrated browsing INCLUDING search bots)
        # if not self.request.GET.get('start_date'):
            # context['params']['start_date'] = "2014-01-01"
        # if not self.request.GET.get('end_date'):
            # context['params']['end_date'] = "2016-12-31"

        if 'distances' in self.request.GET:
            context['params']['distances'] = self.request.GET.get('distances').split(',')

        # sport_name = self.request.session['selected_sport'] or Sport.objects.first().name

        sport_name = self.kwargs.get('sport', None)
        sport = get_object_or_404(Sport, name__iexact=sport_name)

        viewport = ''
        if 'viewport' in self.request.GET:
            viewport = self.request.GET.get('viewport').split(',')

        # get prefilled racelist html
        data = races_formatted_search(format='dict',
                                      sport=sport,
                                      viewport=viewport,
                                      start_date=self.request.GET.get('start_date'),
                                      end_date=self.request.GET.get('end_date'),
                                      distances=self.request.GET.getlist('distances'),
                                      search_expr=self.request.GET.get('q'))
        context.update({'racelist': ''.join(data['html'])})
        context.update({'json_races': dumps(data['races'])})
        context['params']['sport'] = sport_name
        context['sport'] = sport

        return context


class EventView(LoginRequiredMixin, DetailView):
    model = Event
    context_object_name = "event"
    template_name = "events/event_view.html"


class RaceView(DetailView):
    model = Race
    context_object_name = "race"
    template_name = "events/race_view.html"

    def get_context_data(self, **kwargs):
        planned_race = ''
        if self.request.user.is_authenticated():
            user = self.request.user
            up = UserPlanning.objects.get(user=user)
            planned_race = [sr.race for sr in ShortlistedRace.objects.filter(user_planning=up)]

        context = super(RaceView, self).get_context_data(**kwargs)
        context.update({'planned_race': planned_race})

        return context


# CRUD
@login_required
def create_event(request, pk=None):
    if pk:
        e = Event.objects.get(pk=pk)
        eventSrc = e.clone()
        eventSrc.edition += 1
        eventSrc.save()
        return HttpResponseRedirect(reverse('update_event', kwargs={'pk': eventSrc.pk}))

    event_name = request.GET.get('name')

    eventForm = EventForm(request.POST or None, initial={'name': event_name})

    if request.method == 'POST':
        eventForm = EventForm(request.POST)
        if eventForm.is_valid():
            event = eventForm.save()
            return HttpResponseRedirect(reverse('update_event', kwargs={'pk': event.pk}))

    return render(request, 'events/event_edit.html', {'eventForm': eventForm,
                                                      'pk': None,
                                                      'race_list': None})


@login_required
def create_organizer(request):
    organizerForm = OrganizerForm(request.POST or None)

    if request.method == 'POST':
        if organizerForm.is_valid():
            event = organizerForm.save()
            return HttpResponseRedirect(reverse('update_event', kwargs={'pk': event.pk}))

    return render(request, 'events/event_edit.html', {'eventForm': organizerForm,
                                                      'pk': None,
                                                      'race_list': None})


@login_required
def update_event(request, pk):
    event = Event.objects.get(pk=pk)

    eventForm = EventForm(request.POST or None, instance=event)
    race_list = event.get_races()
    created = request.GET.get('created')

    # if form sent
    if request.method == 'POST':

        if eventForm.is_valid():
            eventForm.save()

            if not event.event_mod_source:
                # creation
                messages.success(request, (
                    "L'événement {0} a bien été créé et sera publié "
                    "après validation par nos services".format(event.name)
                    ))
            else:
                # update
                messages.success(request, (
                    "L'événement {0} a bien été modifié et sera publié "
                    "après validation par nos services".format(event.event_mod_source.name)
                    ))

            return HttpResponseRedirect(reverse('list_race'))
    # if form init
    else:
        if event.validated:
            cloned_event = event.clone()
            print("event cloned")
            return HttpResponseRedirect(reverse('update_event', kwargs={'pk': cloned_event.pk}) + '?created=True')

    return render(request, 'events/event_edit.html', {'eventForm': eventForm,
                                                      'pk': pk,
                                                      'race_list': race_list,
                                                      'created': created or False,
                                                      })


class EventDelete(LoginRequiredMixin, DeleteView):
    model = Event
    template_name = 'events/event_delete.html'
    context_object_name = "event"
    hard_delete = True

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        self.instance = get_object_or_404(Event, pk=pk)
        return self.instance

    def get_success_url(self):
        return reverse('list_race')

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        if not self.hard_delete:
            # Soft delete
            self.object.to_be_deleted = True
            self.object.save()
            messages.success(request, (
                        "La demande de suppression de l'événement {0} a bien été prise en compte "
                        " et sera traitée par notre équipe de validation".format(self.instance.name)
                        ))
        else:
            # hard delete
            self.object.delete()

        return HttpResponseRedirect(success_url)


class EventSoftDelete(EventDelete):
    hard_delete = False


class RaceEdit(LoginRequiredMixin, SessionWizardView):

    TEMPLATES = {"race": "events/race_edit.html",
                 "location": "events/race_edit.html",
                 "contact": "events/race_edit.html"}

    update_flg = False
    event = None
    # template_name = 'events/race_edit.html'

    def get_form_kwargs(self, step):
        # if update
        if 'pk' in self.kwargs:
            self.update_flg = True
        return super(RaceEdit, self).get_form_kwargs(step)

    def get_context_data(self, form, **kwargs):
        event_pk = self.kwargs['event']
        context = super(RaceEdit, self).get_context_data(form=form, **kwargs)
        context.update({'event_pk': event_pk, 'update_flg': self.update_flg})
        return context

    # Define template files trough TEMPLATES dict
    def get_template_names(self):
        return [self.TEMPLATES[self.steps.current]]

    def get_form_initial(self, step):
        # initial = self.initial_dict.get(step, {})
        if 'event' in self.kwargs:
            event_pk = self.kwargs['event']
            self.event = Event.objects.get(pk=event_pk)

        if 'pk' in self.kwargs:
            return {}
        else:
            data = {}
            if self.event.races.count():
                if step == 'location':
                    data = self.event.races.last().location.__dict__.copy()
                elif step == 'contact':
                    data = self.event.races.last().contact.__dict__.copy()
            return self.initial_dict.get(step, data)

    def get_form_instance(self, step):
        if 'pk' in self.kwargs:
            pk = self.kwargs['pk']
            race = Race.objects.get(pk=pk)

            if (step == "race"):
                instance = race
            elif (step == "location"):
                instance = race.location
            elif (step == "contact"):
                instance = race.contact

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
        if self.request.user.is_authenticated():
            if self.update_flg:
                race.modified_by = self.request.user.username
            else:
                race.created_by = self.request.user.username

        if not hasattr(race, 'event'):
            race.event = self.event

        race.save()

        if race.pk:
            changed_fields = []
            for form in form_list:
                if form.has_changed():
                    changed_fields.append(form.changed_data)

            return HttpResponseRedirect(reverse('update_event', kwargs={'pk': race.event.pk}))

        messages.error(self.request, ("Il y a eu un problème lors de la création de la course"))
        return HttpResponseRedirect(reverse('create_race'))


class RaceDelete(LoginRequiredMixin, DeleteView):
    model = Race
    template_name = 'events/race_delete.html'
    # success_url = reverse_lazy('list_race')
    context_object_name = "race"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        self.instance = get_object_or_404(Race, pk=pk)
        return self.instance

    def get_success_url(self):
        return reverse('update_event', kwargs={'pk': self.instance.event.pk})

    def delete(self, request, *args, **kwargs):
        """
        Calls the delete() method on the fetched object and then
        redirects to the success URL.
        """
        self.object = self.get_object()
        success_url = self.get_success_url()
        self.object.to_be_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)
