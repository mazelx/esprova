from django.db import models
from events.models import Race
from django.contrib.auth.models import User

import os
from binascii import hexlify


class UserPlanning(models.Model):
    user = models.ForeignKey(User, unique=True)
    secret_key = models.CharField(max_length=10)

    def natural_key(self):
        return (self.user)

    def __str__(self):
        return "Planning {0}".format(self.user)

    def save(self, *args, **kwargs):
        if not self.secret_key:
            self.secret_key = hexlify(os.urandom(5))
        super(UserPlanning, self).save(*args, **kwargs)


class ShortlistedRace(models.Model):
    """
        Represent a shortlisted race

    """
    user_planning = models.ForeignKey(UserPlanning, related_name='races')
    race = models.ForeignKey(Race)
    registered = models.BooleanField(default=False)

    def natural_key(self):
        return (self.race)

    def __str__(self):
        return "{0}".format(self.race)
