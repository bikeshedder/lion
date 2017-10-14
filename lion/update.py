def update_object(obj, data, fields):
    '''
    Update an object by using the values from `data` limited by
    the fields in `fields`. Returns `True` if the object was modified.
    '''
    modified = False
    for field in fields:
        if field in data:
            # FIXME smart conversion of data types
            value = data[field]
            if getattr(obj, field) != value:
                setattr(obj, field, data[field])
                modified = True
    return modified