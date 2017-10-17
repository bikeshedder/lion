import datetime
from uuid import UUID

import pytz

import lion

from . import objectify


def test_bool_field():
    class MyMapper(lion.Mapper):
        a = lion.BoolField()
        b = lion.BoolField()
        c = lion.BoolField()
        d = lion.BoolField()
    data = { 'a': True, 'b': False, 'c': 'truthy value', 'd': '' }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'a': True,
        'b': False,
        'c': True,
        'd': False
    }


def test_int_field():
    class MyMapper(lion.Mapper):
        v = lion.IntField()
    data = { 'v': 42 }
    obj = objectify(data)
    assert MyMapper().dump(obj) == data


def test_str_field():
    class MyMapper(lion.Mapper):
        s = lion.StrField()
    data = { 's': 'hello world' }
    obj = objectify(data)
    assert MyMapper().dump(obj) == data


def test_const_field():
    class MyMapper(lion.Mapper):
        a = lion.ConstField('hello world')
        b = lion.ConstField(42)
    data = { 'a': 'something else', 'b': 43 }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'a': 'hello world',
        'b': 42,
    }


def test_uuid_field():
    class MyMapper(lion.Mapper):
        id = lion.UUIDField()
    data = { 'id': UUID('23101702-056b-40a3-aec2-8c10942c176d') }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'id': '23101702-056b-40a3-aec2-8c10942c176d'
    }


def test_mapper_method_field():
    class MyMapper(lion.Mapper):
        squared = lion.MapperMethodField()
        def get_squared(self, obj):
            return obj.x ** 2
    data = {'x': 8}
    obj = objectify(data)
    assert MyMapper().dump(obj) == {'squared': 64}


def test_list_field():
    class MyMapper(lion.Mapper):
        l = lion.ListField(lion.IntField)
    data = {'l': [42, 43, 44]}
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'l': [42, 43, 44]
    }


def test_list_mapper_field():
    class SthMapper(lion.Mapper):
        title = lion.StrField()
    class MyMapper(lion.Mapper):
        l = lion.ListField(SthMapper)
    data = {'l': [{'title': 'foo'}, {'title': 'bar'}]}
    obj = objectify(data)
    assert MyMapper().dump(obj) == data


def test_mapper_field():
    class SthMapper(lion.Mapper):
        title = lion.StrField()
    class MyMapper(lion.Mapper):
        sth = lion.MapperField(SthMapper)
    data = {'sth': {'title': 'foo'}}
    obj = objectify(data)
    assert MyMapper().dump(obj) == data

