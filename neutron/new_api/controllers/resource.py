import pecan
from pecan import rest

from neutron.core import core


class CollectionController(rest.RestController):
    def __init__(self, api_model, core_manager):
        self.manager = core_manager
        self.api_model = api_model

    @pecan.expose()
    def get_all(self, fields=(), **kwargs):
        result = self.manager.query(
            pecan.request.context
            # add filter/pagination
        )

        import pdb;pdb.set_trace()
        return self.api_model.bulk_serializer(result)

    @pecan.expose()
    def get_one(self, pk):
        result = self.manager.query(
            pecan.request.context
            # add filter/pagination
        )

        import pdb;pdb.set_trace()
        return dict()

    @pecan.expose()
    def post(self, pk, **data):
        import pdb;pdb.set_trace()
        return dict()

    @pecan.expose()
    def edit(self, pk, **data):
        import pdb;pdb.set_trace()
        return dict()

    @pecan.expose()
    def delete(self):
        import pdb;pdb.set_trace()
        return dict()
