import unittest
import os
from Selenium2Library.elementfinder import ElementFinder
from mockito import *

class ElementFinderTests(unittest.TestCase):

    def test_find_with_invalid_prefix(self):
        finder = ElementFinder()
        browser = mock()
        with self.assertRaises(ValueError) as context:
            finder.find(browser, "something=test1")
        self.assertEqual(context.exception.message, "Locator with prefix 'something' is not supported")

    def test_find_with_no_tag(self):
        finder = ElementFinder()
        browser = mock()
        finder.find(browser, "test1")
        verify(browser).find_elements_by_xpath("//*[@id='test1' or @name='test1']")

    def test_find_with_tag(self):
        finder = ElementFinder()
        browser = mock()
        finder.find(browser, "test1", tag='div')
        verify(browser).find_elements_by_xpath("//div[@id='test1' or @name='test1']")

    def test_find_with_locator_with_apos(self):
        finder = ElementFinder()
        browser = mock()
        finder.find(browser, "test '1'")
        verify(browser).find_elements_by_xpath("//*[@id=\"test '1'\" or @name=\"test '1'\"]")

    def test_find_with_locator_with_quote(self):
        finder = ElementFinder()
        browser = mock()
        finder.find(browser, "test \"1\"")
        verify(browser).find_elements_by_xpath("//*[@id='test \"1\"' or @name='test \"1\"']")

    def test_find_with_locator_with_quote_and_apos(self):
        finder = ElementFinder()
        browser = mock()
        finder.find(browser, "test \"1\" and '2'")
        verify(browser).find_elements_by_xpath(
            "//*[@id=concat('test \"1\" and ', \"'\", '2', \"'\", '') or @name=concat('test \"1\" and ', \"'\", '2', \"'\", '')]")

    def test_find_with_a(self):
        finder = ElementFinder()
        browser = mock()
        when(browser).get_current_url().thenReturn("http://localhost/mypage.html")
        finder.find(browser, "test1", tag='a')
        verify(browser).find_elements_by_xpath(
            "//a[@id='test1' or @name='test1' or @href='test1' or normalize-space(descendant-or-self::text())='test1' or @href='http://localhost/test1']")

    def test_find_with_link_synonym(self):
        finder = ElementFinder()
        browser = mock()
        when(browser).get_current_url().thenReturn("http://localhost/mypage.html")
        finder.find(browser, "test1", tag='link')
        verify(browser).find_elements_by_xpath(
            "//a[@id='test1' or @name='test1' or @href='test1' or normalize-space(descendant-or-self::text())='test1' or @href='http://localhost/test1']")

    def test_find_with_img(self):
        finder = ElementFinder()
        browser = mock()
        when(browser).get_current_url().thenReturn("http://localhost/mypage.html")
        finder.find(browser, "test1", tag='img')
        verify(browser).find_elements_by_xpath(
            "//img[@id='test1' or @name='test1' or @src='test1' or @alt='test1' or @src='http://localhost/test1']")

    def test_find_with_image_synonym(self):
        finder = ElementFinder()
        browser = mock()
        when(browser).get_current_url().thenReturn("http://localhost/mypage.html")
        finder.find(browser, "test1", tag='image')
        verify(browser).find_elements_by_xpath(
            "//img[@id='test1' or @name='test1' or @src='test1' or @alt='test1' or @src='http://localhost/test1']")

    def test_find_with_input(self):
        finder = ElementFinder()
        browser = mock()
        when(browser).get_current_url().thenReturn("http://localhost/mypage.html")
        finder.find(browser, "test1", tag='input')
        verify(browser).find_elements_by_xpath(
            "//input[@id='test1' or @name='test1' or @value='test1' or @src='test1' or @src='http://localhost/test1']")

    def test_find_with_radio_button_synonym(self):
        finder = ElementFinder()
        browser = mock()
        when(browser).get_current_url().thenReturn("http://localhost/mypage.html")
        finder.find(browser, "test1", tag='radio button')
        verify(browser).find_elements_by_xpath(
            "//input[@id='test1' or @name='test1' or @value='test1' or @src='test1' or @src='http://localhost/test1']")

    def test_find_with_button(self):
        finder = ElementFinder()
        browser = mock()
        finder.find(browser, "test1", tag='button')
        verify(browser).find_elements_by_xpath(
            "//button[@id='test1' or @name='test1' or @value='test1' or normalize-space(descendant-or-self::text())='test1']")

    def test_find_by_class_name(self):
        finder = ElementFinder()
        browser = mock()

        elements = self.make_mock_elements('div', 'a', 'body', 'a')
        when(browser).find_elements_by_class_name("test1").thenReturn(elements)

        result = finder.find(browser, "class=test1")
        self.assertEqual(result, elements)
        result = finder.find(browser, "class=test1", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_css_selector(self):
        finder = ElementFinder()
        browser = mock()

        elements = self.make_mock_elements('div', 'a', 'body', 'a')
        when(browser).find_elements_by_css_selector("#test1").thenReturn(elements)

        result = finder.find(browser, "css=#test1")
        self.assertEqual(result, elements)
        result = finder.find(browser, "css=#test1", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_id(self):
        finder = ElementFinder()
        browser = mock()

        elements = self.make_mock_elements('div', 'a', 'body', 'a')
        when(browser).find_elements_by_id("test1").thenReturn(elements)

        result = finder.find(browser, "id=test1")
        self.assertEqual(result, elements)
        result = finder.find(browser, "id=test1", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_name(self):
        finder = ElementFinder()
        browser = mock()

        elements = self.make_mock_elements('div', 'a', 'body', 'a')
        when(browser).find_elements_by_name("test1").thenReturn(elements)

        result = finder.find(browser, "name=test1")
        self.assertEqual(result, elements)
        result = finder.find(browser, "name=test1", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_tag_name(self):
        finder = ElementFinder()
        browser = mock()

        elements = self.make_mock_elements('div', 'a', 'body', 'a')
        when(browser).find_elements_by_tag_name("div").thenReturn(elements)

        result = finder.find(browser, "tag=div")
        self.assertEqual(result, elements)
        result = finder.find(browser, "tag=div", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_xpath(self):
        finder = ElementFinder()
        browser = mock()

        elements = self.make_mock_elements('div', 'a', 'body', 'a')
        when(browser).find_elements_by_xpath("//*[@test='1']").thenReturn(elements)

        result = finder.find(browser, "xpath=//*[@test='1']")
        self.assertEqual(result, elements)
        result = finder.find(browser, "xpath=//*[@test='1']", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])


    def make_mock_elements(self, *tags):
        elements = []
        for tag in tags:
            element = mock()
            element.tag_name = tag
            elements.append(element)
        return elements

if __name__ == "__main__":
    unittest.main()
