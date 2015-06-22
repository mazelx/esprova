from django.db import models
from events.models import Race
from django.contrib.auth.models import User


class ShortlistedRace(models.Model):
    """
        Represent a shortlisted race

    """
    class Meta:
        unique_together = (("user", "race"),)

    user = models.ForeignKey(User)
    race = models.ForeignKey(Race)
    registered = models.BooleanField(default=False)

    def natural_key(self):
        return (self.user, self.race)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.race)
