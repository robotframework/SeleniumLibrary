import unittest

from robot.utils.asserts import assert_equal, assert_not_equal, assert_raises
from SeleniumLibrary.utils import DotDict


class TestDotDict(unittest.TestCase):

    def setUp(self):
        self.ad = DotDict([('z', 1), (2, 'y'), ('x', 3)])

    def test_get(self):
        assert_equal(self.ad[2], 'y')
        assert_equal(self.ad.x, 3)
        assert_raises(KeyError, self.ad.__getitem__, 'nonex')
        assert_raises(AttributeError, self.ad.__getattr__, 'nonex')

    def test_equality_with_normal_dict(self):
        assert_equal(self.ad, {'z': 1, 2: 'y', 'x': 3})

    def test_set(self):
        self.ad.x = 42
        self.ad.new = 43
        self.ad[2] = 44
        self.ad['n2'] = 45
        assert_equal(self.ad, {'z': 1, 2: 44, 'x': 42, 'new': 43, 'n2': 45})

    def test_del(self):
        del self.ad.x
        del self.ad[2]
        self.ad.pop('z')
        assert_equal(self.ad, {})
        assert_raises(KeyError, self.ad.__delitem__, 'nonex')
        assert_raises(AttributeError, self.ad.__delattr__, 'nonex')

    def test_same_str_and_repr_format_as_with_normal_dict(self):
        D = {'foo': 'bar', '"\'': '"\'', '\n': '\r', 1: 2, (): {}, True: False}
        for d in {}, {'a': 1}, D:
            for formatter in str, repr:
                result = formatter(DotDict(d))
                assert_equal(eval(result, {}), d)

if __name__ == '__main__':
    unittest.main()
