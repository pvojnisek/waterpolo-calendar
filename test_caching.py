
import unittest
from caching import Caching
import random
from time import sleep, time


def random_number(seed: int) -> float:
    random.seed(seed)
    return time()


def concat_strings(st1: str, st2: str) -> str:
    return st1 + st2


def contcat_strings_random(st1: str, st2: str, seed: int) -> str:
    return concat_strings(st1, st2)+str(random_number(seed))


class CachingTest(unittest.TestCase):

    def setUp(self) -> None:
        pass

    def tearDown(self) -> None:
        pass

    def test_basic_functions(self):
        '''Basic functions'''
        ch = Caching(10, random_number)

        val = ch.get('first')
        self.assertEqual(val, ch.get('first'))
        self.assertNotEqual(val, ch.get('second'))

    def test_forget(self):
        '''Forgetting after timeout'''
        ch = Caching(1, random_number)
        val = ch.get('first')
        self.assertEqual(val, ch.get('first'))
        sleep(2)
        self.assertNotEqual(val, ch.get('first'))

    def test_multiple_parameters(self):
        ''''''
        ch = Caching(10, concat_strings)
        val = ch.get(('s1', 's2'))
        self.assertEqual(val, 's1s2')

    def test_multiple_parameters_timer(self):
        ch = Caching(1, contcat_strings_random)
        val = ch.get(('s1', 's2', 42))
        self.assertEqual(val, ch.get(('s1', 's2', 42)))
        self.assertNotEqual(val, ch.get(('s1', 's2', 43)))
        sleep(2)
        self.assertNotEqual(val, ch.get(('s1', 's2', 42)))
        self.assertNotEqual(val, ch.get(('s1', 's2', 43)))
