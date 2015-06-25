from django.conf.urls import url, patterns, include
from accounts.views import *

urlpatterns = patterns('',
                       url(r'^register$', CustomRegistrationView.as_view(), name="registration_register"),
                       url(r'^reset/done$', custom_password_reset_done, name="auth_password_reset_done"),
                       url(r'^password/change/done/$', custom_password_change_done, name="auth_password_change_done"),
                       url(r'^reset/done$', custom_password_reset_done, name="auth_password_reset_done"),
                       url(r'^settings$', UserSettingsView.as_view(), name="user_settings"),
                       url(r'', include('registration.backends.default.urls')),
                       )
