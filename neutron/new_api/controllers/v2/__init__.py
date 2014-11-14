import pecan
from pecan import rest

from neutron.new_api.controllers import resource
from neutron.new_api.models import v2

class YARestController(object):
    def __init__(self, resource_manager, parent=None):
        self.manager = manager
        self.parent = parent

    def get_object(self, pk):
        return None

    def create(self, pk):
        pass

    def delete(self, pk):
        pass

    def update(self, pk, data):
        pass


class V2ResourceController(rest.RestController):
    def __init__(self, resource):
        self.resource = resource

    @pecan.expose('json')
    def get_all(self, fields=(), **kwargs):
        result = self._resource._manager.query(
            pecan.request.context,
        )
        import pdb;pdb.set_trace()
        return self.resource.bulk_to_dict(result)

    @pecan.expose('json')
    def get_one(self, id):
        result = self._resource._manager.get(pecan.request.context, id)
        import pdb;pdb.set_trace()
        return result

    @pecan.expose('json')
    def post(self):
        pass

    @pecan.expose('json')
    def put(self, id):
        pass

    @pecan.expose()
    def delete(self, id):
        self._resource._manager.delete(id)

class V2Controller(object):
    networks = resource.CollectionController(v2.Network)

    @pecan.expose()
    def _lookup(self, *remainder):
        #import pdb;pdb.set_trace()
        pecan.abort(422)
