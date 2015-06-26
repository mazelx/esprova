from django.conf.urls import patterns, url
from django.contrib.sitemaps import FlatPageSitemap, GenericSitemap
from django.contrib.sitemaps.views import sitemap

from events.models import Race
from planning.models import ShortlistedRace
from core.views import PlanningSiteMap, StaticViewSitemap

race_dict = {
    'queryset': Race.objects.filter(event__validated=True),
    'date_field': 'modified_date',
}


sitemaps = {
    'static': StaticViewSitemap(),
    'races': GenericSitemap(race_dict, priority=0.8),
    'planning': PlanningSiteMap(),
}

urlpatterns = patterns('', url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps},
                               name='django.contrib.sitemaps.views.sitemap'),)
