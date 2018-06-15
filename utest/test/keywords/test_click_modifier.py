import unittest

from mockito import mock, unstub
from selenium.webdriver.common.keys import Keys

from SeleniumLibrary.keywords import ElementKeywords


class ParsingModifierKeys(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = mock()
        cls.element = ElementKeywords(cls.ctx)

    @classmethod
    def tearDownClass(cls):
        unstub()

    def test_parsing_one_mofier(self):
        parsed = self.element.parse_modifier('CTRL')
        self.assertEqual(parsed, [Keys.CONTROL])
        parsed = self.element.parse_modifier('control')
        self.assertEqual(parsed, [Keys.CONTROL])
        parsed = self.element.parse_modifier('alt')
        self.assertEqual(parsed, [Keys.ALT])
        parsed = self.element.parse_modifier('sHifT')
        self.assertEqual(parsed, [Keys.SHIFT])

    def test_parsing_multiple_modifiers(self):
        parsed = self.element.parse_modifier('ctrl+shift')
        self.assertEqual(parsed, [Keys.CONTROL, Keys.SHIFT])

        parsed = self.element.parse_modifier('ctrl+alt+shift')
        self.assertEqual(parsed, [Keys.CONTROL, Keys.ALT, Keys.SHIFT])
