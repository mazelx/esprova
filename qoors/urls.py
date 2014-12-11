from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import ListView
from core.models import Race

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^list/', ListView.as_view(model=Race)),
                       )
