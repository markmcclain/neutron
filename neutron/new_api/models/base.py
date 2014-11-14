import six

from . import attribute


class ResourceMeta(type):
    def __new__(cls, name, bases, attrs):
        resource_attrs = {}
        for key, value in attrs.items():
            if not isinstance(value, attribute.AttributeBase):
                continue

            # set the name of the attribute
            if value.name is None:
                value.name = key

            resource_attrs[value.name] = value

        attrs['__unsaved__'] = set()
        attrs['__resource_attrs__'] = resource_attrs
        attrs['__name__'] = attrs.get('__name__', name).lower()

        if '__plural_name__' not in attrs:
            attrs['__plural_name__'] = '%ss' % attrs['__name__']

        if '__core_resource__' not in attrs:
            attrs['__core_resource__'] = attrs['__plural_name__']

        cls._core_resource = attrs['__core_resource__']

        new_class = type.__new__(cls, name, bases, attrs)

        # build a registry of model on this base
        if not hasattr(cls, '__resources__'):
            cls.__resources__ = {}
        cls.__resources__[name] = new_class

        return new_class

    @classmethod
    def class_for_name(cls, name):
        return getattr(cls, '__resources__', {}).get(name)

@six.add_metaclass(ResourceMeta)
class Resource(object):
    """The Resource base class to contain all logic for a resource.

       A base class is used so that the declarative attributes can be added
       by subclasses easier.
    """

    def __init__(self, **kwargs):
        self._set_values(kwargs)
        self._all_attrs_mutable = True

    def __dir__(self):
        return self.__resource_attrs__.keys()

    @property
    def _valid(self):
        return (
            not bool(self._blank_required_attributes) and
            getattr(self, 'validate', lambda: True)()
        )

    @property
    def _blank_required_attributes(self):
        required = (k for k,v in self.__resource_attrs__.items() if v.required)
        return list(k for k in required if not self.__dict__.get(k))

    @property
    def _name(self):
        return self.__name__

    @property
    def _plural_name(self):
        return self.__plural_name__

    def _set_values(self, data, force=False):
        try:
            self._all_attrs_mutable = True
            for key, value in data.items():
                if key in self.__resource_attrs__:
                    if isinstance(self.__resource_attrs__[key],
                                  attribute.Collection):
                        setattr(self, key, value)
                    elif force:
                        self.__dict__[key] = value
                    else:
                        setattr(self, key, value)
        finally:
            self._all_attrs_mutable = False

    @classmethod
    def json_schema(cls, enforce_required=True):
        schema= {
            'type': 'object',
            'properties': {},
            'required': []
        }

        for attr in cls.__resource_attrs__.values():
            schema['properties'][attr.name] = attr.json_schema()
            if enforce_required and attr.required:
                schema['required'].append(attr.name)

        return schema
