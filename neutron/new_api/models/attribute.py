from neutron.common.constants import ATTR_NOT_SPECIFIED
UUID_PATTERN = '^[0-9a-f]{8}(-[0-9a-f]{4}){3}-[0-9a-f]{12}$'


class AttributeBase(object):
    description = 'A base field'

    def __init__(self, default=ATTR_NOT_SPECIFIED, read_only=False,
                 required=True, blank=False, name=None):

        self.value = default
        self.default = default
        self.read_only = read_only
        self.blank = blank
        self.required = required
        self.name = name
        self.schema = {}
        if self.default is not ATTR_NOT_SPECIFIED:
            self.schema['default'] = self.default

    def is_mutable(self, value):
        if read_only:
            raise AttributeError(_('%s attribute is read-only') % self.name)
        elif not self.blank and not value:
            raise TypeError(_('%s attribute cannot be None') % self.name)

    def __set__(self, instance, value):
        if not instance._all_attrs_mutable:
            self._is_mutable(value)

        if hasattr(self, 'coerce'):
            value = self.coerce(instance, value)

        if value is not None and hasattr(self, 'validator'):
            self.validator(value)

        instance.__dict__[self.name] = value
        instance.__unsaved__.add(self.name)

    def __get__(self, instance, owner):
        return instance.__dict__.get(self.name, self.default)

    @property
    def api_name(self):
        return self.name

    def json_schema(self):
        return self.schema


class BaseString(AttributeBase):
    description ='A string attribute'

    def __init__(self, **kwargs):
        super(BaseString, self).__init__(**kwargs)
        self.schema['type'] = 'string'

    def coerce(self, instance, value):
        return unicode(value)


class String(BaseString):
    def __init__(self, min_length=None, max_length=None, **kwargs):
        super(String, self).__init__(**kwargs)
        self.min_length = min_length
        self.max_length = max_length
        if self.min_length is not None and self.min_length > 0:
            self.schema['minLength'] = self.min_length

        if self.max_length is not None and self.max_length > 0:
            self.schema['maxLength'] = self.max_length


class RegularExpression(String):
    def __init__(self, pattern='.', **kwargs):
        super(RegularExpression, self).__init__(**kwargs)
        self.pattern = pattern
        self.schema['pattern'] = self.pattern


class UUID(BaseString):
    description = 'a UUID attribute'
    def __init__(self, **kwargs):
        super(UUID, self).__init__(**kwargs)
        self.schema['pattern'] = UUID_PATTERN

    def coerce(self, instance, value):
        return str(value)


class Boolean(AttributeBase):
    description = 'a boolean attribute'

    def __init__(self, **kwargs):
        super(Boolean, self).__init__(**kwargs)
        self.schema['type'] = 'boolean'

    def coerce(self, instance, value):
        return bool(value)


class Integer(AttributeBase):
    description = 'an integer attribute'

    def __init__(self, **kwargs):
        super(Boolean, self).__init__(**kwargs)
        self.schema['type'] = 'number'

    def coerce(self, instance, value):
        return int(value)


class Enum(AttributeBase):
    description = 'An enumerated type field'

    def __init__(self, members=(), **kwargs):
        super(Enum, self).__init__(**kwargs)
        self.schema['enum'] = list(set(members))


#### TODO
class Cidr(String):
    description = 'An attribute in Cidr Notation'

class IpAddress(String):
    description = 'An IP address attribute'


class Macaddress(String):
    description = 'A MAC address attribute'


class ResourceAttributeBase(AttributeBase):
    def __init__(self, resource_class, *args, **kwargs):
        super(ResourceAttributeBase, self).__init__(*args, **kwargs)
        self._resource_class = resource_class

    @property
    def resource_class(self):
        """Return the class object for this collection."""
        if isinstance(self._resource_class, basestring):
            from . import base

            cls = base.ResourceMeta.class_for_name(self._resource_class)
            if not cls:
                raise Exception(
                    _('Unable to find class for resource %s.') %
                    self._resource_class
                )
            self._resource_class = cls
        return self._resource_class

    def coerce(self, instance, value):
        if isinstance(value, self.resource_class):
            return value
        try:
            # XXX find correct manager and then create object
            return str(value)
        except ValueError:
            pass

        raise TypeError(
            _('%(value)s is not (%(type)s) or a uuid string') %
            {'value': value, 'type': self.resource_type}
        )


class Resource(ResourceAttributeBase):
    @property
    def api_name(self):
        if not self.name.endswith('_id'):
            return self.name + '_id'

    def __get__(self, instance, owner):
        retval = super(Resource, self).__get__(instance, owner)
        if isinstance(retval, basestring):
            # XXX unlazy load
            pass
        return retval


class Collection(ResourceAttributeBase):
    def __get__(self, instance, owner):
        return instance.__dict__.setdefault(
            self.name,
            CollectionManager(self, instance)
        )

    def coerce(self, instance, value):
        return CollectionManager(self, instance, value)


class CollectionManager(list):
    def __init__(self, parent_attribute, parent_instance, sequence=None):
        self.parent_attribute = parent_attribute
        self.parent_instance = parent_instance
        super(CollectionManager, self).__init__()

        if sequence:
            self.extend(sequence)

    def _validate(self, value):
        if not isinstance(value, self.parent_attribute.resource_class):
            raise TypeError(
                _('%(value)s is not of the expected type: %(type)s') %
                {'value': value, 'type': self.parent_attribute.resource_class}
            )
        elif not value._valid:
            raise ValueError(_('%s is not valid') % value)

        return value

    def _mark_dirty(self):
        self.parent_instance.__unsaved__.add(self.parent_attribute.name)

    def append(self, obj):
        list.append(self, self._validate(obj))
        self._mark_dirty()

    def extend(self, obj):
        validated = [self._validate(v) for v in obj]
        list.extend(self, validated)
        self._mark_dirty()

    def insert(self, index, obj):
        list.insert(self, index, self._validate(obj))
        self._mark_dirty()

    def pop(self, *args):
        list.pop(self, *args)
        self._mark_dirty()

    def remove(self, value):
        list.remove(self, value)
        self._mark_dirty()

    def __delitem__(self, key):
        list.__delitem__(self, key)
        self._mark_dirty()

    def __setitem__(self, key, value):
        list.__setitem__(self, key, self._validate(value))
        self._mark_dirty()


class IPAddressList(object):
    def __set__(self, instance, value):
        if self.modify == READONLY:
            raise AttributeError(_('This attribute is read-only'))

        if not self.blank and not value:
            raise ValueError(_('Value cannot be set to None'))

        if hasattr(self, 'coerce'):
            value = self.coerce(value)

        if value is not None and hasattr(self, 'validator'):
            self.validator(value)

        if instance._is_bound and self.modify == AT_UPDATE:
            raise AttributeError(
                _('%s attribute is read-only after resource creation')
                % self.name
            )

        instance.__dict__[self.name] = value
        instance.__unsaved__.add(self.name)
