from .ql import parse, every_dict

class FieldList(object):

    @classmethod
    def parse(cls, fields=None):
        return parse(fields)


class Mapper(object):

    def __init__(self, *fields):
        self.fields = []
        for field in fields:
            if callable(field):
                self.fields.append(field)
            else:
                self.fields.append(raw_field(field))

    def __call__(self, obj, d=None, fields=every_dict):
        if d is None:
            d = {}
        for field in self.fields:
            field(obj, d, fields)
        return d

    def as_field(self, name, getter=getattr, skip_cond=None):
        if skip_cond:
            def f(obj, d, fields):
                if name in fields and not skip_cond(obj):
                    v = getter(obj, name)
                    d[name] = self(v, fields=fields[name])
        else:
            def f(obj, d, fields):
                if name in fields:
                    v = getter(obj, name)
                    d[name] = self(v, fields=fields[name])
        f.name = name
        return f