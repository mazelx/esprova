from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import *
from core.forms import ContactForm, RaceForm, LocationForm, EventForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from rest_framework import routers
from api import views

from planning.views import *

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView


router = routers.DefaultRouter()
router.register(r'/race', views.RaceViewSet)
router.register(r'/sport', views.SportViewSet)
router.register(r'/event', views.EventViewSet)
router.register(r'/distancecat', views.DistanceCategoryViewSet)
router.register(r'/contact', views.ContactViewSet)
router.register(r'/location', views.LocationViewSet)



race_named_forms = (
    # ("eventReference", EventReferenceForm),
    # ("event", EventForm),
    ("race", RaceForm),
    ("location", LocationForm),
    ("contact", ContactForm)
)

race_edit = RaceEdit.as_view(race_named_forms)

sqs = SearchQuerySet().facet('distance_cat')


urlpatterns = patterns('',
                       # Login
                       url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'},
                           name="login"),
                       
                       url(r'^logout$', 'django.contrib.auth.views.logout', {'next_page': 'intro'},
                           name="logout"),

                       # Introduction
                       url(r'^$', IntroView.as_view(), name="intro"),

                       # Race list (main page)
                       # url(r'^search\/?$', RaceList.as_view(), name='list_race'),
                       url(r'^races\/?$', RaceList.as_view(), name='list_race'),
                       # url(r'^facet$', FacetTest.as_view(), name='list_facet_race'),

                       url(r'^facet$', FacetedSearchView(form_class=FacetedSearchForm, 
                                                         searchqueryset=sqs,
                                                         template="core/test_facet.html"
                                                         ), name='list_facet_race'),


                       # CRUD
                       url(r'^races/(?P<slug>[-\w\d]+)_(?P<pk>\d+)$', RaceView.as_view(), name='view_race'),
                       url(r'^events/(?P<pk>\d+)$', EventView.as_view(), name='view_event'),
                       # url(r'^update/(?P<slug>[-\w\d]+)_(?P<pk>\d+)$', racewizard, name="edit_race"),
                       
                       url(r'^create/$', create_event, name='create_event'),
                       url(r'^update/(?P<pk>\d+)$', update_event, name='update_event'),
                       url(r'^delete/(?P<pk>\d+)$', EventDelete.as_view(), name='delete_event'),


                       url(r'^update/(?P<event>\d+)/(?P<pk>\d+)$', race_edit, name="update_race"),
                       url(r'^update/(?P<event>\d+)/add_race$', race_edit, name="add_race"),
                       url(r'^update/(?P<event>\d+)/delete_race/(?P<pk>\d+)$', RaceDelete.as_view(), name="delete_race"),

                       # Ajax views
                       url(r'^api/races/$', ajx_get_races, name='ajx_search_race'),
                       url(r'^api/delete/race/(?P<pk>\d+)$', ajx_delete_race, name="ajx_delete_race"),
                       # url(r'^api/delete/(?P<pk>\d+)$', ajx_delete_event, name="ajx_delete_event"),
                       url(r'^api/sport-session/', ajx_sport_session, name="ajx_sport_session"),
                       url(r'^api/distance/(?P<name>[\w ]+)$', ajx_get_distances, name="ajx_get_distances"),

                       # API
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^api-rest', include(router.urls)),

                       # Admin
                       url(r'^admin/', include(admin.site.urls)),

                       # Robots
                       url(r'^robots\.txt$', TemplateView.as_view(
                           template_name='robots.txt',
                           content_type='text/plain')),

                       url(r'^legal/$', TemplateView.as_view(
                           template_name='legal.html'), name='legal'),

                       # UI refactor
                       # url(r'^listv2/$', TemplateView.as_view(template_name='core/ui_refactor.html')),
                       # url(r'^racev2/(?P<slug>[-\w\d]+)_(?P<pk>\d+)$', RaceViewv2.as_view(), name='view_racev2'),

                       url(r'^planning/$', PlanningList.as_view(), name='planning'),
                       url(r'^api/planning/add$', add_race_to_planning, name='planning_add_race'),
                       url(r'^api/planning/remove$', remove_race_from_planning, name='planning_remove_race'),

                       url(r'^validation$', EventValidationList.as_view(), name='list_event_validation'),

                       )

# serve static files on dev
urlpatterns += staticfiles_urlpatterns()
