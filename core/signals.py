from core.models import Race
from django.db import models
from haystack import signals


class RaceOnlySignalProcessor(signals.BaseSignalProcessor):
    def setup(self):
        # Listen only to the ``Race`` model.
        models.signals.post_save.connect(self.handle_save, sender=Race)
        models.signals.post_delete.connect(self.handle_delete, sender=Race)

    def teardown(self):
        # Disconnect only for the ``Race`` model.
        models.signals.post_save.disconnect(self.handle_save, sender=Race)
        models.signals.post_delete.disconnect(self.handle_delete, sender=Race)
