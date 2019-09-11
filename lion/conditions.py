def no_condition(obj, value):
    return True

def skip_none(obj, value):
    return value is not None

def skip_empty(obj, value):
    return value is not None and len(value) > 0

def skip_false(obj, value):
    return bool(value)
