import unittest

from SeleniumLibrary.utils import escape_xpath_value


class UtilsPackageTests(unittest.TestCase):

    def test_escape_xpath_value_with_apos(self):
        self.assertEqual(escape_xpath_value("test '1'"),
                         "\"test '1'\"")

    def test_escape_xpath_value_with_quote(self):
        self.assertEqual(escape_xpath_value("test \"1\""),
                         "'test \"1\"'")

    def test_escape_xpath_value_with_quote_and_apos(self):
        self.assertEqual(escape_xpath_value("test \"1\" and '2'"),
                         "concat('test \"1\" and ', \"'\", '2', \"'\", '')")
