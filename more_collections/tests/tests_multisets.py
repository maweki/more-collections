from unittest import TestCase
from more_collections.multisets import multiset, frozenmultiset, orderable_multiset, orderable_frozenmultiset
from itertools import chain, repeat, product

class TestPuredict(TestCase):

    constructors_ord = (orderable_multiset, orderable_frozenmultiset)
    constructors_unord = (multiset, frozenmultiset)
    constructors = constructors_unord + constructors_ord
    test_depth = 10

    def test_constructors(self):
        cnt = 2**self.test_depth

        for c in self.constructors:
            ms = c()
            self.assertEqual(0, len(ms))

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
