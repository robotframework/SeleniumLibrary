import unittest

from mockito import mock, unstub, when

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
