from django.apps import AppConfig


class EventsAppConfig(AppConfig):
    name = 'events'

    def ready(self):
        import events.signals
