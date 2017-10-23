import unittest

from SeleniumLibrary.utils import parse_range


class RangeMatcherTests(unittest.TestCase):

    def test_range_as_number(self):
        value = parse_range(1)
        self.assertEqual(value.minimum, 1)
        self.assertEqual(value.maximum, 1)
        value = parse_range('1')
        self.assertEqual(value.minimum, 1)
        self.assertEqual(value.maximum, 1)

    def test_range_as_range(self):
        value = parse_range('1..2')
        self.assertEqual(value.minimum, 1)
        self.assertEqual(value.maximum, 2)
        value = parse_range('7..5')
        self.assertEqual(value.minimum, 5)
        self.assertEqual(value.maximum, 7)

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
        with self.assertRaisesRegexp(ValueError, 'Invalid range definition'):
            parse_range('1..C')
