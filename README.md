# More Collections

This package provides some more collections than the standard collections package.

The package currently provides:

* **puredict**/**frozendict** - a functionally **pure** and **immutable dictionary** that is even **hashable**,
if all keys and values are hashable.
* **multiset**/**frozenmultiset** - a multiset implementation
* **orderable_multiset**/**orderable_frozenmultiset** - a multiset implementation for orderable carriers so that
multisets of those elements themselves are orderable, even including **nestable_orderable_frozenmultiset**
which is a multiset-ordering-extension that gives a total ordering for arbitrarily nested multisets over an orderable carrier.

If you want to see any more collections, contact me, open a ticket (I'll happily implement it) or send in a patch.

## Usage
### puredict

The constructors `empty()`, `insert(key, value)` and `remove(key)` create new
references to immutable dictionaries.

    from more_collections import puredict
    e = puredict.empty().insert(5, "foo")
    e = e.insert(3, "bar").remove(5)
    print(e[3])

Insert and Remove can also be called statically:
    `puredict.insert(puredict.empty(), 5, "bar")`

The basic constructor supports common dictionary constructors:

    puredict.puredict({3:6, 2:12, 4:1})
    puredict.puredict((a, a**4) for a in range(6))
    puredict.puredict(a=2, b=5)

This dictionary stores all its data within bound variables so it is properly immutable. The implementation is purely functional. The constructors need constant time while `__getitem__` and `__contains__` run in O(n) with n as the number of operations that were used to build the dictionary (not the number of items in the dictionary).

### multiset

There are 5 multiset variants in `more_collections`.

`multiset`/`frozenmultiset` work like normal `set`/`frozenset` but with elements
having a multiplicity.

    from more_collections import multiset
    list(multiset('aaabbc')) # ['b', 'b', 'c', 'a', 'a', 'a']
    multiset('aaabbc').count('a') # 3
    multiset('aaabbc').count('d') # 0
    list(multiset('aaabbc').items()) # [('b', 2), ('c', 1), ('a', 3)]

The relations `<=`, `<`, `>=` and `>` mean, as with normal sets, subset, proper subset, superset and proper superset respectively.

Additionally to the normal set operations, multisets support the `+`-operator, which means union-plus, adding the multiplicities of both multisets.

    a, b = multiset('ab'), multiset('bc')
    ''.join(a | b) # 'acb'
    ''.join(a & b) # 'b'
    ''.join(a ^ b) # 'ca'
    ''.join(a - b) # 'a'
    ''.join(a + b) # 'acbb'

`orderable_multiset`/`orderable_frozenmultiset` work like `multiset`/`frozenmultiset` but the relations `<=`, `<`, `>=` and `>` mean a well-founded total ordering if the carrier (the elements of the sets) have a total order (like strings or numbers).

    from more_collections import orderable_multiset
    a, b = orderable_multiset('abc'), orderable_multiset('bcd')
    a < b or a > b # True

`nestable_orderable_frozenmultiset` are like `orderable_frozenmultiset` but the ordering is extended to arbitrarily nested multisets.

    from more_collections import nestable_orderable_frozenmultiset as nofms
    a, b = nofms('abc'), nofms((nofms('abc'),'c'))
    a < b or a > b # True

*Note:* (proper) subset/superset imply less/greater (or equal) within the implemented total ordering.

The non-frozen multiset variants support `.add(el)` and `.discard(el)` to add and remove items.

The multisets are dictionary-backed so, like normal sets, items in the set need to be *hashable*.

## Todo

* nice documentation
