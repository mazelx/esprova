from django.contrib.auth.decorators import login_required
from django.views.generic import TemplateView
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse


from django.contrib.auth.models import User
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


def handler500(request):
    response = render_to_response('500.html', {'random_race': Race.objects.random()},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


class PlanningSiteMap(Sitemap):
    changefreq = "weekly"
    priority = 0.5

    def items(self):
        return User.objects.all()

    def location(self, obj):
        return reverse('planning', args=[obj.username])


class StaticViewSitemap(Sitemap):
    changefreq = 'daily'
    prioritized_items = {'legal': 0.1, 'list_race': 0.9, 'intro': 1.0}

    def items(self):
        return [item for item, priority in self.prioritized_items.items()]

    def location(self, item):
        return reverse(item)

    def priority(self, item):
        return self.prioritized_items[item]

