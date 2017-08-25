import unittest

from SeleniumLibrary.utils import is_string, is_truthy, is_falsy


class IsstringTests(unittest.TestCase):

    def test_is_string(self):
        strings = ['1', 'foo', ' ', u'', '']
        for item in strings:
            self.assertTrue(is_string(item))

    def test_is_not_string(self):
        strings = [1, 2.345, None, False]
        for item in strings:
            self.assertFalse(is_string(item))


class IsTruthyTests(unittest.TestCase):

    def test_is_truthy(self):
        truthys = ['1', 'foo', ' ', 1, 23.45, True, [1, 2], 'True', {'k': 'v'}]
        for item in truthys:
            self.assertTrue(is_truthy(item))

    def test_is_not_truthy(self):
        not_truthys = [0, False, None, [], {}, u'', '', 'False', 'None']
        for item in not_truthys:
            self.assertFalse(is_truthy(item))


class IsFalsyTest(unittest.TestCase):

    def test_is_falsy(self):
        truthys = ['1', 'foo', ' ', 1, 23.45, True, [1, 2], 'True', {'k': 'v'}]
        for item in truthys:
            self.assertFalse(is_falsy(item))

    def test_is_not_falsy(self):
        not_truthys = [0, False, None, [], {}, u'', '', 'False', 'None']
        for item in not_truthys:
            self.assertTrue(is_falsy(item))
