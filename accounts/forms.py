from django import forms
from registration.forms import RegistrationFormUniqueEmail
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class customRegistrationForm(RegistrationFormUniqueEmail):
    """
    Subclass of ``RegistrationForm`` which enforces uniqueness of
    username (case insensitive)

    """
    def clean_username(self):
        """
        Validate that the supplied username is unique for the
        site.

        """
        if User.objects.filter(username__iexact=self.cleaned_data['username']):
            raise forms.ValidationError(_("This username is already in use. Please supply a different username."))
        return self.cleaned_data['username']
