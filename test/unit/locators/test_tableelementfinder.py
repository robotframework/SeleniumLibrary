import unittest

from mockito import mock, verify, when, unstub

from SeleniumLibrary.locators.tableelementfinder import TableElementFinder


class ElementFinderTest(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self.ctx.element_finder = mock()
        self.finder = TableElementFinder(self.ctx)

    def tearDown(self):
        unstub()

    def test_find_by_col(self):
        element = mock()
        xpath = ['//tr//*[self::td or self::th][1]']
        when(self.finder)._search_in_locators('id:table', xpath,
                                              'content').thenReturn(element)
        self.finder.find_by_col('id:table', 1, 'content')

        xpath = ['//tbody/tr/td[position()=last()-(2-1)]',
                 '//tbody/tr/td[position()=last()-(2-1)]']
        when(self.finder)._search_in_locators('id:table', xpath,
                                              'content').thenReturn(element)
        self.finder.find_by_col('id:table', 1, 'content')

    def test_find_by_row(self):
        element = mock()
        xpath = ['//tr[2]//*']
        when(self.finder)._search_in_locators('xpath=//table', xpath,
                                              'content').thenReturn(element)
        self.finder.find_by_row('xpath=//table', 2, 'content')

        xpath = ['//tbody/tr[position()=last()-(3-1)]']
        when(self.finder)._search_in_locators('xpath=//table', xpath,
                                              'content').thenReturn(element)
        self.finder.find_by_row('xpath=//table', -3, 'content')

    def test_by_search_in_locators(self):
        xpath = ['//th']
        table = mock()
        element1 = mock()
        element2 = mock()
        element1.text = 'not here'
        element2.text = 'content'
        table_elements = [element1, element2]
        when(self.ctx.element_finder).find(
            'css=table', None, True, True, None).thenReturn(table)
        when(self.ctx.element_finder).find(
            xpath[0], None, False, False, table).thenReturn(table_elements)
        self.finder._search_in_locators('css=table', xpath, 'content')
