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