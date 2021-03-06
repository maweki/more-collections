from unittest import TestCase
from more_collections.multisets import multiset, frozenmultiset, orderable_multiset, orderable_frozenmultiset, nestable_orderable_frozenmultiset
try: # Python compat < 3.3
    from collections.abc import Hashable, Set
except ImportError:
    from collections import Hashable, Set
from itertools import chain, repeat, product

class TestPuredict(TestCase):

    constructors_ord = (orderable_multiset, orderable_frozenmultiset)
    constructors_unord = (multiset, frozenmultiset)
    constructors_hashing = (frozenmultiset, orderable_frozenmultiset)
    constructors_mutable = (multiset, orderable_multiset)
    constructors = constructors_unord + constructors_ord
    test_depth = 10

    def test_constructors(self):
        cnt = 2**self.test_depth

        for c in self.constructors:
            ms = c()
            self.assertEqual(0, len(ms))
            self.assertTrue(isinstance(ms, Set))

            ms = c(range(cnt))
            self.assertEqual(cnt, len(ms))
            for i in range(cnt):
                self.assertEqual(1, ms.count(i))
                self.assertIn(i, ms)
            self.assertNotIn(cnt, ms)

            ms = c(chain(range(cnt),range(cnt)))
            self.assertEqual(cnt*2, len(ms))
            for i in range(cnt):
                self.assertEqual(2, ms.count(i))
                self.assertIn(i, ms)
            self.assertNotIn(cnt, ms)

    def test_iter(self):
        cnt = 2**self.test_depth

        for c in self.constructors:
            ms = c(range(cnt))
            self.assertEqual(frozenset(range(cnt)), frozenset(ms))

            ms = c(repeat(0, cnt))
            self.assertEqual(list(repeat(0, cnt)), list(ms))
            self.assertEqual(frozenset((0,)), frozenset(ms))

    def test_mutable(self):
        r = 2**self.test_depth

        for c in self.constructors_mutable:
            ms = c()
            for cnt in range(r):
                self.assertEqual(len(ms), cnt)
                ms.add(5)
                self.assertIn(5, ms)
                self.assertEqual(len(ms), cnt + 1)

            for cnt in range(r):
                self.assertIn(5, ms)
                self.assertEqual(len(ms), r - cnt)
                ms.discard(5)
                self.assertEqual(len(ms), r - cnt - 1)

    def test_hashing(self):
        for c in self.constructors_hashing:
            self.assertEqual(hash(c()), hash(c()))

            a = c((1, 1, 2))
            b = c(a)
            self.assertEqual(hash(a), hash(b))

            a = c((0, 1, 1))
            b = c((0, 1, 1))
            self.assertEqual(hash(a), hash(b))

            with self.assertRaises(AttributeError):
                c().add(5)

            with self.assertRaises(AttributeError):
                c().discard(5)

            self.assertEqual(frozenset((a,b)), frozenset((a,)))
            self.assertEqual(len(set((c(),c()))), 1)

            self.assertTrue(isinstance(c(), Hashable))

    def test_le(self):

        for c in self.constructors_unord:
            ms1 = c()
            ms2 = c('bc')
            ms3 = c('abc')
            ms = (ms1, ms2, ms3)
            self.assertTrue(ms1 <= ms2)
            self.assertTrue(ms1 <= ms3)
            self.assertTrue(ms2 <= ms3)
            for m in ms:
                self.assertTrue(m <= m)
            self.assertFalse(ms2 <= ms1)
            self.assertFalse(ms3 <= ms1)
            self.assertFalse(ms3 <= ms2)

            raises = (
                'foo', 0, frozenset(), [], {}
            )
            for m, o in product(ms, raises):
                with self.assertRaises(NotImplementedError):
                    m <= o
                with self.assertRaises(NotImplementedError):
                    o <= m

    def test_eq(self):
        cnt = 2**self.test_depth
        for c in self.constructors:
            ms1 = c(range(cnt))
            ms2 = c(range(cnt))
            ms3 = c(range(cnt*2))
            self.assertEqual(ms1, ms2)
            self.assertNotEqual(ms2, ms3)
            ms = (ms1, ms2, ms3)

            raises = (
                'foo', 0, frozenset(), [], {}
            )
            for m, o in product(ms, raises):
                with self.assertRaises(NotImplementedError):
                    m == o
                with self.assertRaises(NotImplementedError):
                    o == m

    def test_lt(self):

        for c in self.constructors_unord:
            ms1 = c()
            ms2 = c('bc')
            ms3 = c('abc')
            ms = (ms1, ms2, ms3)
            self.assertTrue(ms1 < ms2)
            self.assertTrue(ms1 < ms3)
            self.assertTrue(ms2 < ms3)
            for m in ms:
                self.assertFalse(m < m)
            self.assertFalse(ms2 < ms1)
            self.assertFalse(ms3 < ms1)
            self.assertFalse(ms3 < ms2)

            raises = (
                'foo', 0, frozenset(), [], {}
            )
            for m, o in product(ms, raises):
                with self.assertRaises(NotImplementedError):
                    m < o
                with self.assertRaises(NotImplementedError):
                    o < m

    def test_operators(self):
        for c in self.constructors:
            s1, s2, s3 = '123123', '123', '134'
            ms1 = c(s1)
            ms2 = c(s2)
            ms3 = c(s3)
            ds = [
                (ms1, s1, 0, 6, 6, 0),
                (ms1, s2, 3, 6, 3, 3),
                (ms1, s3, 4, 7, 2, 5),
                (ms2, s1, 0, 6, 3, 3),
                (ms2, s2, 0, 3, 3, 0),
                (ms2, s3, 1, 4, 2, 2),
                (ms3, s1, 1, 7, 2, 5),
                (ms3, s2, 1, 4, 2, 2),
                (ms3, s3, 0, 3, 3, 0)
            ]
            for l, _r, minus, union, intersection, disjointunion in ds:
                for r in (_r, c(_r)):
                    self.assertEqual(minus, len(l - r), (l,r))
                    self.assertIs(type(l), type(l - r))

                    plus = len(l) + len(r)
                    self.assertEqual(plus, len(l + r), (l,r))
                    self.assertIs(type(l), type(l + r))

                    self.assertEqual(union, len(l | r), (l,r))
                    self.assertIs(type(l), type(l | r))

                    self.assertEqual(intersection, len(l & r), (l,r))
                    self.assertIs(type(l), type(l & r))

                    self.assertEqual(disjointunion, len(l ^ r), (l,r))
                    self.assertIs(type(l), type(l ^ r))

                    self.assertEqual(l ^ r, (l | r) - (l & r))

    def test_ordering(self):
        from itertools import combinations, combinations_with_replacement, product
        import operator

        for c in self.constructors_ord:
            m1 = (2,)
            m2 = (1,3)
            m3 = (1,1,1,2)
            m4 = (2,)*4
            m5 = (1,2)
            ms = (m1, m2, m3, m4, m5)

            for m in ms:
                self.assertTrue(c() < c(m))
                self.assertTrue(m <= m)

            order = list(c(m) for m in (
                (),
                m1,
                m5,
                m3,
                m4,
                m2,
            ))

            self.assertEqual(order, list(sorted(order)))

            for a, b in combinations(order, 2):
                self.assertTrue(a < b)
                self.assertTrue(b > a)
                self.assertTrue(a <= b)
                self.assertTrue(b >= a)
                self.assertFalse(a == b)
                self.assertFalse(b < a)
                self.assertFalse(a > b)

            for a, b in combinations_with_replacement(order, 2):
                self.assertTrue(a <= b)
                self.assertFalse(a > b)

            for a in order:
                self.assertTrue(a == a)
                self.assertTrue(a <= a)
                self.assertTrue(a >= a)
                self.assertFalse(a != a)

            for c_ in self.constructors_unord:
                for a, b in product(order, repeat=2):
                    if c_(a) < c_(b):
                        self.assertTrue(a < b)
                    if c_(a) <= c_(b):
                        self.assertTrue(a <= b)

                    ops = (operator.lt, operator.le, operator.gt, operator.ge)
                    for o in ops:
                        self.assertRaises(NotImplementedError, o, c_(a), c(b))
                        self.assertRaises(NotImplementedError, o, c_(b), c(a))
                        self.assertRaises(NotImplementedError, o, c(a), c_(b))
                        self.assertRaises(NotImplementedError, o, c(b), c_(a))


    def test_nestable(self):
        from itertools import combinations, combinations_with_replacement, product

        c = nestable_orderable_frozenmultiset
        m1 = c([c([1, 0, 0]), 5, c([c([0]), 1, 1, 1])])
        m2 = c([c([c(), 1, 2]), c([5, 2, 5]), 5])
        m3 = c([c([1, 1]), c([c([0]), 1, 2]), 0])
        l = list(sorted((m1,m2,m3, c())))
        for m in l:
            self.assertEqual(l, l)

        for a, b in combinations(l, 2):
            self.assertTrue(a < b)
            self.assertTrue(a <= b)
            self.assertTrue(b > a)
            self.assertTrue(b >= a)
            self.assertFalse(a == b)
            self.assertFalse(b == a)
            self.assertFalse(a > b)
            self.assertFalse(a >= b)
            self.assertFalse(b < a)
            self.assertFalse(b <= a)

        for a, b in combinations_with_replacement(l, 2):
            self.assertTrue(a <= b)
            self.assertTrue(b >= a)
            self.assertFalse(a > b)
            self.assertFalse(b < a)

        for a, b in product(l, repeat=2):
            if a == b:
                self.assertTrue(a <= b)
                self.assertTrue(b <= a)
                self.assertTrue(a >= b)
                self.assertTrue(b >= a)
                self.assertEqual(b, a)
            else:
                self.assertFalse(a == b)
                self.assertFalse(b == a)
                self.assertTrue(a < b or a > b)
                self.assertTrue(b < a or b > a)

    def test_readme(self):
        # tests from the readme file
        from more_collections import multiset
        l = list(multiset('aaabbc')) # ['b', 'b', 'c', 'a', 'a', 'a']
        l.sort()
        self.assertEqual(l, ['a', 'a', 'a', 'b', 'b', 'c'])
        self.assertEqual(multiset('aaabbc').count('a'), 3)
        self.assertEqual(frozenset(multiset('aaabbc').items()), frozenset([('b', 2), ('c', 1), ('a', 3)]))

        a, b = multiset('ab'), multiset('bc')
        self.assertEqual(''.join(sorted(a | b)), 'abc') # 'acb'
        self.assertEqual(''.join(sorted(a & b)), 'b') # 'b'
        self.assertEqual(''.join(sorted(a ^ b)), 'ac') # 'ca'
        self.assertEqual(''.join(sorted(a - b)), 'a') # 'a'
        self.assertEqual(''.join(sorted(a + b)), 'abbc') # 'acbb'

        from more_collections import orderable_multiset
        a, b = orderable_multiset('abc'), orderable_multiset('bcd')
        self.assertTrue(a < b or a > b)

        from more_collections import nestable_orderable_frozenmultiset as nofms
        a, b = nofms('abc'), nofms((nofms('abc'),'c'))
        self.assertTrue(a < b or a > b)
