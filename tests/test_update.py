class Person:
    def __init__(self, name):
        self.name = name

def test_update_0():
    from lion.update import update_object
    obj = Person("foo")
    assert update_object(obj, {"name": "bar"}, ['name']) == {
        "name": ("foo", "bar")
    }

def test_update_1():
    from lion.update import update_object
    obj = Person("foo")
    assert update_object(obj, {}, ['name']) == {}
