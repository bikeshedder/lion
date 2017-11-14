import collections

from . import ql


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
        self.include_fields = fields
        self.fields = [
            field.bind(self)
            for field in self.fields
            if field.name in fields
        ]

    def dump(self, obj, target=None):
        if target is None:
            target = {}
        for field in self.fields:
            field.dump(obj, target)
        return target

    def drf(self):
        '''
        Return a mapper that is compatible to the Django REST Framework
        serializer API.
        '''
        from lion.contrib.drf import DRFMapper
        return DRFMapper.wrap(self)


class LazyMapper:

    def __init__(self, mapper_class, fields):
        self.mapper_class = mapper_class
        self.fields = fields
        self.mapper = None

    def dump(self, *args, **kwargs):
        if self.mapper is None:
            self.mapper = self.mapper_class(self.fields)
        return self.mapper.dump(*args, **kwargs)
