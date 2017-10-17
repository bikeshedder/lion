def no_condition(value):
    return True

def skip_none(value):
    return value is not None

def skip_empty(value):
    return value is not None and len(value) > 0

def skip_false(value):
    return bool(value)
