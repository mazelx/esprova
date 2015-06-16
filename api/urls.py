from django.conf.urls import url, include
from rest_framework import routers
from api.views import *
from planning.views import add_race_to_planning, remove_race_from_planning

router = routers.DefaultRouter()
router.register(r'/race', RaceViewSet)
router.register(r'/sport', SportViewSet)
router.register(r'/event', EventViewSet)
router.register(r'/distancecat', DistanceCategoryViewSet)
router.register(r'/contact', ContactViewSet)
router.register(r'/location', LocationViewSet)


# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^rest', include(router.urls)),
    # Ajax views
    url(r'^races/$', ajx_get_races, name='ajx_search_race'),
    url(r'^delete/race/(?P<pk>\d+)$', ajx_delete_race, name="ajx_delete_race"),
    # url(r'^delete/(?P<pk>\d+)$', ajx_delete_event, name="ajx_delete_event"),
    url(r'^sport-session/', ajx_sport_session, name="ajx_sport_session"),
    url(r'^distance/(?P<name>[\w ]+)$', ajx_get_distances, name="ajx_get_distances"),
    url(r'^validate/(?P<pk>\d+)$', ajx_validate_event, name="ajx_validate_event"),
    url(r'^planning/add$', add_race_to_planning, name='planning_add_race'),
    url(r'^planning/remove$', remove_race_from_planning, name='planning_remove_race'),
]
