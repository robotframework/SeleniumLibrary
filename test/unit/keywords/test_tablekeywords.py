import unittest

from mockito import mock, when, unstub

from SeleniumLibrary.keywords import TableElementKeywords


class TableKeywordsTest(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self.ctx._element_finder = mock()
        self.finder = TableElementKeywords(self.ctx)

    def tearDown(self):
        unstub()

    def test_find_by_column(self):
        xpath = '//tr//*[self::td or self::th][1]'
        when(self.finder)._find('id:table', xpath, 'content').thenReturn(mock())
        self.finder._find_by_column('id:table', 1, 'content')

    def test_find_by_column_with_negative_index(self):
        xpath = '//tr//*[self::td or self::th][position()=last()]'
        when(self.finder)._find('id:table', xpath, 'content').thenReturn(mock())
        self.finder._find_by_column('id:table', -1, 'content')

    def test_find_by_row(self):
        xpath = '//tr[2]'
        when(self.finder)._find('xpath=//table', xpath, 'content').thenReturn(mock())
        self.finder._find_by_row('xpath=//table', 2, 'content')

    def test_find_by_row_with_negative_index(self):
        xpath = '//tr[position()=last()-2]'
        when(self.finder)._find('xpath=//table', xpath, 'content').thenReturn(mock())
        self.finder._find_by_row('xpath=//table', -3, 'content')
