def everything(value):
    return True

def nothing(value):
    return False

def skip_none(value):
    return value is not None

def skip_empty(value):
    return len(value) > 0

def skip_false(value):
    return bool(value)