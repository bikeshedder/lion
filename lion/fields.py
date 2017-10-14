def RawField(name, skip_empty=False):
    if skip_empty:
        def f(obj, d, fields):
            if name in fields:
                v = getattr(obj, name)
                if v or not skip_empty:
                    d[name] = v
    else:
        def f(obj, d, fields):
            if name in fields:
                v = getattr(obj, name)
                d[name] = v
    f.name = name
    return f

def StrField(name, getter=getattr, skip_empty=False):
    if skip_empty:
        def f(obj, d, fields):
            if name in fields:
                v = getter(obj, name)
                if v:
                    d[name] = str(v)
    else:
        def f(obj, d, fields):
            if name in fields:
                v = getter(obj, name)
                d[name] = str(v)
    f.name = name
    return f

# XXX
UUIDField = StrField

def IntField(name, getter=getattr, skip_null=True):
    def f(obj, d, fields):
        if name in fields:
            v = getter(obj, name)
            if v is None:
                d[name] = int(v)
            elif not skip_null:
                d[name] = None
    f.name = name
    return f

def ConstField(name, value):
    def f(obj, d, fields):
        if name in fields:
            d[name] = value
    f.name = name
    return f

def DateTimeField(name, getter=getattr, skip_null=False):
    if skip_null:
        def f(obj, d, fields):
            if name in fields:
                v = getter(obj, name)
                if v is not None:
                    d[name] = v.isoformat()
    else:
        def f(obj, d, fields):
            if name in fields:
                v = getter(obj, name)
                d[name] = v.isoformat() if v is not None else None
    f.name = name
    return f

def ListField(name, mapper, getter=getattr, skip_empty=False):
    def f(obj, d, fields):
        if name in fields:
            v = getter(obj, name)
            l = [
                mapper(x, fields=fields[name]) for x in v
            ]
            if l or not skip_empty:
                d[name] = l
    f.name = name
    return f