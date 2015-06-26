from django.conf.urls import patterns, include, url, handler404
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.sitemaps.views import sitemap

from django.views.generic import TemplateView

from core.views import *
from events.views import *
from events.forms import ContactForm, RaceForm, LocationForm


from planning.views import *

handler404 = "core.views.handler404"

# Prepare for Race edition
race_named_forms = (
    ("race", RaceForm),
    ("location", LocationForm),
    ("contact", ContactForm)
)
race_edit = RaceEdit.as_view(race_named_forms)

if settings.ALLOW_SEARCHBOTS:
    robot_path = 'robots.txt'
else:
    robot_path = 'robots_deny_all.txt'

urlpatterns = patterns('',
                       # 404 test
                       url(r'^404$', handler404),
                       url(r'^500$', handler500),


                       # Introduction
                       url(r'^$', IntroView.as_view(), name="intro"),

                       # Search
                       url(r'^races\/?$', RaceList.as_view(), name='list_race'),

                       # View
                       url(r'^races/(?P<slug>[-\w\d]+)_(?P<pk>\d+)$', RaceView.as_view(), name='view_race'),
                       url(r'^events/(?P<pk>\d+)$', EventView.as_view(), name='view_event'),

                       # CRUD
                       url(r'^create/$', create_event, name='create_event'),
                       url(r'^update/(?P<pk>\d+)$', update_event, name='update_event'),
                       url(r'^delete/(?P<pk>\d+)$', EventDelete.as_view(), name='delete_event'),
                       url(r'^soft_delete/(?P<pk>\d+)$', EventSoftDelete.as_view(), name='soft_delete_event'),

                       url(r'^update/(?P<event>\d+)/(?P<pk>\d+)$', race_edit, name="update_race"),
                       url(r'^update/(?P<event>\d+)/add_race$', race_edit, name="add_race"),
                       url(r'^update/(?P<event>\d+)/delete_race/(?P<pk>\d+)$',
                           RaceDelete.as_view(),
                           name="delete_race"),

                       # Planning
                       url(r'^planning/$', redirect_to_planning, name='planning'),
                       url(r'^planning/(?P<username>[-\w\d]+)$', PlanningList.as_view(), name='planning'),

                       # Validation
                       url(r'^validation$', EventValidationList.as_view(), name='list_event_validation'),

                       # Robots
                       url(r'^robots\.txt$', TemplateView.as_view(
                           template_name=robot_path,
                           content_type='text/plain')),

                       # legal
                       url(r'^legal/$', TemplateView.as_view(
                           template_name='legal.html'), name='legal'),

                       # sitemap
                       url(r'', include('core.urls')),

                       # Admin
                       url(r'^admin/', include(admin.site.urls)),

                       # Accounts
                       url(r'^user/', include('accounts.urls')),

                       # API
                       url(r'^api/', include('api.urls')),

                       )

# serve static files on dev
urlpatterns += staticfiles_urlpatterns()
