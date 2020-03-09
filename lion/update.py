from collections import namedtuple

Change = namedtuple('Change', ['old', 'new'])


def update_object(obj, data, fields):
    '''
    Update an object by using the values from `data` limited by
    the fields in `fields`. Returns a dictionary of the format
    `{field_name: (old_value, new_value)}`.
    '''
    modified = {}
    for field in fields:
        if field in data:
            # FIXME smart conversion of data types
            new_value = data[field]
            old_value = getattr(obj, field)
            if old_value != new_value:
                modified[field] = Change(old_value, new_value)
                setattr(obj, field, new_value)
    return modified
