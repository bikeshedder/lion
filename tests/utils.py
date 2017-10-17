class Obj(object):
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)

def objectify(value):
    if isinstance(value, dict):
        return Obj(**{k: objectify(v) for k, v in value.items()})
    if isinstance(value, list):
        return [objectify(entry) for entry in value]
    return value
