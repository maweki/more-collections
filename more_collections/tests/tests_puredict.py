from unittest import TestCase
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
