class Obj(object):

    def __init__(self, **kwargs):
        self.__keys = list(kwargs.keys())
        for k, v in kwargs.items():
            setattr(self, k, v)

    def __eq__(self, other):
        for k in self.__keys:
            if getattr(self, k) != getattr(other, k):
                return False
        return True


def objectify(value):
    if isinstance(value, dict):
        return Obj(**{k: objectify(v) for k, v in value.items()})
    if isinstance(value, list):
        return [objectify(entry) for entry in value]
    return value
