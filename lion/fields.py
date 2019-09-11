from copy import copy, deepcopy

from .conditions import no_condition
from .mapper import LazyMapper


class BaseField(object):

    def dump(self, obj, target):
        raise NotImplemented("Subclasses of BaseField need to implement this method.")

    def bind(self, mapper):
        # Most fields don't need anything special when being bound so
        # they simply return theirselves.
        return self


class Field(BaseField):

    def __init__(self, source=None, getter=None, condition=no_condition):
        self.name = None
        self.source = source
        if getter:
            self.getter = getter
        self.condition = condition

    def getter(self, obj, name):
        return getattr(obj, name)

    def dump(self, obj, target):
        value = self.getter(obj, self.source)
        if self.condition(obj, value):
            value = self.denormalize_value(value)
            target[self.name] = value

    def denormalize_value(self, value):
        return value

    def contribute_to_mapper(self, mapper, name):
        clone = deepcopy(self)
        clone.name = name
        clone.source = clone.source or name
        mapper.fields.append(clone)
        return clone


class BoolField(Field):

    def denormalize_value(self, value):
        if value is None:
            return None
        return bool(value)


class IntField(Field):

    def denormalize_value(self, value):
        if value is None:
            return None
        return int(value)


class FloatField(Field):

    def denormalize_value(self, value):
        if value is None:
            return None
        return float(value)


class StrField(Field):

    def denormalize_value(self, value):
        if value is None:
            return None
        return str(value)


class ConstField(BaseField):

    def __init__(self, value):
        self.value = value

    def dump(self, obj, target):
        target[self.name] = self.value

    def contribute_to_mapper(self, mapper, name):
        clone = deepcopy(self)
        clone.name = name
        mapper.fields.append(clone)
        return clone


class UUIDField(StrField):
    pass


class DateTimeField(Field):

    def __init__(self, source=None, getter=None, condition=no_condition, tz=None):
        super().__init__(source, getter, condition)
        self.tz = tz

    def denormalize_value(self, value):
        if value is None:
            return None
        if self.tz is not None:
            if value.tzinfo is not None:
                value = value.astimezone(self.tz)
            else:
                value = self.tz.localize(value)
        return value.isoformat()


class MapperMethodField(BaseField):

    def __init__(self, method_name=None, condition=no_condition):
        self.name = None
        self.method_name = method_name
        self.condition = condition
        self.mapper = None

    def bind(self, mapper):
        clone = copy(self)
        clone.mapper = mapper
        return clone

    def dump(self, obj, target):
        method = getattr(self.mapper, self.method_name)
        value = method(obj)
        if self.condition(obj, value):
            target[self.name] = value

    def contribute_to_mapper(self, mapper, name):
        clone = deepcopy(self)
        clone.mapper = mapper
        clone.name = name
        clone.method_name = self.method_name or 'get_' + name
        mapper.fields.append(clone)
        return clone


class MapperField(Field):

    def __init__(self, mapper, **kwargs):
        super().__init__(**kwargs)
        self.mapper_class = mapper
        self.mapper = None
        self.lazy = False

    def bind(self, mapper):
        clone = copy(self)
        if self.lazy:
            # FIXME This should not be needed:
            # If fields is the `every_dict` there is no need to bind the
            # mapper and otherwise cycles are impossible.
            clone.mapper = LazyMapper(clone.mapper_class, mapper.include_fields[self.name])
        else:
            clone.mapper = clone.mapper_class(mapper.include_fields[self.name])
        return clone

    def denormalize_value(self, value):
         if value is None:
             return None
         return self.mapper.dump(value)

    def contribute_to_mapper(self, mapper, name):
        clone = super().contribute_to_mapper(mapper, name)
        if clone.mapper_class == 'self':
            clone.mapper_class = mapper
            clone.lazy = True
        return clone


class ListField(MapperField):

    def denormalize_value(self, value):
        if value is None:
            return None
        mapper = self.mapper
        if isinstance(mapper, BaseField):
            return [
                mapper.denormalize_value(x)
                for x in value
            ]
        else:
            return [
                mapper.dump(x)
                for x in value
            ]
