from neutron.new_api.models import attribute as attr
from . import base

VALID_STATUSES = [
    'ACTIVE',
    'DOWN',
    'CREATING',
    'DELETING',
    'UPDATING',
    'ERROR'
]


class Network(base.V2Model):
    id = attr.UUID()
    name = attr.String(255)
    admin_state_up = attr.Boolean()
    status = attr.Enum(VALID_STATUSES)
    shared = attr.Boolean()
    tenant_id = attr.Boolean()
