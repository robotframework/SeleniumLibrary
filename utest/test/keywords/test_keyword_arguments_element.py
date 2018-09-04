import unittest

from mockito import mock, unstub, when
from robot.api import logger

from SeleniumLibrary.keywords import ElementKeywords


class KeywordArgumentsElementTest(unittest.TestCase):

    def setUp(self):
        ctx = mock()
        ctx._browser = mock()
        self.element = ElementKeywords(ctx)

    def tearDown(self):
        unstub()

    def test_locator_should_match_x_times(self):
        locator = '//div'
        when(self.element).find_elements(locator).thenReturn([])
        with self.assertRaisesRegexp(AssertionError, 'should have matched'):
            self.element.locator_should_match_x_times(locator, 1)

        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.element.locator_should_match_x_times(locator, 1, 'foobar')

    def test_element_text_should_be(self):
        locator = '//div'
        element = mock()
        element.text = 'text'
        when(self.element).find_element(locator).thenReturn(element)
        with self.assertRaisesRegexp(AssertionError, 'should have been'):
            self.element.element_text_should_be(locator, 'not text')
        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.element.element_text_should_be(locator, 'not text', 'foobar')

    def test_get_matching_xpath_count(self):
        locator = '//div'
        when(self.element).find_elements('xpath:' + locator).thenReturn([])
        count = self.element.get_matching_xpath_count(locator)
        self.assertEqual(count, '0')
        count = self.element.get_matching_xpath_count(locator, 'True')
        self.assertEqual(count, '0')

        count = self.element.get_matching_xpath_count(locator, 'False')
        self.assertEqual(count, 0)

    def test_xpath_should_match_x_times(self):
        locator = '//div'
        when(self.element).find_elements('xpath:{}'.format(locator)).thenReturn([])
        with self.assertRaisesRegexp(AssertionError, 'should have matched'):
            self.element.xpath_should_match_x_times(locator, 1)

        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.element.xpath_should_match_x_times(locator, 1, 'foobar')
