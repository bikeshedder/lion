from copy import copy

from .predicates import everything as predicate_everything


class Field(object):

    def __init__(self, source=None, getter=None, predicate=predicate_everything):
        self.name = None
        self.source = source
        if getter:
            self.getter = getter
        self.predicate = predicate

    def bind(self, fields):
        # Most fields don't need anything special when being bound so
        # they simply return theirselves.
        return self

    def getter(self, obj, name):
        if name is None:
            print(self)
        return getattr(obj, name)

    def denormalize(self, obj, target):
        value = self.getter(obj, self.source)
        if self.predicate(value):
            value = self.denormalize_value(value)
            target[self.name] = value
        return value

    def contribute_to_mapper(self, mapper, name):
        clone = copy(self)
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


class BoundListField(Field):

    def __init__(self, mapper, **kwargs):
        super().__init__(**kwargs)
        self.mapper = mapper

    def denormalize_value(self, value):
        if value is None:
            return None
        mapper = self.mapper
        return [
            mapper.denormalize(x)
            for x in value
        ]


class ListField(Field):

    def __init__(self, mapper, **kwargs):
        super().__init__(**kwargs)
        self.mapper_class = mapper
        self.kwargs = kwargs

    def bind(self, fields):
        bound_field = BoundListField(self.mapper_class(fields), **self.kwargs)
        bound_field.name = self.name
        bound_field.source = self.source
        return bound_field


class BoundMapperField(Field):

    def __init__(self, mapper, **kwargs):
        super().__init__(**kwargs)
        self.mapper = mapper

    def denormalize_value(self, value):
        if value is None:
            return None
        return self.mapper.denormalize(value)


class MapperField(Field):

    def __init__(self, mapper, **kwargs):
        super().__init__(**kwargs)
        self.mapper_class = mapper
        self.kwargs = kwargs

    def bind(self, fields):
        bound_field = BoundMapperField(self.mapper_class(fields), **self.kwargs)
        bound_field.name = self.name
        bound_field.source = self.source
        return bound_field
