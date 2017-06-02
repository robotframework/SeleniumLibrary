import unittest

from Selenium2Library.locators.elementfinder import ElementFinder


class LocatorParserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parse = ElementFinder()._parse_locator

    def test_parse_xpath(self):
        prefix, criteria = self.parse('//foo/bar')
        self.assertEqual(prefix, 'xpath')
        self.assertEqual(criteria, '//foo/bar')

        prefix, criteria = self.parse('(//foo/bar)[2]')
        self.assertEqual(prefix, 'xpath')
        self.assertEqual(criteria, '(//foo/bar)[2]')

        prefix, criteria = self.parse('xpath=//foo[@attr=value]')
        self.assertEqual(prefix, 'xpath')
        self.assertEqual(criteria, '//foo[@attr=value]')

    def test_parse_dom(self):
        prefix, criteria = self.parse(
            'dom=document.images[56]')
        self.assertEqual(prefix, 'dom')
        self.assertEqual(criteria, 'document.images[56]')

    def test_parse_link(self):
        prefix, criteria = self.parse('link=My Link')
        self.assertEqual(prefix, 'link')
        self.assertEqual(criteria, 'My Link')

        prefix, criteria = self.parse('partial link=y Lin')
        self.assertEqual(prefix, 'partial link')
        self.assertEqual(criteria, 'y Lin')

    def test_parse_id(self):
        prefix, criteria = self.parse('id=my_element')
        self.assertEqual(prefix, 'id')
        self.assertEqual(criteria, 'my_element')

        prefix, criteria = self.parse('my_element')
        self.assertEqual(prefix, 'default')
        self.assertEqual(criteria, 'my_element')

    def test_parse_leave_trailing_spaces(self):
        prefix, criteria = self.parse('id= test1  ')
        self.assertEqual(prefix, 'id')
        self.assertEqual(criteria, 'test1  ')

        prefix, criteria = self.parse('//foo/bar  ')
        self.assertEqual(prefix, 'xpath')
        self.assertEqual(criteria, '//foo/bar  ')

    def test_parse_identifier(self):
        prefix, criteria = self.parse('identifier=my_element')
        self.assertEqual(prefix, 'identifier')
        self.assertEqual(criteria, 'my_element')

    def test_parse_default(self):
        prefix, criteria = self.parse('default=page?a=b')
        self.assertEqual(prefix, 'default')
        self.assertEqual(criteria, 'page?a=b')

    def test_parse_invalid(self):
        prefix, criteria = self.parse('foo=bar')
        self.assertEqual(prefix, 'foo')
        self.assertEqual(criteria, 'bar')

    def test_parse_empty(self):
        prefix, criteria = self.parse('')
        self.assertEqual(prefix, 'default')
        self.assertEqual(criteria, '')
