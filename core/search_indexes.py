from core.models import Race
from haystack import indexes


class RaceIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    name = indexes.CharField(model_attr='event__name')
    distance_cat = indexes.CharField(model_attr='distance_cat__name')
    # distance_cat_long = indexes.CharField(model_attr='distance_cat__long_name')
    # federation = indexes.CharField(model_attr='federation__name')
    # label = indexes.CharField(model_attr='label__name')
    city = indexes.CharField(model_attr='location__city')
    # Todo : région / département
    # ...
    contact = indexes.CharField(model_attr='contact')

    def get_model(self):
        return Race

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
