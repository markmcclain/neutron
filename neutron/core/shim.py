from neutron.core import base
from neutron import manager

class ShimResourceManager(base.ResourceManager):
    def __init__(self, name, plural_name=None):
        self.name = name
        self.plural = plural_name or name +'s'

    def query(self, context, filters=None, marker=None, limit=None,
              reverse=False, sort_keys=None):

        method = getattr(
            manager.NeutronManager.get_plugin(),
            'get_%s' % self.plural
        )

        result = method(
            context,
            filters=filters,
            marker=marker,
            limit=limit,
            page_reverse=reverse,
            sorts=sort_keys
        )

        # TODO: make this into API object
        return result

    def get(self, context, resource_id):
        import pdb;pdb.set_trace()
        method = getattr(
            manager.NeutronManager.get_plugin(),
            'get_%s' % self.name
        )
        return method(context, resource_id)

    def create(self, context, api_model):
        import pdb;pdb.set_trace()

    def update(self, context, api_model):
        import pdb;pdb.set_trace()

    def delete(self, context, resource_id):
        method = getattr(
            manager.NeutronManager.get_plugin(),
            'delete_%s' % self.name
        )

        return method(context, resource_id)


class Shim(object):
    networks = ShimResourceManager('network')
