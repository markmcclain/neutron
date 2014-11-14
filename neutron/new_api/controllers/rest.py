import abc
import six

from pecan

class DemoResource(object):
    def get_all(self, **args):
        pass

    def create(self, **args):
        pass

    def get_one(self, pk):
        pass

    def update(self, instance, **args):
        pass

    def delete(self, instance):
        pass

class ResourceControllerMetaclass(type):
    def __new__(cls, name, bases, attrs):
        # set the correct content_type


@six.add_metaclass(ResourceControllerMetaclass)
class ResourceController(object):
    @pecan.expose(template='json', generic=True)
    def index(self):
        # return all list
        pass

    @index.when(method='POST')
    def index_post(self):
        # create object
        pass

    @pecan.expose()
    def _lookup(self, obj_id, *reminader):
        obj = self.get_object(obj_id)

        if obj:
            return ResourceControllerHelper(self, obj), *remainder
        else:
            pecan.abort(404)


class ResourceControllerHelper(object):
    def __init__(self, parent, obj):
        self.parent = parent
        self.obj = obj

        #remove the methods not supported by the delegate
        method_map = {'update': 'index_put', 'delete': 'index_delete'}

        for method, rest_controller in method_map.items():
            if not hasattr(self.parent, method):
                delattr(self, rest_controller)

    @pecan_expose(template='json', generic=True)
    def index(self):
        # return Object
        pass

    @index.when(method='PUT')
    def index_update(self, **data):
        pass

    @index.when(method='DELETE')
    def index_delete(









class SimpleRestCollection(object):
    def __init__(self, obj_delegate):
        content_type = getattr(obj_delegate, 'CONTENT_TYPE', None)
        self.obj_delegate = obj_delegate
        self.index = pecan.expose(content_type, generic=True)(self._idx_proto)

        if hasattr(obj_delegate, 'create'):
            self.create = self.index.when(method='POST')(self._create_proto)

    @pecan.expose()
    def _lookup(self, pk, *remainder):
        obj = self.obj_ctlr.get_
        if obj:
            return self.obj_ctlr

    def _idx_proto(self, **kwargs):
        return self.obj_ctlr.collection(**kwargs)

    def _create_proto(self, **kwargs):
        return self.obj_ctlr.create(**kwargs)

@six.add_metaclass(abc.ABCMeta)
class SimpleRest(object):
    def __new__(cls, *args, **kwargs):
        #wrap with collection manager
        me = super(SimpleRest, self).__new__(cls)
        me.__init__(*args, **kwargs)
        return SimpleRestCollection(me)

    def __init__(self, obj):
        self.obj = obj

    @abc.abstractmethod
    def get_object(self, pk):
        pass

    def collection(self):
        return ''
    
    @pecan.expose(CONTENT_TYPE, generic=True)
    def index(self):




@add_all_and_post_handlers
class TestRestController(SimpleRest):
    CONTENT_TYPE = 'json'

    def __init__(self):
        pass

    def get_object(self, pk):
        return pk

    def create(self, **data):
        pass

    def update(self, pk, **data):
        pass

    def get(self, pk):
        return serializer(pk)

    def delete(self, pk):
        pass
