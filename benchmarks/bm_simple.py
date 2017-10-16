from django.conf import settings
settings.configure()

import django
django.setup()

from rest_framework import serializers as rf_serializers
from utils import write_csv
import marshmallow
import serpy
import lion


class SimpleRF(rf_serializers.Serializer):
    foo = rf_serializers.ReadOnlyField()


class SimpleM(marshmallow.Schema):
    foo = marshmallow.fields.Str()


class SimpleS(serpy.Serializer):
    foo = serpy.Field()


class SimpleL(lion.Mapper):
    foo = lion.Field()


if __name__ == '__main__':
    data = {'foo': 'bar'}
    write_csv(__file__, data, SimpleRF, SimpleM().dump, SimpleS, SimpleL().drf(), 100)
