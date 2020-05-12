# Lion

Lion is a very flexible yet fast library for mapping objects to
dictionaries. It uses a declarative API and supports a query language
similar to GraphQL. Unlike other serialization libraries it also
allows to skip entire fields instead of having a ``null`` value
in the dictionary.

It is inspired by libraries like [serpy][serpy], [marshmallow][marshmallow],
[Django REST Framework][drf] and [Kim][kim].

## Example

```python
import lion

class UserMapper(lion.Mapper):
    id = lion.UUIDField()
    email = lion.StrField(condition=lion.skip_empty)
    first_name = lion.StrField()
    last_name = lion.StrField()

user = User(
    id=UUID('ad94d0e8-2526-4d9b-ad76-0fbffcf41033'),
    email='john.doe@example.com',
    first_name='John',
    last_name='Doe'
)

# Dump all fields to a dictionary
assert UserMapper().dump(user) == {
    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',
    'email': 'john.doe@example.com',
    'first_name': 'John',
    'last_name': 'Doe'
}

# Dump a subset of fields
assert UserMapper('{id,email}').dump(user) == {
    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',
    'email': 'john.doe@example.com'
}
```

## Subfields

The query language also supports subfields:

```python
UserMapper('{id,email,groups{id,name}}').dump(user)
```

## Performance

The performance is somewhat slower than serpy_ but still far ahead of
marshmallow_ and `Django REST Framework`_

Right now only ``dumping`` (aka. serialization, marshalling) is supported
but future versions will also introduce ``loading`` (aka. deserialization,
unmarshalling) of data.

[serpy]: https://pypi.python.org/pypi/serpy
[marshmallow]: https://pypi.python.org/pypi/marshmallow/
[kim]: https://pypi.python.org/pypi/py-kim/1.2.0
[drf]: https://pypi.python.org/pypi/djangorestframework