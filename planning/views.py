from planning.models import ShortlistedRace
from django.views.generic import ListView


class PlanningList(ListView):
    model = ShortlistedRace
    template_name = 'planning/planning_list.html'
    context_object_name = "planned_race_list"

    def get_queryset(self):
        return ShortlistedRace.objects.filter(user=self.request.user)
