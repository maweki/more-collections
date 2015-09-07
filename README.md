# More Collections

This package provides some more collections than the standard collections package.

The package currently provides:

* **puredict**/**frozendict** - a functionally **pure** and **immutable dictionary** that is even **hashable**,
if all keys and values are hashable.

The package will provide in the near future

* **multiset**/**frozenmultiset** - a multiset implementation
* **orderable_multiset**/**orderable_frozenmultiset** - a multiset implementation for orderable carriers so that
multisets of those elements themselves are orderable
* **eq_dict**/**eq_ordered_dict** - dictionary implementations where the keys do not need to be hashable (linear time). If the keys admit a total ordering, **eq_ordered_dict** operates in logarithmic time.
* **bijection** - a one-to-one mapping

## Usage
### puredict

    from more_collections import puredict
    e = puredict.empty().insert(5, "foo")
    e = e.insert(3, "bar").remove(5)
    print(e[3])

Insert and Remove can also be called statically:
    `puredict.insert(puredict.empty(), 5, "bar")`

The constructor supports common dictionary constructors:

    puredict.puredict({3:6, 2:12, 4:1})
    puredict.puredict((a, a**4) for a in range(6))

## Todo

* implement missing collections
* more tests
* nice documentation
* packaging to PyPi
* version numbers
