from django.http import HttpResponseRedirect
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.models import User

from django.shortcuts import get_object_or_404

from django.views.generic import DetailView

from django.template.loader import render_to_string
from django.core.urlresolvers import reverse

# from django.contrib.auth.views import password_reset_done
from registration.backends.default.views import RegistrationView


class CustomRegistrationView(RegistrationView):
    success_url = 'list_race'

    def get_success_url(self, request, user):
        msg = render_to_string('registration/registration_complete.txt')
        messages.success(request, msg)
        return super(RegistrationView, self).get_success_url(request, user)


def custom_password_reset_done(request, **kwargs):
    messages.success(request, render_to_string('registration/password_reset_done.txt'))
    return HttpResponseRedirect(reverse('list_race'))


def custom_password_change_done(request, **kwargs):
    messages.success(request, render_to_string('registration/password_change_done.txt'))
    return HttpResponseRedirect(reverse('user_settings'))


class UserSettingsView(DetailView):
    model = User
    template_name = "accounts/user_settings.html"
    context_object_name = "user"

    def get_object(self):
        return get_object_or_404(User, pk=self.request.user.pk)
