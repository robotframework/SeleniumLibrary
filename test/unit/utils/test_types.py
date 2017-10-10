import unittest

from SeleniumLibrary.utils import is_string, is_truthy, is_falsy, is_noney


class IsstringTests(unittest.TestCase):

    def test_is_string(self):
        strings = ['1', 'foo', ' ', u'', '']
        for item in strings:
            self.assertTrue(is_string(item))

    def test_is_not_string(self):
        strings = [1, 2.345, None, False]
        for item in strings:
            self.assertFalse(is_string(item))


class IsTruthyFalsyNoneyTests(unittest.TestCase):
    truthy = ['0', 'foo', ' ', 1, 2.3, True, [1], 'True', {'k': 'v'}]
    falsy = [0, False, None, [], {}, (), u'', '', 'False', 'None']

    def test_is_truthy(self):
        for item in self.truthy:
            self.assertTrue(is_truthy(item) is True)
        for item in self.falsy:
            self.assertTrue(is_truthy(item) is False)

    def test_is_falsy(self):
        for item in self.truthy:
            self.assertTrue(is_falsy(item) is False)
        for item in self.falsy:
            self.assertTrue(is_falsy(item) is True)

    def test_is_noney(self):
        for item in [None, 'None', 'NONE', 'none']:
            self.assertTrue(is_noney(item) is True)
        for item in self.truthy + [False, 0, 'False', '', [], {}, ()]:
            self.assertTrue(is_noney(item) is False)
