from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.formtools.wizard.views import SessionWizardView
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import DeleteView
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse

from core.forms import EventForm
from core.models import Race, Event

from planning.models import ShortlistedRace

import logging


# Should probably not mix CBV and classic views.. TODO: some cleaning, you know


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, *initargs, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(*initargs, **initkwargs)
        return login_required(view)


# List and view
class IntroView(TemplateView):
    template_name = 'core/introduction.html'


class EventValidationList(LoginRequiredMixin, ListView):
    model = Event
    queryset = Event.objects.filter(event_mod_source=None)
    template_name = "core/list_event_validation.html"
    context_object_name = "event_list"


class RaceList(TemplateView):
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
            # directly assign into params.distances.XS for examplew
            context['params']['distances'][dist] = True


class EventView(DetailView):
    model = Event
    context_object_name = "event"
    template_name = "core/view_event.html"


class RaceView(DetailView):
    model = Race
    context_object_name = "race"
    template_name = "core/race.html"

    def get_context_data(self, **kwargs):
        planned_race = ''
        if self.request.user.is_authenticated():
            user = self.request.user
            planned_race = [sr.race for sr in ShortlistedRace.objects.filter(user=user)]
        context = super(RaceView, self).get_context_data(**kwargs)
        context.update({'planned_race': planned_race})
        return context


# CRUD
@login_required
def create_event(request):
    eventForm = EventForm(request.POST or None)

    if request.method == 'POST':
        if eventForm.is_valid():
            event = eventForm.save()
            messages.success(request, (
                "L'évènement {0} a bien été modifié et sera publié "
                "après validation par nos services".format(event.name))
            )

            return HttpResponseRedirect(reverse('update_event', kwargs={'pk': event.pk}))

    return render(request, 'core/edit_event.html', {'eventForm': eventForm,
                                                    'pk': None,
                                                    'race_list': None})


@login_required
def update_event(request, pk):
    event = Event.objects.get(pk=pk)

    eventForm = EventForm(request.POST or None, instance=event)
    race_list = event.get_races()

    # if form sent
    if request.method == 'POST':

        if eventForm.is_valid():
            eventForm.save()
            messages.success(request, (
                "L'évènement {0} a bien été modifié et sera publié "
                "après validation par nos services".format(event.name)
                )
            )

            return HttpResponseRedirect(reverse('list_race'))
    # if form init
    else:
        if event.validated:
            cloned_event = event.clone()
            return HttpResponseRedirect(reverse('update_event', kwargs={'pk': cloned_event.pk}))

    return render(request, 'core/edit_event.html', {'eventForm': eventForm,
                                                    'pk': pk,
                                                    'race_list': race_list,
                                                    })


class EventDelete(LoginRequiredMixin, DeleteView):
    mode = Event
    template_name = 'core/delete_event.html'
    context_object_name = "event"

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
        self.object.to_be_deleted = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class RaceEdit(LoginRequiredMixin, SessionWizardView):

    TEMPLATES = {"race": "core/edit_race.html",
                 "location": "core/edit_race.html",
                 "contact": "core/edit_race.html"}

    update_flg = False
    # template_name = 'core/edit_race.html'

    def get(self, request, *args, **kwargs):
        """
        This method handles GET requests.

        If a GET request reaches this point, the wizard assumes that the user
        just starts at the first step or wants to restart the process.
        The data of the wizard will be resetted before rendering the first step.
        """

        # if update
        if 'pk' in self.kwargs:
            self.update_flg = True

        event_pk = self.kwargs['event']
        event = Event.objects.get(pk=event_pk)

        if event.validated:
            cloned_event = event.clone()
            if self.update_flg:
                # TODO : ne pas transmettre l'ancien race pk ! mais quoi ?
                return HttpResponseRedirect(reverse('update_event', kwargs={'pk': cloned_event.pk}))
            return HttpResponseRedirect(reverse('add_race', kwargs={'event': cloned_event.pk}))

        self.storage.reset()

        # reset the current step to the first step.
        self.storage.current_step = self.steps.first
        return self.render(self.get_form())

    def get_context_data(self, form, **kwargs):
        event_pk = self.kwargs['event']
        context = super(RaceEdit, self).get_context_data(form=form, **kwargs)
        context.update({'event_pk': event_pk, 'update_flg': self.update_flg})
        return context

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
            changed_fields = []
            for form in form_list:
                if form.has_changed():
                    changed_fields.append(form.changed_data)

            return HttpResponseRedirect(reverse('update_event', kwargs={'pk': race.event.pk}))

        messages.error(self.request, ("Il y a eu un problème lors de la création de la course"))
        return HttpResponseRedirect(reverse('create_race'))


class RaceDelete(LoginRequiredMixin, DeleteView):
    model = Race
    template_name = 'core/delete_race.html'
    # success_url = reverse_lazy('list_race')
    context_object_name = "race"

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk', None)
        self.instance = get_object_or_404(Race, pk=pk)
        return self.instance

    def get_success_url(self):
        return reverse('update_event', kwargs={'pk': self.instance.event.pk})
