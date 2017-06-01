import unittest

from Selenium2Library.locators.elementfinder import LocatorParser


class LocatorParserTests(unittest.TestCase):

    def test_parse_xpath(self):
        prefix, criteria = LocatorParser.parse('//foo/bar')
        self.assertEqual(prefix, 'xpath')
        self.assertEqual(criteria, '//foo/bar')

        prefix, criteria = LocatorParser.parse('(//foo/bar)[2]')
        self.assertEqual(prefix, 'xpath')
        self.assertEqual(criteria, '(//foo/bar)[2]')

        prefix, criteria = LocatorParser.parse(
            'xpath=//foo[@attr=value]')
        self.assertEqual(prefix, 'xpath')
        self.assertEqual(criteria, '//foo[@attr=value]')

    def test_parse_dom(self):
        prefix, criteria = LocatorParser.parse(
            'dom=document.images[56]')
        self.assertEqual(prefix, 'dom')
        self.assertEqual(criteria, 'document.images[56]')

    def test_parse_link(self):
        prefix, criteria = LocatorParser.parse('link=My Link')
        self.assertEqual(prefix, 'link')
        self.assertEqual(criteria, 'My Link')

        prefix, criteria = LocatorParser.parse('partial link=y Lin')
        self.assertEqual(prefix, 'partial link')
        self.assertEqual(criteria, 'y Lin')

    def test_parse_id(self):
        prefix, criteria = LocatorParser.parse('id=my_element')
        self.assertEqual(prefix, 'id')
        self.assertEqual(criteria, 'my_element')

        prefix, criteria = LocatorParser.parse('my_element')
        self.assertEqual(prefix, 'default')
        self.assertEqual(criteria, 'my_element')

        prefix, criteria = LocatorParser.parse('id= test1  ')
        self.assertEqual(prefix, 'id')
        self.assertEqual(criteria, 'test1')

    def test_parse_identifier(self):
        prefix, criteria = LocatorParser.parse('identifier=my_element')
        self.assertEqual(prefix, 'identifier')
        self.assertEqual(criteria, 'my_element')

    def test_parse_default(self):
        prefix, criteria = LocatorParser.parse('default=page?a=b')
        self.assertEqual(prefix, 'default')
        self.assertEqual(criteria, 'page?a=b')
