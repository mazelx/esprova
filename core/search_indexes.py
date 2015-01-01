from core.models import Race
from haystack import indexes


class RaceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    location = indexes.LocationField(model_attr='get_point')
    rendered = indexes.CharField(use_template=True, indexed=False)

    def get_model(self):
        return Race

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
