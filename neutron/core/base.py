import abc
import six

ASCENDING = '+'
DESCENDING = '-'

class NotFoundError(Exception):
    pass

class NotAuthorizedError(ValueError):
    pass

@six.add_metaclass(abc.ABCMeta)
class ResourceManager(object):
    """Manager object for backend representation of resource"""
    @abc.abstractmethod
    def query(self, context, filters=None, marker=None, limit=None,
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

    def count(self, context, filters=None):
        """Retrieve count of resources matching the filter."""
        return len(self.query(context, filters=filters))

    @abc.abstractmethod
    def get(self, context, resource_id):
        """Retrieve API model representation for resource """

    #@add_pre_hook
    @abc.abstractmethod
    def create(self, context, api_model):
        """Create resource from api_model"""

    #@add_pre_hook
    @abc.abstractmethod
    def update(self, context, api_model):
        """Update resource with information from API model."""

    #@add_pre_hook
    @abc.abstractmethod
    def delete(self, context, resource_id):
        """Delete resource for given id."""
