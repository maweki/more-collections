from unittest import TestCase, skip
from more_collections import puredict

class TestPuredict(TestCase):

    def tests(self):
        self.assertEqual(puredict.puredict(), puredict.empty())

        e = puredict.empty().insert(2,4).insert(6,4).insert(2,5).delete(6)
        self.assertEqual(len(frozenset((e))),1)
        self.assertEqual(len(e), 1)
        self.assertIn(2, e)
        self.assertNotIn(6, e)
        self.assertRaises(KeyError, e.__getitem__, 6)

    def test_constructor_empty(self):
        e = puredict.puredict()
        self.assertEqual(e, puredict.empty())

    def test_constructor_dict(self):
        e = puredict.puredict({"a":2, "b":5})
        self.assertIn("a", e)
        self.assertIn("b", e)
        self.assertEqual(e['a'], 2)
        self.assertEqual(e['b'], 5)
        self.assertEqual(len(e), 2)

    def test_constructor_iterable(self):
        e = puredict.puredict(zip('aab', 'cfg'))
        self.assertIn("a", e)
        self.assertIn("b", e)
        self.assertEqual(e['a'], 'f')
        self.assertEqual(e['b'], 'g')
        self.assertEqual(len(e), 2)

    def test_constructor_named_params(self):
        e = puredict.puredict(a=2, b=5)
        self.assertIn("a", e)
        self.assertIn("b", e)
        self.assertEqual(e['a'], 2)
        self.assertEqual(e['b'], 5)
        self.assertEqual(len(e), 2)

    def test_constructors_doc(self):
        dict = puredict.puredict
        # example from
        # https://docs.python.org/3/library/stdtypes.html?highlight=dict#dict
        a = dict(one=1, two=2, three=3)
        b = {'one': 1, 'two': 2, 'three': 3}
        c = dict(zip(['one', 'two', 'three'], [1, 2, 3]))
        d = dict([('two', 2), ('one', 1), ('three', 3)])
        e = dict({'three': 3, 'one': 1, 'two': 2})
        self.assertTrue(a == b == c == d == e)
