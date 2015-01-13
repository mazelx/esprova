from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import RaceView, RaceList, getRacesAjax, RaceWizard
from core.forms import ContactForm, RaceForm, LocationForm, EventForm

race_named_forms = (
    ("event", EventForm),
    ("race", RaceForm),
    ("location", LocationForm),
    ("contact", ContactForm)
)

create_race = RaceWizard.as_view(race_named_forms, url_name="create_race_step")


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', RaceList.as_view(), name='list_race'),
                       url(r'^race/(?P<pk>\d+)$', RaceView.as_view(), name='view_race'),
                       url(r'^search/$', getRacesAjax, name='search_race'),
                       url(r'^create/$', create_race, name="create_race"),
                       url(r'^create/(?P<step>[-\w]+)/$', create_race, name="create_race_step"),
                       )
