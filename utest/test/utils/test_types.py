import unittest

from SeleniumLibrary.utils import is_truthy, is_falsy, is_noney


class IsTruthyFalsyNoneyTests(unittest.TestCase):
    truthy = ['foo', ' ', 1, 2.3, True, [1], 'True', {'k': 'v'}]
    falsy = [0, False, None, [], {}, (), u'', '', 'False', 'None', '0', 'off']

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
