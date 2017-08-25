import unittest

from mockito import mock, unstub, when
from mockito.matchers import ANY

from SeleniumLibrary.keywords import WaitingKeywords


class KeywordArgumentsWaitingKeywordsTest(unittest.TestCase):

    def setUp(self):
        ctx = mock()
        ctx._browser = mock()
        ctx._timeout_in_secs = 0.01
        self.waiting = WaitingKeywords(ctx)
        self.ctx = ctx

    def tearDown(self):
        unstub()

    def test_wait_for_condition(self):
        condition = 'return document.getElementById("intro")'
        error = 'did not become true'
        with self.assertRaisesRegexp(AssertionError, error):
            self.waiting.wait_for_condition(condition)
        with self.assertRaisesRegexp(AssertionError, 'foobar'):
            self.waiting.wait_for_condition(condition, 'None', 'foobar')

    def test_wait_until_page_contains(self):
        text = 'text'
        when(self.waiting.element).is_text_present(text).thenReturn(None)
        with self.assertRaisesRegexp(AssertionError, "Text 'text' did not"):
            self.waiting.wait_until_page_contains(text)
        with self.assertRaisesRegexp(AssertionError, "error"):
            self.waiting.wait_until_page_contains(text, 'None', 'error')
