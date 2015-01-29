from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import *
from core.forms import ContactForm, RaceForm, LocationForm, EventReferenceForm
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.generic import TemplateView
from rest_framework import routers
from api import views

from haystack.forms import FacetedSearchForm
from haystack.query import SearchQuerySet
from haystack.views import FacetedSearchView


router = routers.DefaultRouter()
router.register(r'/race', views.RaceViewSet)
router.register(r'/sport', views.SportViewSet)
router.register(r'/event', views.EventReferenceViewSet)
router.register(r'/distancecat', views.DistanceCategoryViewSet)
router.register(r'/contact', views.ContactViewSet)
router.register(r'/location', views.LocationViewSet)



race_named_forms = (
    ("event", EventReferenceForm),
    ("race", RaceForm),
    ("location", LocationForm),
    ("contact", ContactForm)
)

racewizard = RaceWizard.as_view(race_named_forms)

sqs = SearchQuerySet().facet('distance_cat')


urlpatterns = patterns('',
                       # Login
                       url(r'^login$', 'django.contrib.auth.views.login', {'template_name': 'core/login.html'},
                           name="login"),
                       url(r'^logout$', 'django.contrib.auth.views.logout_then_login', name="logout"),

                       # Introduction
                       url(r'^$', IntroView.as_view(), name="intro"),

                       # Race list (main page)
                       url(r'^list$', RaceList.as_view(), name='list_race'),
                       # url(r'^facet$', FacetTest.as_view(), name='list_facet_race'),

                       url(r'^facet$', FacetedSearchView(form_class=FacetedSearchForm, 
                                                         searchqueryset=sqs,
                                                         template="core/test_facet.html"
                                                         ), name='list_facet_race'),


                       # CRUD
                       url(r'^create/$', racewizard, name="create_race"),
                       url(r'^race/(?P<slug>[-\w\d]+)_(?P<pk>\d+)$', RaceView.as_view(), name='view_race'),
                       url(r'^update/(?P<slug>[-\w\d]+)_(?P<pk>\d+)$', racewizard, name="edit_race"),
                       url(r'^delete/(?P<slug>[-\w\d]+)_(?P<pk>\d+)$', RaceDelete.as_view(), name="delete_race"),

                       url(r'^validate/$', RaceValidationList.as_view(), name="validate_racelist"),

                       # Ajax views
                       url(r'^ajx/search/$', ajx_get_races, name='ajx_search_race'),
                       url(r'^ajx/delete/(?P<pk>\d+)$', ajx_delete_race, name="ajx_delete_race"),
                       url(r'^ajx/validate/(?P<pk>\d+)$', ajx_validate_race, name="ajx_validate_race"),

                       # API
                       url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
                       url(r'^api', include(router.urls)),

                       # Admin
                       url(r'^admin/', include(admin.site.urls)),

                       # Robots
                       url(r'^robots\.txt$', TemplateView.as_view(
                           template_name='robots.txt',
                           content_type='text/plain')),

                       )

# serve static files on dev
urlpatterns += staticfiles_urlpatterns()
