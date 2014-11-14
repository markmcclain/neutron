from neutron.core import base

class AddressPool(Resource):
    pass

class Network(Resource):
    """Manager object for Networks"""
    def query(cls, context, filters=None, marker=None, limit=None,
             reverse=False, sort_keys=None, detailed=False):
        """Retreive a list of API models matching query.

        context: v3 Context Object
        filters: dict of key/value pairs.  Filters are AND and if values are
        list then equivalent to SQL in should be used.
        marker: page marker
        limit: Number of results to return
        reverse: page through results backwards???
        sort_keys: iterable of (key, direction) pairs
        detailed: Return detailed API model (ie all related sub resources)
        """
        import pdb;pdb.set_trace()

    def count(cls, context, filters=None):
        """Retrieve count of resources matching the filter."""
        return len(self.query(context, filters=filters))

    def get(cls, context, resource_id):
        import pdb;pdb.set_trace()

    #@add_pre_hook
    def create(cls, context, api_model):
        import pdb;pdb.set_trace()

    #@add_pre_hook
    def update(self, context, api_model):
        import pdb;pdb.set_trace()

    #@add_pre_hook
    def delete(cls, context, resource_id):
        import pdb;pdb.set_trace()

    def api_model(self, detailed=False):
        import pdb;pdb.set_trace()


class Port(Resource):
    pass


class SecurityGroup(Resource):
    pass


class Routers(Resource):
    pass


class FloatingIps(Resource):
    pass


class Quotas(Resource):
    pass


class Agents(Resource):
    pass


class V3Core(object):
    address_pools = AddressPool
    networks = Network
    ports = Port
    security_groups = SecurityGroup
    routers = Router
    floating_ips = FloatingIp
    quotas = Quota
    # TODO(markmcclain): This should serve as a good ext load test case
    agents = Agent

    def __init__(self):
        # TODO(markmcclain): add hook to load new extension resources
        pass
