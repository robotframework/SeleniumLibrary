import unittest

from mockito import mock, verify, when, unstub

from Selenium2Library.locators.tableelementfinder import TableElementFinder


class ElementFinderTests(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self._browser = mock()
        self.ctx._browser = self._browser
        self.finder = TableElementFinder(self.ctx)

    def tearDown(self):
        unstub()

    def test_find_with_implicit_css_locator(self):
        when(self._browser).find_elements_by_css_selector(
            "table#test1").thenReturn([])
        self.finder.find("test1")
        verify(self._browser).find_elements_by_css_selector("table#test1")

    def test_find_with_css_selector(self):
        elements = self._make_mock_elements('table', 'table', 'table')
        when(self._browser).find_elements_by_css_selector(
            "table#test1").thenReturn(elements)
        self.assertEqual(
            self.finder.find("css=table#test1"),
            elements[0])
        verify(self._browser).find_elements_by_css_selector("table#test1")

    def test_find_with_xpath_selector(self):
        elements = self._make_mock_elements('table', 'table', 'table')
        when(self._browser).find_elements_by_xpath(
            "//table[@id='test1']").thenReturn(elements)
        self.assertEqual(
            self.finder.find("xpath=//table[@id='test1']"),
            elements[0])
        verify(self._browser).find_elements_by_xpath(
            "//table[@id='test1']")

    def test_find_with_content_constraint(self):
        elements = self._make_mock_elements('td', 'td', 'td')
        elements[1].text = 'hi'
        when(self._browser).find_elements_by_css_selector(
            "table#test1").thenReturn(elements)
        self.assertEqual(
            self.finder.find_by_content("test1", 'hi'),
            elements[1])
        verify(self._browser).find_elements_by_css_selector("table#test1")

    def test_find_with_null_content_constraint(self):
        elements = self._make_mock_elements('td', 'td', 'td')
        elements[1].text = 'hi'
        when(self._browser).find_elements_by_css_selector(
            "table#test1").thenReturn(elements)
        self.assertEqual(
            self.finder.find_by_content("test1", None),
            elements[0])
        verify(self._browser).find_elements_by_css_selector("table#test1")

    def test_find_by_content_with_css_locator(self):
        when(self._browser).find_elements_by_css_selector(
            "table#test1").thenReturn([])
        self.finder.find_by_content("css=table#test1", 'hi')
        verify(self._browser).find_elements_by_css_selector("table#test1")

    def test_find_by_content_with_xpath_locator(self):
        when(self._browser).find_elements_by_xpath(
            "//table[@id='test1']//*").thenReturn([])
        self.finder.find_by_content("xpath=//table[@id='test1']", 'hi')
        verify(self._browser).find_elements_by_xpath("//table[@id='test1']//*")

    def test_find_by_header_with_css_locator(self):
        when(self._browser).find_elements_by_css_selector(
            "table#test1 th").thenReturn([])
        self.finder.find_by_header("css=table#test1", 'hi')
        verify(self._browser).find_elements_by_css_selector("table#test1 th")

    def test_find_by_header_with_xpath_locator(self):
        when(self._browser).find_elements_by_xpath(
            "//table[@id='test1']//th").thenReturn([])
        self.finder.find_by_header("xpath=//table[@id='test1']", 'hi')
        verify(self._browser).find_elements_by_xpath(
            "//table[@id='test1']//th")

    def test_find_by_footer_with_css_locator(self):
        when(self._browser).find_elements_by_css_selector(
            "table#test1 tfoot td").thenReturn([])
        self.finder.find_by_footer("css=table#test1", 'hi')
        verify(self._browser).find_elements_by_css_selector(
            "table#test1 tfoot td")

    def test_find_by_footer_with_xpath_locator(self):
        when(self._browser).find_elements_by_xpath(
            "//table[@id='test1']//tfoot//td").thenReturn([])
        self.finder.find_by_footer("xpath=//table[@id='test1']", 'hi')
        verify(self._browser).find_elements_by_xpath("//table[@id='test1']"
                                                     "//tfoot//td")

    def test_find_by_row_with_css_locator(self):
        when(self._browser).find_elements_by_css_selector(
            "table#test1 tr:nth-child(2)").thenReturn([])
        self.finder.find_by_row("css=table#test1", 2, 'hi')
        verify(self._browser).find_elements_by_css_selector("table#test1 "
                                                            "tr:nth-child(2)")

    def test_find_by_row_with_xpath_locator(self):
        when(self._browser).find_elements_by_xpath(
            "//table[@id='test1']//tr[2]//*").thenReturn([])
        self.finder.find_by_row("xpath=//table[@id='test1']", 2, 'hi')
        verify(self._browser).find_elements_by_xpath("//table[@id='test1']"
                                                     "//tr[2]//*")

    def test_find_by_col_with_css_locator(self):
        when(self._browser).find_elements_by_css_selector(
            "table#test1 tr td:nth-child(2)").thenReturn([])
        when(self._browser).find_elements_by_css_selector(
            "table#test1 tr th:nth-child(2)").thenReturn([])
        self.finder.find_by_col("css=table#test1", 2, 'hi')
        verify(self._browser).find_elements_by_css_selector(
            "table#test1 tr td:nth-child(2)")
        verify(self._browser).find_elements_by_css_selector(
            "table#test1 tr th:nth-child(2)")

    def test_find_by_col_with_xpath_locator(self):
        when(self._browser).find_elements_by_xpath("//table[@id='test1']//tr//"
                                                   "*[self::td or self"
                                                   "::th][2]").thenReturn([])
        self.finder.find_by_col("xpath=//table[@id='test1']", 2, 'hi')
        verify(self._browser).find_elements_by_xpath("//table[@id='test1']"
                                                     "//tr//*[self::td or self"
                                                     "::th][2]")

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
