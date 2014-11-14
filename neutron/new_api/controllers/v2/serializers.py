import abc

import jsonschema


class BaseV2Serializer(object):
    model_class = None

    def __init__(self):
        pass
    @abc.abstractmethod
    def deserialize(self, json_data):
        pass

    @abc.abstractmethod
    def serialize(self, obj):
        pass

    def json_schema(self):
        properties = _build_properties(self.model_class)

        schema = {
            'type': 'object',
            'properties': properties
        }

        return schema

    def bulk_json_schema(self):
        schema = {

        }


    def _build_properties(self):
        return {
            (v.api_name or k):build_type_info(v)
            for k,v in self.model_class.attributes
        }
