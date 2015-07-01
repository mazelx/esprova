from django.contrib.auth.models import User
from django.db.models.signals import post_save

from planning.models import UserPlanning


def create_planning(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        up = UserPlanning(user=user)
        up.save()

post_save.connect(create_planning, sender=User)
