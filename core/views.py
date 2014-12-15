from django.shortcuts import render
from django.views.generic import ListView, DetailView
from core.models import Race


class RaceList(ListView):
    model = Race
    context_object_name = "derniers_articles"
    template_name = "blog/accueil.html"

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
