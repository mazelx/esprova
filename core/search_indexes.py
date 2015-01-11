from core.models import Race
from haystack import indexes


class RaceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    event_id = indexes.CharField(indexed=False, model_attr='event__id')
    date = indexes.DateField(model_attr='date')
    location = indexes.LocationField(model_attr='get_point')
    distance_cat = indexes.CharField(model_attr='distance_cat__name')
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return Race

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
