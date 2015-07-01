from events.models import Race
from django.db import models
from haystack import signals
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from planning.models import UserPlanning


class RaceOnlySignalProcessor(signals.BaseSignalProcessor):
    def setup(self):
        # Listen only to the ``Race`` model.
        models.signals.post_save.connect(self.handle_save, sender=Race)
        models.signals.post_delete.connect(self.handle_delete, sender=Race)

    def teardown(self):
        # Disconnect only for the ``Race`` model.
        models.signals.post_save.disconnect(self.handle_save, sender=Race)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Race)


@receiver(post_save, sender=User)
def create_planning(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        up = UserPlanning(user=user)
        up.save()
