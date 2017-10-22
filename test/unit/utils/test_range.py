import unittest

from SeleniumLibrary.utils import parse_range


class RangeMatcherTests(unittest.TestCase):

    def test_range_as_number(self):
        self.assertEqual(parse_range(1), 1)
        self.assertEqual(parse_range('1'), 1)

    def test_range_as_range(self):
        self.assertEqual(parse_range('1..2'), (1, 2))
        self.assertEqual(parse_range('7..5'), (5, 7))

    def test_invalid_range(self):
        with self.assertRaisesRegexp(ValueError, 'Invalid range definition'):
            parse_range('0...1')
        with self.assertRaisesRegexp(ValueError, 'Invalid range definition'):
            parse_range('0.1')
        with self.assertRaisesRegexp(ValueError, 'Invalid range definition'):
            parse_range('0..-1')
        with self.assertRaisesRegexp(ValueError, 'Invalid range definition'):
            parse_range('-1..2')
        with self.assertRaisesRegexp(ValueError, 'Invalid range definition'):
            parse_range('1..A')
        with self.assertRaisesRegexp(ValueError, 'Invalid range definition'):
            parse_range('1A2')
