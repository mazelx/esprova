from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from events.models import Race


class LoginRequiredMixin(object):
    @classmethod
    def as_view(cls, *initargs, **initkwargs):
        view = super(LoginRequiredMixin, cls).as_view(*initargs, **initkwargs)
        return login_required(view)


# List and view
class IntroView(TemplateView):
    template_name = 'core/introduction.html'


def handler404(request):
    response = render_to_response('404.html', {'random_race': Race.objects.random()},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

