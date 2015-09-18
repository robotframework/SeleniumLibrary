import unittest

from robot.utils.asserts import assert_equal, assert_not_equal, assert_raises
from Selenium2Library.utils import AttrDict
try:
    from robot.utils import IRONPYTHON
except ImportError:  # New in RF 2.9
    import sys
    IRONPYTHON = sys.platform == 'cli'
    pass


class TestAttrDict(unittest.TestCase):

    def setUp(self):
        self.dd = AttrDict([('z', 1), (2, 'y'), ('x', 3)])

    def test_get(self):
        assert_equal(self.dd[2], 'y')
        assert_equal(self.dd.x, 3)
        assert_raises(KeyError, self.dd.__getitem__, 'nonex')
        assert_raises(AttributeError, self.dd.__getattr__, 'nonex')

    def test_equality_with_normal_dict(self):
        assert_equal(self.dd, {'z': 1, 2: 'y', 'x': 3})

    def test_set(self):
        self.dd.x = 42
        self.dd.new = 43
        self.dd[2] = 44
        self.dd['n2'] = 45
        assert_equal(self.dd, {'z': 1, 2: 44, 'x': 42, 'new': 43, 'n2': 45})

    def test_del(self):
        del self.dd.x
        del self.dd[2]
        self.dd.pop('z')
        assert_equal(self.dd, {})
        assert_raises(KeyError, self.dd.__delitem__, 'nonex')
        assert_raises(AttributeError, self.dd.__delattr__, 'nonex')

    def test_same_str_and_repr_format_as_with_normal_dict(self):
        D = {'foo': 'bar', '"\'': '"\'', '\n': '\r', 1: 2, (): {}, True: False}
        for d in {}, {'a': 1}, D:
            for formatter in str, repr:
                result = formatter(AttrDict(d))
                assert_equal(eval(result, {}), d)

if __name__ == '__main__':
    unittest.main()
