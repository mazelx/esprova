from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login
from django.contrib.auth.models import User

from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404

from django.views.generic import DetailView

from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

# from django.contrib.auth.views import password_reset_done
from registration.backends.default.views import RegistrationView, ActivationView

from registration.signals import user_activated

import time
import jwt
import uuid
import urllib


class CustomRegistrationView(RegistrationView):
    success_url = 'list_race'

    def get_success_url(self, request, user):
        msg = render_to_string('registration/registration_complete.txt')
        messages.success(request, msg)
        return super(CustomRegistrationView, self).get_success_url(request, user)


class CustomActivationView(ActivationView):
    success_url = 'list_race'

    def get_success_url(self, request, user):
        msg = render_to_string('registration/activation_complete.txt')
        messages.success(request, msg)
        return (self.success_url, (), {})


def custom_password_reset_done(request, **kwargs):
    messages.success(request, render_to_string('registration/password_reset_done.txt'))
    return HttpResponseRedirect(reverse('list_race'))


def custom_password_change_done(request, **kwargs):
    messages.success(request, render_to_string('registration/password_change_done.txt'))
    return HttpResponseRedirect(reverse('user_settings'))


# Auto login user when activated
def login_on_activation(sender, user, request, **kwargs):
    """Logs in the user after activation"""
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

# Registers the function with the django-registration user_activated signal
user_activated.connect(login_on_activation)


class UserSettingsView(DetailView):
    model = User
    template_name = "accounts/user_settings.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)


# This example relies on you having install PyJWT, `sudo easy_install PyJWT` - you can
# read more about this in the GitHub repository https://github.com/progrium/pyjwt

@login_required
def sso_zendesk(request):
    payload = {
        "iat": int(time.time()),
        "jti": str(uuid.uuid1()),
        "name": request.user.username,
        "email": request.user.email
    }

    subdomain = "esprova"
    shared_key = "nnMNVBEKLB6woqM2BZwyuFGMNmPz1ddo1Dvl7VpZlAjULmAx"
    jwt_string = jwt.encode(payload, shared_key)
    location = "https://" + subdomain + ".zendesk.com/access/jwt?jwt=" + jwt_string.decode()
    return_to = request.GET.get('return_to')

    if return_to is not None:
        location += "&return_to=" + urllib.parse.quote(return_to)


    # from json import dumps
    # from django.conf import settings
    # if settings.DEBUG:
    #     return HttpResponse(dumps(payload))

    return HttpResponseRedirect(location)
