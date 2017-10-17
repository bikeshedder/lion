def call_method(obj, name):
    return getattr(obj, name)()

def call_mapper_method(obj, name):
    # FIXME this is currently impossible
    raise RuntimeError('FSCK!')
