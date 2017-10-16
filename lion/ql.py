from pyparsing import alphas, alphanums, delimitedList, Dict, Forward, \
        Group, Literal, Optional, Suppress, Word

bracket_open = Suppress(Literal('{'))
bracket_close = Suppress(Literal('}'))
identifier = Word(alphas, alphanums + "_" ).setName("identifier")
field = Forward()
fields = delimitedList(field)
obj = Dict(bracket_open + fields + bracket_close)
field << Group(identifier + Optional(obj, default=None))

ql = obj

class EveryDict(object):

    def __contains__(self, name):
        return True

    def __getitem__(self, name):
        return self

every_dict = EveryDict()

def to_dict(d):
    return {
        k: to_dict(v) if v != None else every_dict
        for k, v in d.items()
    }

def parse(s):
    if not s:
        return every_dict
    return to_dict(ql.parseString(s))