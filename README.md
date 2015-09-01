# More Collections

This package provides some more collections than the standard collections package.

The package currently provides:

* **puredict**/**frozendict** - a functionally **pure** and **immutable dictionary** that is even **hashable**,
if all keys and values are hashable.

The package will provide in the near future

* **multiset** - a multiset implementation
* **orderable_multiset** - a multiset implementation for orderable carriers so that
multisets of those elements themselves are orderable
* **eq_dict**/**eq_ordered_dict** - dictionary implementations where the keys do not need to be hashable (linear time). If the values admit a total ordering, **eq_ordered_dict** operates in logarithmic time.
* **bijection** - a one-to-one mapping
