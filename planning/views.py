from planning.models import ShortlistedRace
from events.models import Race
from core.views import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.generic.base import RedirectView
from django.core.urlresolvers import reverse


class PlanningList(LoginRequiredMixin, ListView):
    model = ShortlistedRace
    template_name = 'planning/planning_list.html'
    context_object_name = "planned_race_list"

    def get_queryset(self):
        username = self.kwargs.get('user', None)
        user = User.objects.filter(username=username) or self.request.user
        return ShortlistedRace.objects.filter(user=user).order_by("race__date")


def redirect_to_planning(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('planning', kwargs={'user': request.user}))
    return HttpResponseRedirect(reverse('auth_login') + '?next=' + reverse('planning'))


@login_required
def add_race_to_planning(request):
    # Ajax calls
    # if this is a POST request we need to process the form data
    if ((request.is_ajax() or settings.DEBUG) and request.user.is_authenticated()):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            race_pk = request.POST.get("race")
            try:
                race = Race.objects.get(pk=race_pk)
                user = request.user
                planned = ShortlistedRace(user=user, race=race)
                planned.save()
            except race.DoesNotExist:
                pass
            messages.success(request, 'La course a bien été ajoutée du programme')
            return HttpResponse('')
    
    messages.error(request, "Il y a eu un problème lors de l'ajout de la course au programme")
    return HttpResponseBadRequest


def remove_race_from_planning(request):
    # Ajax calls
    # if this is a POST request we need to process the form data
    if ((request.is_ajax() or settings.DEBUG) and request.user.is_authenticated()):
        if request.method == 'POST':
            # create a form instance and populate it with data from the request:
            race_pk = request.POST.get("race")
            try:
                race = Race.objects.get(pk=race_pk)
                user = request.user
                planned = ShortlistedRace.objects.get(user=user, race=race)
                planned.delete()
            except race.DoesNotExist:
                pass
            messages.success(request, 'La course a bien été supprimée du programme')
            return HttpResponse('')

    messages.error(request, "Il y a eu un problème lors de la retrait de la course du programme")
    return HttpResponseBadRequest

