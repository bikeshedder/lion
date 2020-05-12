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

class GroupMapper(lion.Mapper):
    id = lion.UUIDField()
    name = lion.StrField()

class UserMapper(lion.Mapper):
    id = lion.UUIDField()
    email = lion.StrField(condition=lion.skip_empty)
    first_name = lion.StrField()
    last_name = lion.StrField()
    groups = lion.ListField(GroupMapper)

user = User(
    id=UUID('ad94d0e8-2526-4d9b-ad76-0fbffcf41033'),
    email='john.doe@example.com',
    first_name='John',
    last_name='Doe',
    groups=[
        Group(
            id=UUID('95a326fc-32e5-4d9b-a385-1ea1257d98da'),
            name='Awesome people'
        )
    ]
)

# Dump all fields to a dictionary
assert UserMapper().dump(user) == {
    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',
    'email': 'john.doe@example.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'groups': [
        {
            'id': '95a326fc-32e5-4d9b-a385-1ea1257d98da',
            'name': 'Awesome people'
        }
    ]
}

# Load user object from a dictionary
assert user == UserMapper().load({
    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',
    'email': 'john.doe@example.com',
    'first_name': 'John',
    'last_name': 'Doe',
    'groups': [
        {
            'id': '95a326fc-32e5-4d9b-a385-1ea1257d98da',
            'name': 'Awesome people'
        }
    ]
})
```

## Query language

By using the GraphQL-like query language it is possible
to dump and load only parts of a given structure:

```python
# Dump a subset of fields
assert UserMapper('{id,email}').dump(user) == {
    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',
    'email': 'john.doe@example.com'
}

# Dump subset of a nested mapper
assert UserMapper('{id,email,groups{id}}').dump(user) == {
    'id': 'ad94d0e8-2526-4d9b-ad76-0fbffcf41033',
    'email': 'john.doe@example.com',
    'groups': [
        'id': '95a326fc-32e5-4d9b-a385-1ea1257d98da'
    ]
}
```

## Performance

The performance is somewhat slower than [serpy][serpy] but still far ahead of [marshmallow][marshmallow] and [Django REST Framework][drf].

![Simple Benchmark](https://raw.githubusercontent.com/bikeshedder/lion/master/docs/benchmark-chart-simple.svg)

![Complex Benchmark](https://raw.githubusercontent.com/bikeshedder/lion/master/docs/benchmark-chart-complex.svg)

## Caveats

Lion also supports loading (serialization/marshalling) of data but currently does not perform any kind of validation. This is not a big deal if using Lion as part of a project which uses something like [connexion][connexion] which already performs validation using the provided OpenAPI specification file. Just be warned that loading an unvalidated data structure using Lion might result in somewhat weird looking data.


[serpy]: https://pypi.python.org/pypi/serpy
[marshmallow]: https://pypi.python.org/pypi/marshmallow/
[kim]: https://pypi.python.org/pypi/py-kim
[drf]: https://pypi.python.org/pypi/djangorestframework
[connexion]: https://pypi.org/project/connexion/
