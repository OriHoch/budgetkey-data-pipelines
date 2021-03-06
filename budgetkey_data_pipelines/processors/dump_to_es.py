from datapackage_pipelines_elasticsearch.processors.dump.to_index import ESDumper
from tableschema_elasticsearch.mappers import MappingGenerator


class BoostingMappingGenerator(MappingGenerator):

    @classmethod
    def _convert_type(cls, schema_type, field, prefix):
        prop = super(BoostingMappingGenerator, cls)._convert_type(schema_type, field, prefix)
        if schema_type == 'string':
            if 'es:title' in field:
                prop['boost'] = 10
        return prop


class DumpToElasticSearch(ESDumper):
    
    def __init__(self):
        super(DumpToElasticSearch, self).__init__(mapper_cls=BoostingMappingGenerator)


DumpToElasticSearch()()