import unittest

from mockito import mock, unstub, when


from SeleniumLibrary.keywords import SelectElementKeywords


class KeywordArgumentsElementTest(unittest.TestCase):

    def setUp(self):
        ctx = mock()
        ctx._browser = mock()
        self.element = SelectElementKeywords(ctx)
        self.ctx = ctx

    def tearDown(self):
        unstub()

    def test_get_list_items_false(self):
        locator = '//select'
        element = mock()
        element.text = 'foo'
        when(self.element)._get_options(locator).thenReturn([element])
        self.element.get_list_items(locator)
        self.element.get_list_items(locator, 'None')
        self.element.get_list_items(locator, 'No')

    def test_get_list_items_true(self):
        locator = '//select'
        element = mock()
        when(element).get_attribute('value').thenReturn('text')
        when(self.element)._get_options(locator).thenReturn([element])
        self.element.get_list_items(locator, True)
        self.element.get_list_items(locator, 'True')
        self.element.get_list_items(locator, 'Yes')
