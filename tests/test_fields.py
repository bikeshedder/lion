import datetime
from uuid import UUID

import pytz

import lion

from .utils import objectify


def test_bool_field():
    class MyMapper(lion.Mapper):
        v = lion.BoolField()
        v_skip_none = lion.BoolField(condition=lion.skip_none)
        v_skip_false = lion.BoolField(condition=lion.skip_false)
        v_skip_true = lion.BoolField(condition=lambda v: v is not None and not v)
        v_boolify_true = lion.BoolField()
        v_boolify_false = lion.BoolField()
    data = {
        'v': True,
        'v_skip_none': None,
        'v_skip_false': False,
        'v_skip_true': True,
        'v_boolify_true': 'Hi everybody!',
        'v_boolify_false': '',
    }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'v': True,
        'v_boolify_true': True,
        'v_boolify_false': False,
    }


def test_int_field():
    class MyMapper(lion.Mapper):
        v = lion.IntField()
        v_skip_none = lion.IntField(condition=lion.skip_none)
        v_skip_false = lion.IntField(condition=lion.skip_false)
        v_skip_negative = lion.IntField(condition=lambda v: v is not None and v >= 0)
        v_intify = lion.IntField()
    data = {
        'v': 42,
        'v_skip_none': None,
        'v_skip_false': 0,
        'v_skip_negative': -42,
        'v_intify': '42',
    }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'v': 42,
        'v_intify': 42,
    }


def test_float_field():
    class MyMapper(lion.Mapper):
        v = lion.FloatField()
        v_skip_none = lion.FloatField(condition=lion.skip_none)
        v_skip_false = lion.FloatField(condition=lion.skip_false)
        v_skip_negative = lion.FloatField(condition=lambda v: v is not None and v >= 0)
        v_intify = lion.FloatField()
    data = {
        'v': 4.2,
        'v_skip_none': None,
        'v_skip_false': 0.0,
        'v_skip_negative': -4.2,
        'v_intify': '4.2',
    }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'v': 4.2,
        'v_intify': 4.2,
    }


def test_str_field():
    class MyMapper(lion.Mapper):
        s = lion.StrField()
        s_none = lion.StrField()
        s_skip_none = lion.StrField(condition=lion.skip_none)
        s_skip_empty = lion.StrField(condition=lion.skip_empty)
        stringify = lion.StrField()
    data = {
        's': 'hello world',
        's_none': None,
        's_skip_none': None,
        's_skip_empty': '',
        'stringify': 42,
    }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        's': 'hello world',
        's_none': None,
        'stringify': '42',
    }


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
        id_skip_none = lion.UUIDField(condition=lion.skip_none)
    data = {
        'id': UUID('23101702-056b-40a3-aec2-8c10942c176d'),
        'id_skip_none': None
    }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'id': '23101702-056b-40a3-aec2-8c10942c176d'
    }


def test_datetime_field():
    class MyMapper(lion.Mapper):
        dt_naive = lion.DateTimeField()
        dt_berlin = lion.DateTimeField()
        dt_naive_to_utc = lion.DateTimeField(tz=pytz.utc)
        dt_berlin_to_utc = lion.DateTimeField(tz=pytz.utc)
        dt_utc_to_berlin = lion.DateTimeField(tz=pytz.timezone('Europe/Berlin'))
        dt_skip_none = lion.DateTimeField(condition=lion.skip_none)
    data = {
        'dt_naive': datetime.datetime(2017, 10, 17, 15, 45, 3, tzinfo=pytz.utc),
        'dt_berlin': pytz.timezone('Europe/Berlin').localize(datetime.datetime(2017, 10, 17, 15, 45, 3)),
        'dt_naive_to_utc': datetime.datetime(2017, 10, 17, 15, 45, 3),
        'dt_berlin_to_utc': pytz.timezone('Europe/Berlin').localize(datetime.datetime(2017, 10, 17, 15, 45, 3)),
        'dt_utc_to_berlin': datetime.datetime(2017, 10, 17, 15, 45, 3, tzinfo=pytz.utc),
        'dt_skip_none': None,
    }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'dt_naive': '2017-10-17T15:45:03+00:00',
        'dt_berlin': '2017-10-17T15:45:03+02:00',
        'dt_naive_to_utc': '2017-10-17T15:45:03+00:00',
        'dt_berlin_to_utc': '2017-10-17T13:45:03+00:00',
        'dt_utc_to_berlin': '2017-10-17T17:45:03+02:00',
    }


def test_mapper_method_field():
    class MyMapper(lion.Mapper):
        squared = lion.MapperMethodField()
        def get_squared(self, obj):
            return obj.x ** 2
    data = {
        'x': 8
    }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'squared': 64
    }


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
        l_empty = lion.ListField(SthMapper)
        l_skip_none = lion.ListField(SthMapper, condition=lion.skip_none)
        l_skip_empty = lion.ListField(SthMapper, condition=lion.skip_empty)
    data = {
        'l': [
            {'title': 'foo'},
            {'title': 'bar'}
        ],
        'l_empty': [],
        'l_skip_none': None,
        'l_skip_empty': [],
    }
    obj = objectify(data)
    assert MyMapper().dump(obj) == {
        'l': [
            {'title': 'foo'},
            {'title': 'bar'}
        ],
        'l_empty': [],
    }


def test_mapper_field():
    class SthMapper(lion.Mapper):
        title = lion.StrField()
    class MyMapper(lion.Mapper):
        sth = lion.MapperField(SthMapper)
    data = {'sth': {'title': 'foo'}}
    obj = objectify(data)
    assert MyMapper().dump(obj) == data

