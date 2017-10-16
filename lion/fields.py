from copy import copy, deepcopy

from .conditions import no_condition


class Field(object):

    def __init__(self, source=None, getter=None, condition=no_condition):
        self.name = None
        self.source = source
        if getter:
            self.getter = getter
        self.condition = condition

    def bind(self, fields):
        # Most fields don't need anything special when being bound so
        # they simply return theirselves.
        return self

    def getter(self, obj, name):
        if name is None:
            print(self)
        return getattr(obj, name)

    def dump(self, obj, target):
        value = self.getter(obj, self.source)
        if self.condition(value):
            value = self.denormalize_value(value)
            target[self.name] = value
        return value

    def denormalize_value(self, value):
        return value

    def contribute_to_mapper(self, mapper, name):
        clone = deepcopy(self)
        clone.name = name
        clone.source = clone.source or name
        mapper.fields.append(clone)


class StrField(Field):

    def denormalize_value(self, value):
        if value is None:
            return None
        return str(value)


class UUIDField(StrField):
    pass

class IntField(Field):

    def denormalize_value(self, value):
        if value is None:
            return None
        return int(value)


class ConstField(Field):

    def __init__(self, value):
        super().__init__(getter=lambda obj, name: value)


class DateTimeField(Field):

    def denormalize_value(self, value):
        if value is None:
            return None
        return value.isoformat()


class ListField(Field):

    def __init__(self, mapper, **kwargs):
        super().__init__(**kwargs)
        self.mapper_class = mapper
        self.mapper = None
        self.kwargs = kwargs

    def bind(self, fields):
        clone = copy(self)
        clone.mapper = clone.mapper_class(fields)
        return clone

    def denormalize_value(self, value):
        if value is None:
            return None
        mapper = self.mapper
        return [
            mapper.dump(x)
            for x in value
        ]


class MapperField(Field):

    def __init__(self, mapper, **kwargs):
        super().__init__(**kwargs)
        self.mapper_class = mapper
        self.mapper = None

    def bind(self, fields):
        clone = copy(self)
        clone.mapper = clone.mapper_class(fields)
        return clone

    def denormalize_value(self, value):
         if value is None:
             return None
         return self.mapper.dump(value)