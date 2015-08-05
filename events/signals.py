from events.models import Race, Event
from django.db.models.signals import post_delete
from django.dispatch import receiver


@receiver(post_delete, sender=Race)
def post_delete_race(sender, instance, *args, **kwargs):
    if instance.contact:
        if instance.contact.pk:
            instance.contact.delete()
    if instance.location:
        if instance.location.pk:
            instance.location.delete()


@receiver(post_delete, sender=Event)
def post_delete_event(sender, instance, *args, **kwargs):
    if instance.organizer:
        if instance.organizer.pk and instance.organizer.event_set.count() == 0:
            instance.organizer.delete()
