from django.conf import settings
settings.configure()

import django
django.setup()

from rest_framework import serializers as rf_serializers
from utils import write_csv
import marshmallow
import serpy
import lion


class SubRF(rf_serializers.Serializer):
    w = rf_serializers.FloatField()
    x = rf_serializers.SerializerMethodField()
    y = rf_serializers.CharField()
    z = rf_serializers.IntegerField()

    def get_x(self, obj):
        return obj.x + 10


class ComplexRF(rf_serializers.Serializer):
    foo = rf_serializers.ReadOnlyField()
    bar = rf_serializers.IntegerField()
    sub = SubRF()
    subs = SubRF(many=True)


class SubM(marshmallow.Schema):
    w = marshmallow.fields.Int()
    x = marshmallow.fields.Method('get_x')
    y = marshmallow.fields.Str()
    z = marshmallow.fields.Int()

    def get_x(self, obj):
        return obj.x + 10


class CallField(marshmallow.fields.Field):

    def _serialize(self, value, attr, obj):
        return value()


class ComplexM(marshmallow.Schema):
    foo = marshmallow.fields.Str()
    bar = CallField()
    sub = marshmallow.fields.Nested(SubM)
    subs = marshmallow.fields.Nested(SubM, many=True)


class SubS(serpy.Serializer):
    w = serpy.IntField()
    x = serpy.MethodField()
    y = serpy.StrField()
    z = serpy.IntField()

    def get_x(self, obj):
        return obj.x + 10


class ComplexS(serpy.Serializer):
    foo = serpy.StrField()
    bar = serpy.IntField(call=True)
    sub = SubS()
    subs = SubS(many=True)


class SubL(lion.Mapper):
    w = lion.IntField()
    x = lion.MapperMethodField()
    y = lion.StrField()
    z = lion.IntField()

    def get_x(self, obj):
        return obj.x + 10


class ComplexL(lion.Mapper):
    foo = lion.StrField()
    bar = lion.Field(getter=lion.getters.call_method)
    sub = lion.MapperField(SubL)
    subs = lion.ListField(SubL)


if __name__ == '__main__':
    data = {
        'foo': 'bar',
        'bar': lambda: 5,
        'sub': {
            'w': 1000,
            'x': 20,
            'y': 'hello',
            'z': 10
        },
        'subs': [{
            'w': 1000 * i,
            'x': 20 * i,
            'y': 'hello' * i,
            'z': 10 * i
        } for i in range(10)]
    }
    write_csv(__file__, data, ComplexRF, ComplexM().dump, ComplexS, ComplexL().drf(), 1)
