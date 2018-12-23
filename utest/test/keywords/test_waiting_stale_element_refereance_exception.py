import unittest

from selenium.common.exceptions import StaleElementReferenceException
from mockito import mock, when, unstub

from SeleniumLibrary.keywords import WaitingKeywords


def _raise(*a):
    raise StaleElementReferenceException('Darn')


class TableKeywordsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.ctx = mock()
        cls.waiting = WaitingKeywords(cls.ctx)
        cls.timeout = 0.5
        cls.count = 0

    def tearDown(self):
        unstub()

    def test_wait_until_element_is_visible(self):
        locator = '//div'
        element = mock()
        when(self.waiting).find_element(locator, required=False).thenReturn(element)
        when(element).is_displayed().thenRaise(StaleElementReferenceException()).thenReturn(True)
        self.waiting.wait_until_element_is_visible(locator, self.timeout)

    def test_wait_until_element_is_visible_fails(self):
        locator = '//div'
        element = mock()
        when(self.waiting).find_element(locator, required=False).thenReturn(element)
        when(element).is_displayed().thenRaise(StaleElementReferenceException('foo'))
        with self.assertRaisesRegexp(AssertionError, 'Message: foo'):
            self.waiting.wait_until_element_is_visible(locator, self.timeout)

    def test_wait_until_element_is_not_visible(self):
        locator = '//div'
        element = mock()
        when(self.waiting).find_element(locator, required=False).thenReturn(element)
        when(element).is_displayed().thenRaise(StaleElementReferenceException()).thenReturn(False)
        self.waiting.wait_until_element_is_not_visible(locator, self.timeout)

    def test_wait_until_element_is_enabled(self):
        locator = '//div'
        element = mock()
        when(self.waiting).find_element(locator, None).thenReturn(element)
        when(element).is_enabled().thenRaise(StaleElementReferenceException()).thenReturn(True)
        self.waiting.wait_until_element_is_enabled(locator, self.timeout)

    def test_wait_until_element_is_enabled_get_attribute_readonly(self):
        locator = '//div'
        element = mock()
        when(self.waiting).find_element(locator, None).thenReturn(element)
        when(element).is_enabled().thenReturn(True)
        when(element).get_attribute('readonly').thenRaise(StaleElementReferenceException()).thenReturn(None)
        self.waiting.wait_until_element_is_enabled(locator, self.timeout)

    def test_wait_until_element_is_enabled_fails(self):
        locator = '//div'
        element = mock()
        when(self.waiting).find_element(locator, None).thenReturn(element)
        when(element).is_enabled().thenRaise(StaleElementReferenceException('foo'))
        with self.assertRaisesRegexp(AssertionError, 'Message: foo'):
            self.waiting.wait_until_element_is_enabled(locator, self.timeout)

    def test_wait_until_element_contains(self):
        locator = '//div'
        text = 'foo'
        element1, element2 = mock(), mock({'text': 'foobar'})
        element1.__class__.text = property(_raise)
        when(self.waiting).find_element(locator).thenReturn(element1).thenReturn(element2)
        self.waiting.wait_until_element_contains(locator, text, self.timeout)

    def test_wait_until_element_does_not_contain(self):
        locator = '//div'
        text = 'foo'
        element1, element2 = mock(), mock({'text': 'tidii'})
        element1.__class__.text = property(_raise)
        when(self.waiting).find_element(locator).thenReturn(element1).thenReturn(element2)
        self.waiting.wait_until_element_does_not_contain(locator, text, self.timeout)
