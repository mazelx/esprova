from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import RaceView, RaceList, getRacesAjax, RaceWizard
from core.forms import ContactForm, RaceForm, LocationForm, EventForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView


race_named_forms = (
    ("event", EventForm),
    ("race", RaceForm),
    ("location", LocationForm),
    ("contact", ContactForm)
)

create_race = RaceWizard.as_view(race_named_forms, url_name="create_race_step")


urlpatterns = patterns('',
                       url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'},
                           name="login"),
                       url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name="logout"),
                       url(r'^robots\.txt$', TemplateView.as_view(
                           template_name='robots.txt',
                           content_type='text/plain')),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^$', RaceList.as_view(), name='list_race'),
                       url(r'^race/(?P<pk>\d+)$', RaceView.as_view(), name='view_race'),
                       url(r'^search/$', getRacesAjax, name='search_race'),
                       url(r'^create/$', create_race, name="create_race"),
                       url(r'^create/(?P<step>[-\w]+)/$', create_race, name="create_race_step"),
                       )

# serve static files on dev
urlpatterns += staticfiles_urlpatterns()
