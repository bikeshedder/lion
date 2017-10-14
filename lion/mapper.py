import collections

from . import ql
from .fields import MapperField

class FieldList(object):

    @classmethod
    def parse(cls, fields=None):
        return parse(fields)


class MapperMetaclass(type):

    @classmethod
    def __prepare__(metacls, name, bases, **kwds):
        return collections.OrderedDict()

    def __new__(cls, name, bases, namespace, **kwds):
        result = type.__new__(cls, name, bases, dict(namespace))
        result.fields = []
        # Copy fields from bases
        for base in bases:
            if hasattr(base, 'fields'):
                for field in base.fields:
                    field.contribute_to_mapper(result, field.name)
        for field_name, field in namespace.items():
            if hasattr(field, 'contribute_to_mapper'):
                field.contribute_to_mapper(result, field_name)
        return result


class Mapper(object, metaclass=MapperMetaclass):

    def __init__(self, fields=ql.every_dict):
        if isinstance(fields, str):
            fields = ql.parse(fields)
        self.fields = [
            field.bind(fields[field.name])
            for field in self.fields
            if field.name in fields
        ]

    def denormalize(self, obj, target=None):
        if target is None:
            target = {}
        for field in self.fields:
            field.denormalize(obj, target)
        return target