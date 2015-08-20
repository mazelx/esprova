from django.conf.urls import patterns, url
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap

from events.models import Race, Sport
from core.views import StaticViewSitemap

race_dict = {
    'queryset': Race.objects.filter(event__validated=True),
    'date_field': 'modified_date',
}

search_dict = {
    'queryset': Sport.objects.all(),
}

sitemaps = {
    'static': StaticViewSitemap(),
    'races': GenericSitemap(race_dict, priority=0.8),
    'search': GenericSitemap(search_dict, priority=1.0),
}

urlpatterns = patterns('', url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
                               name='django.contrib.sitemaps.views.sitemap'),)
