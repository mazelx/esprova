from django.shortcuts import get_object_or_404
from django.views.generic import ListView, DetailView
from core.models import Race
from django.http import HttpResponse
# from django.template import RequestContext


class RaceList(ListView):
    model = Race
    context_object_name = "derniers_articles"
    template_name = "blog/accueil.html"

    def getRacesFromLatLng(request):
        if request.is_ajax():
            race_id = request.GET.get('race', '')
            race = get_object_or_404(Race, pk=race_id)
            if race_id is None or race_id == "":
                race_id = 'Aucune course transmise'
            return HttpResponse("Race : " + race.event.name)
        return HttpResponse('')
        

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
