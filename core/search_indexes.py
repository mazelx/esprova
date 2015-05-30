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
    event_title = indexes.CharField(model_attr='event__name', boost=1.5)
    sport = indexes.CharField(model_attr='sport__name')
    date = indexes.DateField(model_attr='date', faceted=True)
    administrative_area_level_1 = indexes.CharField(model_attr='location__administrative_area_level_1', faceted=True)
    administrative_area_level_2 = indexes.CharField(model_attr='location__administrative_area_level_2', faceted=True)
    location = indexes.LocationField(model_attr='location__get_point')
    distance_cat = indexes.CharField(model_attr='distance_cat__name', faceted=True)
    rendered = indexes.CharField(use_template=True, indexed=False)
    slug = indexes.CharField(indexed=False, model_attr='slug')
    validated = indexes.BooleanField(model_attr='event__validated')

    def get_model(self):
        return Race

    def index_queryset(self, using=None):
        return self.get_model().objects.all()
