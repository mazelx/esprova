from django.conf import settings
from haystack.backends.elasticsearch_backend import ElasticsearchSearchBackend
from haystack.backends.elasticsearch_backend import ElasticsearchSearchEngine
from haystack.fields import EdgeNgramField as BaseEdgeNgramField
from django.utils import translation
import locale
from haystack.utils import get_identifier
from haystack.exceptions import MissingDependency

try:
    import elasticsearch
except ImportError:
    raise MissingDependency("The 'elasticsearch' backend requires the installation of 'elasticsearch'. Please refer to the documentation.")


# Custom Backend
class CustomElasticBackend(ElasticsearchSearchBackend):

    DEFAULT_ANALYZER = None

    def __init__(self, connection_alias, **connection_options):
        super(CustomElasticBackend, self).__init__(connection_alias, **connection_options)
        user_settings = getattr(settings, 'ELASTICSEARCH_INDEX_SETTINGS', None)
        self.DEFAULT_ANALYZER = getattr(settings, 'ELASTICSEARCH_DEFAULT_ANALYZER', "snowball")
        translation.activate(settings.LANGUAGE_CODE)
        if user_settings:
            setattr(self, 'DEFAULT_SETTINGS', user_settings)

    def build_schema(self, fields):
        content_field_name, mapping = super(CustomElasticBackend, self).build_schema(fields)

        for field_name, field_class in fields.items():
            field_mapping = mapping[field_class.index_fieldname]

            index_analyzer = getattr(field_class, 'index_analyzer', None)
            search_analyzer = getattr(field_class, 'search_analyzer', None)
            field_analyzer = getattr(field_class, 'analyzer', self.DEFAULT_ANALYZER)

            if field_mapping['type'] == 'string' and field_class.indexed:
                if not hasattr(field_class, 'facet_for') and not field_class.field_type in('ngram', 'edge_ngram'):
                    field_mapping['analyzer'] = field_analyzer

            if index_analyzer and search_analyzer:
                field_mapping['index_analyzer'] = index_analyzer
                field_mapping['search_analyzer'] = search_analyzer
                del(field_mapping['analyzer'])

            mapping.update({field_class.index_fieldname: field_mapping})
        return (content_field_name, mapping)

    def more_like_this(self, model_instance, additional_query_string=None,
                       start_offset=0, end_offset=None, models=None,
                       limit_to_registered_models=None, result_class=None, **kwargs):
        from haystack import connections

        if not self.setup_complete:
            self.setup()

        # Deferred models will have a different class ("RealClass_Deferred_fieldname")
        # which won't be in our registry:
        model_klass = model_instance._meta.concrete_model

        index = connections[self.connection_alias].get_unified_index().get_index(model_klass)
        field_name = index.get_content_field()
        params = {}

        if start_offset is not None:
            params['search_from'] = start_offset

        if end_offset is not None:
            params['search_size'] = end_offset - start_offset

        doc_id = get_identifier(model_instance)

        try:
            raw_results = self.conn.mlt(index=self.index_name, doc_type='modelresult', id=doc_id, **params)
        except elasticsearch.TransportError as e:
            if not self.silently_fail:
                raise

            self.log.error("Failed to fetch More Like This from Elasticsearch for document '%s': %s", doc_id, e)
            raw_results = {}

        return self._process_results(raw_results, result_class=result_class)


class CustomElasticSearchEngine(ElasticsearchSearchEngine):
    backend = CustomElasticBackend


# Custom field
class CustomFieldMixin(object):

    def __init__(self, **kwargs):
        self.analyzer = kwargs.pop('analyzer', None)
        self.index_analyzer = kwargs.pop('index_analyzer', None)
        self.search_analyzer = kwargs.pop('search_analyzer', None)
        super(CustomFieldMixin, self).__init__(**kwargs)


class CustomEdgeNgramField(CustomFieldMixin, BaseEdgeNgramField):
    pass
