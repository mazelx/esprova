from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import RaceView, RaceList, getRacesAjax, RaceCreate, RaceWizard
from core.forms import ContactForm, RaceForm, LocationForm, EventForm

race_named_forms = (
    ("event", EventForm),
    ("race", RaceForm),
    ("location", LocationForm),
    ("contact", ContactForm)
)


race_wizard = RaceWizard.as_view(race_named_forms, url_name="race_wizard_step")


urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', RaceList.as_view(), name='list_race'),
                       url(r'^race/(?P<pk>\d+)$', RaceView.as_view(), name='view_race'),
                       url(r'^search/$', getRacesAjax, name='search_race'),
                       url(r'^create/', RaceCreate.as_view(), name='create_race'),
                       # url(r'^wizard/$', race_wizard),
                       url(r'^wizard/(?P<step>[-\w]+)/$', race_wizard, name="race_wizard_step"),
                       url(r'^wizard/$', race_wizard, name="race_wizard"),
                       )
