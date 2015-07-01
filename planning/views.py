from planning.models import ShortlistedRace, UserPlanning
from events.models import Race
from core.views import LoginRequiredMixin
from django.views.generic import ListView
from django.contrib import messages
from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404
from django.core.exceptions import PermissionDenied


class PlanningList(ListView):
    model = ShortlistedRace
    template_name = 'planning/planning_list.html'
    context_object_name = "planned_race_list"
    secret_key = ''
    username = ''

    def get_queryset(self):
        self.username = self.kwargs.get('username', None)
        secret_key = self.request.GET.get('secret_key')
        user = User.objects.filter(username=self.username).first() or self.request.user
        up = get_object_or_404(UserPlanning, user=user)


        if not (user == self.request.user or secret_key == up.secret_key):
            raise PermissionDenied()

        self.secret_key = up.secret_key

        return up.races.order_by("race__date")

    def get_context_data(self, **kwargs):
        context = super(PlanningList, self).get_context_data(**kwargs)
        context['username'] = self.username
        context['secret_key'] = self.secret_key
        return context


def redirect_to_planning(request):
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('planning', kwargs={'username': request.user.username}))
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
                up = UserPlanning.objects.get(user=user)
                planned = ShortlistedRace(user_planning=up, race=race)
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
                up = UserPlanning.objects.get(user=user)
                planned = ShortlistedRace.objects.get(user_planning=up, race=race)
                planned.delete()
            except race.DoesNotExist:
                pass
            messages.success(request, 'La course a bien été retirée du programme')
            return HttpResponse('')

    messages.error(request, "Il y a eu un problème lors de la retrait de la course du programme")
    return HttpResponseBadRequest

