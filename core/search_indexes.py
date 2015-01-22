from core.models import Race
from haystack import indexes
from search_backends.elastic_backend import CustomEdgeNgramField
# from elasticstack.fields import CharField


class RaceIndex(indexes.SearchIndex, indexes.Indexable):
    # text = CharField(document=True, use_template=True, analyzer='esprova_analyzer')
    text = CustomEdgeNgramField(document=True, use_template=True,
                                index_analyzer="edgengram_analyzer",
                                search_analyzer="search_analyzer")
    event_id = indexes.CharField(indexed=False, model_attr='event__id')
    date = indexes.DateField(model_attr='date')
    location = indexes.LocationField(model_attr='get_point')
    distance_cat = indexes.CharField(model_attr='distance_cat__name')
    rendered = indexes.CharField(use_template=True, indexed=False)
    validated = indexes.BooleanField(indexed=False, model_attr='validated')
    slug = indexes.CharField(indexed=False, model_attr='slug')

    def get_model(self):
        return Race

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
