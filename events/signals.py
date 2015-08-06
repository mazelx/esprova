from events.models import Race, Event
from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


@receiver(post_delete, sender=Race)
def post_delete_race(sender, instance, *args, **kwargs):
    try:
        if instance.contact:
            if instance.contact.pk:
                instance.contact.delete()
    except ObjectDoesNotExist:
        pass

    try:
        if instance.location:
            if instance.location.pk:
                instance.location.delete()
    except ObjectDoesNotExist:
        pass


@receiver(post_delete, sender=Event)
def post_delete_event(sender, instance, *args, **kwargs):
    try:
        if instance.organizer:
            if instance.organizer.pk:
                if instance.organizer.event_set.count() == 0:
                    instance.organizer.delete()
    except ObjectDoesNotExist:
        pass
