from django.template.loader import render_to_string
from django.contrib import messages
from registration.backends.default.views import RegistrationView


class CustomRegistrationView(RegistrationView):
    success_url = 'list_race'

    def get_success_url(self, request, user):
        msg = render_to_string('registration/registration_complete.txt')
        messages.success(request, msg)
        return super(RegistrationView, self).get_success_url(request, user)
