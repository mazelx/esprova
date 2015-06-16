from django.conf.urls import url, patterns, include
from accounts.views import *

urlpatterns = patterns('',
                       url(r'', include('registration.backends.default.urls')),
                       url(r'^register', CustomRegistrationView.as_view(), name="registration_register"),
                       url(r'^reset/done', custom_password_reset_done, name="auth_password_reset_done"),
                       )
