from functools import partial

class DRFMapper(object):
    '''
    Wrapper class to support the Serializer API of the Django REST Framework.
    Call `wrap(mapper)` or `mapper.drf()` to get a useable instance of this.
    '''

    def __init__(self, obj, many=False):
        self.obj = obj
        self.many = many

    @classmethod
    def wrap(cls, mapper):
        class BoundDRFMapper(DRFMapper):
            pass
        BoundDRFMapper.mapper = mapper
        return BoundDRFMapper

    @property
    def data(self):
        if self.many:
            return [self.mapper.dump(x) for x in self.obj]
        else:
            return self.mapper.dump(self.obj)
