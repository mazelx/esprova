from django.shortcuts import get_list_or_404
from django.views.generic import ListView, DetailView
from core.models import Race
from django.http import HttpResponse
from django.conf import settings
from django.core import serializers
from django.template import Context
from core.utils import render_block_to_string
from json import dumps


class RaceList(ListView):
    model = Race
    context_object_name = "race_list"
    template_name = "core/race_list.html'"

    def getRacesFromMapBounds(request):
        if request.is_ajax() or settings.DEBUG:
            _lat_lo = request.GET.get('lat_lo')
            _lng_lo = request.GET.get('lng_lo')
            _lat_hi = request.GET.get('lat_hi')
            _lng_hi = request.GET.get('lng_hi')
            raceSet = Race.objects.filter(location__lat__gte=_lat_lo,
                                          location__lng__gte=_lng_lo,
                                          location__lat__lte=_lat_hi,
                                          location__lng__lte=_lng_hi)
            context = Context({"race_list": raceSet})
            return_str = render_block_to_string('core/race_list.html', 'racelist', context)
            # return HttpResponse(serializers.serialize('json', raceSet))
            return HttpResponse(return_str)
            # return HttpResponse(context["race_list"])
        return HttpResponse('404')


class RaceView(DetailView):
    context_object_name = "race"
    model = Race
    template_name = "core/race.html"



    # def get_object(self):
    #     # Nous récupérons l'objet, via la super-classe
    #     article = super(LireArticle, self).get_object()
    
    #     # article.nb_vues += 1  # Imaginons un attribut « Nombre de vues »
    #     article.save()
    
    #     return article  # Et nous retournons l'objet à afficher
