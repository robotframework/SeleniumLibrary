import unittest

from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.locators import ElementFinder, TableElementFinder


class TableElementFinderInAPITest(unittest.TestCase):

    def test_table_finder(self):
        sl = SeleniumLibrary()
        self.assertIsInstance(sl.table_element_finder, TableElementFinder)


class ElementFinderInAPITest(unittest.TestCase):

    def test_table_finder(self):
        sl = SeleniumLibrary()
        self.assertIsInstance(sl.element_finder, ElementFinder)
