try: # Python 2.7 compat
    from collections.abc import Set, MutableSet, Hashable, Iterable
except ImportError:
    from collections import Set, MutableSet, Hashable, Iterable
from collections import defaultdict
from functools import reduce
from itertools import chain
import operator
try: # Python compat < 3.4
    from functools import partialmethod
except ImportError:
    from common import partialmethod

class _base_multiset(Set):

    def __init__(self, items=None):
        self.__bag = {}
        if isinstance(items, Iterable):
            for i in items:
                self.__bag[i] = self.__bag.get(i, 0) + 1

    def __contains__(self, item):
        return self.__bag.get(item, 0) > 0

    def __len__(self):
        return sum(self.__bag.values())

    def __iter__(self):
        for item in self.__bag:
            for _ in range(self.__bag[item]):
                yield item

    def __le__(self, other):
        if not isinstance(other, _base_multiset):
            raise NotImplementedError()
        return all((self.count(i) <= other.count(i)) for i in self.__bag)

    def __eq__(self, other):
        if not isinstance(other, _base_multiset):
            raise NotImplementedError()
        return all((self.count(i) == other.count(i)) for i in chain(self.__bag, other.__bag))

    def __lt__(self, other):
        return (self <= other) and not (self == other)

    def __gt__(self, other):
        if not isinstance(other, _base_multiset):
            raise NotImplementedError()
        return other < self

    def __ge__(self, other):
        if not isinstance(other, _base_multiset):
            raise NotImplementedError()
        return other <= self

    def __combine(self, amnt_op, this_op, other):
        if isinstance(other, _base_multiset):
            result = self.__class__()
            for element in self.__bag:
                amount = amnt_op(self.count(element), other.count(element))
                if amount > 0:
                    result.__bag[element] = amount
            return result

        if isinstance(other, Iterable):
            return this_op(self, self.__class__(other))

        raise NotImplementedError()

    __sub__ = partialmethod(__combine, operator.sub, (lambda l, r: l - r))

    def count(self, item):
        return self.__bag.get(item, 0)

class _hashing_mixin(Hashable):
    def __hash__(self):
        from operator import xor
        pots = (hash(key)**value for (key, value) in self.__bag.items())
        return reduce(xor, pots)

class _orderable_mixin(object):
    pass

class multiset(_base_multiset, MutableSet):
    def add(self, item):
        self.__bag[item] = self.__bag.get(item, 0) + 1

    def discard(self, item):
        if item in self.__bag:
            self.__bag[item] = self.__bag[item] - 1
            if self.__bag[item] == 0:
                del self.__bag[item]

class frozenmultiset(_base_multiset, _hashing_mixin):
    pass

class orderable_multiset(multiset, _orderable_mixin):
    pass

class orderable_frozenmultiset(frozenmultiset, _orderable_mixin):
    pass
