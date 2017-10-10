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

    def test_click_element(self):
        element = mock()
        when(self.element).find_element('//div').thenReturn(element)
        self.element.click_element('//div')