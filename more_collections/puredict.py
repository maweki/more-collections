try: # Python 2.7 compat
    from collections.abc import Mapping, Iterable
except ImportError:
    from collections import Mapping, Iterable
from itertools import chain
from functools import reduce
from .common import _raise

def empty(_ = None):
    class __puredict(puredict_base):
        __len__ = lambda _: 0
        __getitem__ = lambda _, __: _raise(KeyError())
        __contains__ = lambda _, __: False
        __iter__ = lambda _: iter(())
        items = lambda _: iter(())
    return __puredict()

def insert(parent, key, value):
    class __puredict(puredict_base):
        __len__ = lambda _: len(parent) + (0 if (key in parent) else 1)
        __getitem__ = lambda _, _key: value if (key == _key) else parent[_key]
        __contains__ = lambda _, _key: (key == _key) or (_key in parent)
        __iter__ = lambda _: chain((key,), (k for k in parent if not key == k))
        items = lambda _: chain(((key, value),), ((k, v) for (k, v) in parent.items() if not key == k))
    return __puredict()

def delete(parent, key):
    class __puredict(puredict_base):
        __len__ = lambda _: len(parent) - (1 if (key in parent) else 0)
        __getitem__ = lambda _, _key: _raise(KeyError()) if (key == _key) else parent[_key]
        __contains__ = lambda _, _key: (not key == _key) and (_key in parent)
        __iter__ = lambda _: (_key for _key in parent if not key == _key)
        items = lambda _: ((k, v) for (k, v) in parent.items() if not key == k)
    return __puredict()

class puredict_base(Mapping):
    empty = empty
    insert = insert
    delete = delete
    __hash__ = lambda self: hash(frozenset(self.items())) ^ hash(puredict_base)
    __repr__  = lambda self: repr(dict(self))

class puredict(puredict_base):
    from_iterable = lambda it: reduce(lambda x, y: insert(x, *y), it, empty())
    from_mapping = lambda mapping: puredict.from_iterable(mapping.items())
    __new__ = lambda cls, param=None: next((func(param) for (typeof, func) in (
                (type(None), empty),
                (Mapping, cls.from_mapping),
                (Iterable, cls.from_iterable),
                (object, lambda _: _raise(ValueError()))
            ) if isinstance(param, typeof)))
