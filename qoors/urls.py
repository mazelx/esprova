from django.conf.urls import patterns, include, url
from django.contrib import admin
from core.views import RaceView, RaceList, getRacesAjax, RaceCreate

urlpatterns = patterns('',
                       url(r'^admin?/', include(admin.site.urls)),
                       url(r'^$', RaceList.as_view(), name='list_race'),
                       url(r'^race/(?P<pk>\d+)$', RaceView.as_view(), name='view_race'),
                       url(r'^search/$', getRacesAjax, name='search_race'),
                       url(r'^create?/', RaceCreate.as_view(), name='create_race'),
                       )
