from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import RaceView, RaceList

urlpatterns = patterns('',
                       url(r'^admin?/', include(admin.site.urls)),
                       url(r'^$', RaceList.as_view(), name='racelist'),
                       url(r'^race/(?P<pk>\d+)$', RaceView.as_view(), name='raceview'),
                       url(r'^racejson/$', RaceList.getRacesFromLatLng, name='getrace'),
                       )
