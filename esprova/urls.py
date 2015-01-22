from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import *
from core.forms import ContactForm, RaceForm, LocationForm, EventForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView


race_named_forms = (
    ("event", EventForm),
    ("race", RaceForm),
    ("location", LocationForm),
    ("contact", ContactForm)
)

racewizard = RaceWizard.as_view(race_named_forms)

urlpatterns = patterns('',
                       url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'},
                           name="login"),
                       url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name="logout"),
                       url(r'^robots\.txt$', TemplateView.as_view(
                           template_name='robots.txt',
                           content_type='text/plain')),
                       url(r'^$', IntroView.as_view(), name="intro"),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^list$', RaceList.as_view(), name='list_race'),
                       url(r'^race/(?P<slug>.+)$', RaceView.as_view(), name='view_race'),
                       url(r'^search/$', getRacesAjax, name='search_race'),
                       url(r'^create/$', racewizard, name="create_race"),
                       url(r'^update/(?P<slug>.+)$', racewizard, name="edit_race"),
                       url(r'^delete/(?P<slug>.+)$', RaceDelete.as_view(), name="delete_race"),
                       url(r'^tobevalidated/$', RaceValidationList.as_view(), name="validate_racelist"),
                       url(r'^validate/(?P<slug>.+)$', validateRace, name="validate_race"),
                       )

# serve static files on dev
urlpatterns += staticfiles_urlpatterns()
