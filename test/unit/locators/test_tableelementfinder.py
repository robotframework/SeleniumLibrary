import unittest
from Selenium2Library.locators import TableElementFinder
from mockito import *

class ElementFinderTests(unittest.TestCase):

    def test_find_with_implicit_css_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_css_selector("table#test1").thenReturn([])
        
        finder.find(browser, "test1")

        verify(browser).find_elements_by_css_selector("table#test1")

    def test_find_with_css_selector(self):
        finder = TableElementFinder()
        browser = mock()
        elements = self._make_mock_elements('table', 'table', 'table')
        when(browser).find_elements_by_css_selector("table#test1").thenReturn(elements)
        
        self.assertEqual(
            finder.find(browser, "css=table#test1"),
            elements[0])

        verify(browser).find_elements_by_css_selector("table#test1")

    def test_find_with_xpath_selector(self):
        finder = TableElementFinder()
        browser = mock()
        elements = self._make_mock_elements('table', 'table', 'table')
        when(browser).find_elements_by_xpath("//table[@id='test1']").thenReturn(elements)
        
        self.assertEqual(
            finder.find(browser, "xpath=//table[@id='test1']"),
            elements[0])

        verify(browser).find_elements_by_xpath("//table[@id='test1']")

    def test_find_with_content_constraint(self):
        finder = TableElementFinder()
        browser = mock()
        elements = self._make_mock_elements('td', 'td', 'td')
        elements[1].text = 'hi'
        when(browser).find_elements_by_css_selector("table#test1").thenReturn(elements)
        
        self.assertEqual(
            finder.find_by_content(browser, "test1", 'hi'),
            elements[1])

        verify(browser).find_elements_by_css_selector("table#test1")

    def test_find_with_null_content_constraint(self):
        finder = TableElementFinder()
        browser = mock()
        elements = self._make_mock_elements('td', 'td', 'td')
        elements[1].text = 'hi'
        when(browser).find_elements_by_css_selector("table#test1").thenReturn(elements)
        
        self.assertEqual(
            finder.find_by_content(browser, "test1", None),
            elements[0])

        verify(browser).find_elements_by_css_selector("table#test1")

    def test_find_by_content_with_css_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_css_selector("table#test1").thenReturn([])
        
        finder.find_by_content(browser, "css=table#test1", 'hi')

        verify(browser).find_elements_by_css_selector("table#test1")

    def test_find_by_content_with_xpath_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_xpath("//table[@id='test1']//*").thenReturn([])
        
        finder.find_by_content(browser, "xpath=//table[@id='test1']", 'hi')

        verify(browser).find_elements_by_xpath("//table[@id='test1']//*")

    def test_find_by_header_with_css_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_css_selector("table#test1 th").thenReturn([])
        
        finder.find_by_header(browser, "css=table#test1", 'hi')

        verify(browser).find_elements_by_css_selector("table#test1 th")

    def test_find_by_header_with_xpath_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_xpath("//table[@id='test1']//th").thenReturn([])
        
        finder.find_by_header(browser, "xpath=//table[@id='test1']", 'hi')

        verify(browser).find_elements_by_xpath("//table[@id='test1']//th")

    def test_find_by_footer_with_css_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_css_selector("table#test1 tfoot td").thenReturn([])
        
        finder.find_by_footer(browser, "css=table#test1", 'hi')

        verify(browser).find_elements_by_css_selector("table#test1 tfoot td")

    def test_find_by_footer_with_xpath_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_xpath("//table[@id='test1']//tfoot//td").thenReturn([])
        
        finder.find_by_footer(browser, "xpath=//table[@id='test1']", 'hi')

        verify(browser).find_elements_by_xpath("//table[@id='test1']//tfoot//td")

    def test_find_by_row_with_css_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_css_selector("table#test1 tr:nth-child(2)").thenReturn([])
        
        finder.find_by_row(browser, "css=table#test1", 2, 'hi')

        verify(browser).find_elements_by_css_selector("table#test1 tr:nth-child(2)")

    def test_find_by_row_with_xpath_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_xpath("//table[@id='test1']//tr[2]//*").thenReturn([])
        
        finder.find_by_row(browser, "xpath=//table[@id='test1']", 2, 'hi')

        verify(browser).find_elements_by_xpath("//table[@id='test1']//tr[2]//*")

    def test_find_by_col_with_css_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_css_selector("table#test1 tr td:nth-child(2)").thenReturn([])
        when(browser).find_elements_by_css_selector("table#test1 tr th:nth-child(2)").thenReturn([])
        
        finder.find_by_col(browser, "css=table#test1", 2, 'hi')

        verify(browser).find_elements_by_css_selector("table#test1 tr td:nth-child(2)")
        verify(browser).find_elements_by_css_selector("table#test1 tr th:nth-child(2)")

    def test_find_by_col_with_xpath_locator(self):
        finder = TableElementFinder()
        browser = mock()
        when(browser).find_elements_by_xpath("//table[@id='test1']//tr//*[self::td or self::th][2]").thenReturn([])
        
        finder.find_by_col(browser, "xpath=//table[@id='test1']", 2, 'hi')

        verify(browser).find_elements_by_xpath("//table[@id='test1']//tr//*[self::td or self::th][2]")

    def _make_mock_elements(self, *tags):
        elements = []
        for tag in tags:
            element = self._make_mock_element(tag)
            elements.append(element)
        return elements

    def _make_mock_element(self, tag):
        element = mock()
        element.tag_name = tag
        element.attributes = {}
        element.text = None

        def set_attribute(name, value):
            element.attributes[name] = value
        element.set_attribute = set_attribute

        def get_attribute(name):
            return element.attributes[name]
        element.get_attribute = get_attribute

        return element
