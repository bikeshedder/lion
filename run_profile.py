#!/usr/bin/env -S python

import cProfile

import lion

class Foo(object):
    def __init__(self, name, value, bars):
        self.name = name
        self.value = value
        self.bars = bars

class Bar(object):
    def __init__(self, name, x, y, z):
        self.name = name
        self.x = x
        self.y = y
        self.z = z

class Root(object):
    def __init__(self, foos):
        self.foos = foos


class BarMapper(lion.Mapper):
    name = lion.StrField()
    x = lion.IntField()
    y = lion.FloatField()
    z = lion.Field(condition=lion.skip_none)

class FooMapper(lion.Mapper):
    name = lion.StrField()
    value = lion.IntField()
    bars = lion.ListField(BarMapper)

class RootMapper(lion.Mapper):
    foos = lion.ListField(FooMapper)

root = Root(foos=[
    Foo(
        name=f'Foo #{i}',
        value=i,
        bars=[
            Bar(
                name=f'Bar #{i}:{j}',
                x=i*j,
                y=float(i)/float(j+1),
                z=None
            )
            for j in range(50)
        ]
    )
    for i in range(1000)
])

if __name__ == '__main__':
    mapper = RootMapper()
    cProfile.run('mapper.dump(root)')
