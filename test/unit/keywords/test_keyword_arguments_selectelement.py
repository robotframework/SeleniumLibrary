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
        select = mock()
        element = mock()
        element.text = 'foo'
        elements = [element]
        when(self.element)._get_select_list_options(locator).thenReturn(
            (select, elements))
        self.element.get_list_items(locator)
        self.element.get_list_items(locator, 'None')
        self.element.get_list_items(locator, 'No')

    def test_get_list_items_true(self):
        locator = '//select'
        select = mock()
        element = mock()
        elements = [element]
        when(element).get_attribute('value').thenReturn('text')
        # when(element).get_attribute('value').thenReturn('text')
        when(self.element)._get_select_list_options(locator).thenReturn(
            (select, elements))
        self.element.get_list_items(locator, True)
        self.element.get_list_items(locator, 'True')
        self.element.get_list_items(locator, 'Yes')
