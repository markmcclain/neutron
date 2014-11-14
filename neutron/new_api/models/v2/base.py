from neutron.new_api.models import base
from neutron.common.constants import ATTR_NOT_SPECIFIED
from neutron.core import core
class V2Model(base.Resource):
    def _from_dict(self, data):
        pass

    def _to_dict(self, is_root=True, include_undefined=False):
        serialized = {
            k:v.value for k,v in self.__resource_attrs__.items()
            if include_undefined or v.value is not ATTR_NOT_SPECIFIED
        }

        if is_root:
            return {self.__name__: serialized}
        else:
            return serialized

    def __json__(self):
        return _self.to_json()

    @classmethod
    def _bulk_model(cls):
        return V2Collection(cls)


class V2Collection(object):
    def __init__(self, items, klass=None):
        if klass is None:
            klass = items[0].__class__
        self.klass = klass
        self.items = items

    def json_schema(self, enforce_required=True):
        schema = self.klass.json_schema(enforce_required=enforce_required)

        bulk_schema = {
            'type': 'object',
            'properties': {
                cls.__plural_name__: {'type': 'array', 'items': schema}
            },
            'required': []
        }
        return bulk_schema

    def _to_dict(self):
        return {
            self.klass.__plural_name__: o._to_dict(is_root=False) for o in data
        }

    def _from_dict(self, data):
        pass

