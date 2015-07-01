from django.conf.urls import url, patterns, include
from accounts.views import *

urlpatterns = patterns('',
                       url(r'^register/$', CustomRegistrationView.as_view(), name="registration_register"),
                       url(r'^reset/done/$', custom_password_reset_done, name="auth_password_reset_done"),
                       url(r'^password/change/done/$', custom_password_change_done, name="auth_password_change_done"),
                       url(r'^reset/done/$', custom_password_reset_done, name="auth_password_reset_done"),
                       url(r'^settings/$', UserSettingsView.as_view(), name="user_settings"),
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           CustomActivationView.as_view(),
                           name='registration_activate'),
                       url(r'', include('registration.backends.default.urls')),
                       )
