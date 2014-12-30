from core.models import Event, Race
from haystack import indexes


class EventIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='name', faceted=True)

    def get_model(self):
        return Event

    def index_queryset(self):
        return self.get_model().objects.all()