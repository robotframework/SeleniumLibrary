import unittest

from mockito import any, mock, verify, when
from robot.utils.asserts import assert_raises_with_msg

from Selenium2Library.locators.elementfinder import ElementFinder


class ElementFinderTests(unittest.TestCase):

    def test_find_with_invalid_prefix(self):
        ctx = mock()
        finder = ElementFinder(ctx)
        assert_raises_with_msg(ValueError, "Element locator with prefix 'something' is not supported.",
                               finder.find, "something=test1")
        assert_raises_with_msg(ValueError, "Element locator with prefix 'by ID' is not supported.",
                               finder.find, " by ID =test1")

    def test_find_with_null_browser(self):
        ctx = mock()
        finder = ElementFinder(ctx)
        self.assertRaises(AttributeError, finder.find, None, "id=test1")

    def test_find_with_no_tag(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("test1")
        verify(ctx._browser).find_elements_by_xpath("//*[(@id='test1' or "
                                                    "@name='test1')]")

    def test_find_with_explicit_default_strategy(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("default=test1")
        verify(ctx._browser).find_elements_by_xpath("//*[(@id='test1' or "
                                                    "@name='test1')]")

    def test_find_with_explicit_default_strategy_and_equals(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("default=page.do?foo=bar", tag='a')
        verify(ctx._browser).find_elements_by_xpath(
            "//a[(@id='page.do?foo=bar' or @name='page.do?foo=bar' or "
            "@href='page.do?foo=bar' or "
            "normalize-space(descendant-or-self::text())='page.do?foo=bar' or "
            "@href='http://localhost/page.do?foo=bar')]")

    def test_find_with_tag(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("test1", tag='div')
        verify(ctx._browser).find_elements_by_xpath("//div[(@id='test1' or "
                                                    "@name='test1')]")

    def test_find_with_locator_with_apos(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("test '1'")
        verify(ctx._browser).find_elements_by_xpath("//*[(@id=\"test '1'\" or "
                                                    "@name=\"test '1'\")]")

    def test_find_with_locator_with_quote(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("test \"1\"")
        verify(ctx._browser).find_elements_by_xpath("//*[(@id='test \"1\"' or "
                                                    "@name='test \"1\"')]")

    def test_find_with_locator_with_quote_and_apos(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("test \"1\" and '2'")
        verify(ctx._browser).find_elements_by_xpath(
            "//*[(@id=concat('test \"1\" and ', \"'\", '2', \"'\", '') "
            "or @name=concat('test \"1\" and ', \"'\", '2', \"'\", ''))]")

    def test_find_with_a(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='a')
        verify(ctx._browser).find_elements_by_xpath(
            "//a[(@id='test1' or @name='test1' or @href='test1' or "
            "normalize-space(descendant-or-self::text())='test1' or "
            "@href='http://localhost/test1')]")

    def test_find_with_link_synonym(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='link')
        verify(ctx._browser).find_elements_by_xpath(
            "//a[(@id='test1' or @name='test1' or @href='test1' or "
            "normalize-space(descendant-or-self::text())='test1' or "
            "@href='http://localhost/test1')]")

    def test_find_with_img(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='img')
        verify(ctx._browser).find_elements_by_xpath(
            "//img[(@id='test1' or @name='test1' or @src='test1' or "
            "@alt='test1' or @src='http://localhost/test1')]")

    def test_find_with_image_synonym(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='image')
        verify(ctx._browser).find_elements_by_xpath(
            "//img[(@id='test1' or @name='test1' or @src='test1' or "
            "@alt='test1' or @src='http://localhost/test1')]")

    def test_find_with_input(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='input')
        verify(ctx._browser).find_elements_by_xpath(
            "//input[(@id='test1' or @name='test1' or @value='test1' or "
            "@src='test1' or @src='http://localhost/test1')]")

    def test_find_with_radio_button_synonym(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='radio button')
        verify(ctx._browser).find_elements_by_xpath(
            "//input[@type='radio' and (@id='test1' or @name='test1' or "
            "@value='test1' or @src='test1' or "
            "@src='http://localhost/test1')]")

    def test_find_with_checkbox_synonym(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='checkbox')
        verify(ctx._browser).find_elements_by_xpath(
            "//input[@type='checkbox' and (@id='test1' or @name='test1' or "
            "@value='test1' or @src='test1' or "
            "@src='http://localhost/test1')]")

    def test_find_with_file_upload_synonym(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='file upload')
        verify(ctx._browser).find_elements_by_xpath(
            "//input[@type='file' and (@id='test1' or @name='test1' or "
            "@value='test1' or @src='test1' or "
            "@src='http://localhost/test1')]")

    def test_find_with_text_field_synonym(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        ctx._browser.current_url = "http://localhost/mypage.html"
        finder.find("test1", tag='text field')
        verify(ctx._browser).find_elements_by_xpath(
            "//input[@type='text' and (@id='test1' or @name='test1' or "
            "@value='test1' or @src='test1' or "
            "@src='http://localhost/test1')]")

    def test_find_with_button(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("test1", tag='button')
        verify(ctx._browser).find_elements_by_xpath(
            "//button[(@id='test1' or @name='test1' or @value='test1' or "
            "normalize-space(descendant-or-self::text())='test1')]")

    def test_find_with_select(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("test1", tag='select')
        verify(ctx._browser).find_elements_by_xpath(
            "//select[(@id='test1' or @name='test1')]")

    def test_find_with_list_synonym(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        finder.find("test1", tag='list')
        verify(ctx._browser).find_elements_by_xpath(
            "//select[(@id='test1' or @name='test1')]")

    def test_find_with_implicit_xpath(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_xpath(
            "//*[(@test='1')]").thenReturn(elements)
        result = finder.find("//*[(@test='1')]")
        self.assertEqual(result, elements)
        result = finder.find("//*[(@test='1')]", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_identifier(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        id_elements = self._make_mock_elements('div', 'a')
        name_elements = self._make_mock_elements('span', 'a')
        when(ctx._browser).find_elements_by_id("test1").thenReturn(
            list(id_elements)).thenReturn(list(id_elements))
        when(ctx._browser).find_elements_by_name("test1").thenReturn(
            list(name_elements)).thenReturn(list(name_elements))
        all_elements = list(id_elements)
        all_elements.extend(name_elements)
        result = finder.find("identifier=test1")
        self.assertEqual(result, all_elements)
        result = finder.find("identifier=test1", tag='a')
        self.assertEqual(result, [id_elements[1], name_elements[1]])

    def test_find_by_id(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_id("test1").thenReturn(elements)
        result = finder.find("id=test1")
        self.assertEqual(result, elements)
        result = finder.find("id=test1", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_name(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_name("test1").thenReturn(elements)
        result = finder.find("name=test1")
        self.assertEqual(result, elements)
        result = finder.find("name=test1", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_xpath(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_xpath(
            "//*[(@test='1')]").thenReturn(elements)
        result = finder.find("xpath=//*[(@test='1')]")
        self.assertEqual(result, elements)
        result = finder.find("xpath=//*[(@test='1')]", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_dom(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        elems = [elements[1], elements[3]]
        when(ctx._browser).execute_script(
            "return document.getElementsByTagName('a');").thenReturn(elems)
        result = finder.find("dom=document.getElementsByTagName('a')")
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_link_text(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_link_text(
            "my link").thenReturn(elements)
        result = finder.find("link=my link")
        self.assertEqual(result, elements)
        result = finder.find("link=my link", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_partial_link_text(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_partial_link_text(
            "my link").thenReturn(elements)
        result = finder.find("partial link=my link")
        self.assertEqual(result, elements)
        result = finder.find("partial link=my link", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_css_selector(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_css_selector(
            "#test1").thenReturn(elements)
        result = finder.find("css=#test1")
        self.assertEqual(result, elements)
        result = finder.find("css=#test1", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_class_names(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_class_name(
            "test1").thenReturn(elements)
        result = finder.find("class=test1")
        self.assertEqual(result, elements)
        result = finder.find("class=test1", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_tag_name(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_tag_name(
            "div").thenReturn(elements)
        result = finder.find("tag=div")
        self.assertEqual(result, elements)
        result = finder.find("tag=div", tag='a')
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_with_sloppy_prefix(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_id("test1").thenReturn(elements)
        when(ctx._browser).find_elements_by_partial_link_text(
            "test1").thenReturn(elements)
        result = finder.find("ID=test1")
        self.assertEqual(result, elements)
        result = finder.find("iD=test1")
        self.assertEqual(result, elements)
        result = finder.find("id=test1")
        self.assertEqual(result, elements)
        result = finder.find("  id =test1")
        self.assertEqual(result, elements)
        result = finder.find("  partiallink =test1")
        self.assertEqual(result, elements)
        result = finder.find("  p art iallin k =test1")
        self.assertEqual(result, elements)

    def test_find_with_sloppy_criteria(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(ctx._browser).find_elements_by_id("test1  ").thenReturn(elements)
        result = finder.find("id= test1  ")
        self.assertEqual(result, elements)

    def test_find_by_id_with_synonym_and_constraints(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        elements = self._make_mock_elements('div', 'input', 'span', 'input',
                                            'a', 'input', 'div', 'input')
        elements[1].set_attribute('type', 'radio')
        elements[3].set_attribute('type', 'checkbox')
        elements[5].set_attribute('type', 'text')
        elements[7].set_attribute('type', 'file')
        when(ctx._browser).find_elements_by_id("test1").thenReturn(elements)
        result = finder.find("id=test1")
        self.assertEqual(result, elements)
        result = finder.find("id=test1", tag='input')
        self.assertEqual(result, [elements[1], elements[3], elements[5],
                                  elements[7]])
        result = finder.find("id=test1", tag='radio button')
        self.assertEqual(result, [elements[1]])
        result = finder.find("id=test1", tag='checkbox')
        self.assertEqual(result, [elements[3]])
        result = finder.find("id=test1", tag='text field')
        self.assertEqual(result, [elements[5]])
        result = finder.find("id=test1", tag='file upload')
        self.assertEqual(result, [elements[7]])

    def test_find_returns_bad_values(self):
        ctx = mock()
        _browser = mock()
        ctx._browser = _browser
        finder = ElementFinder(ctx)
        # selenium.webdriver.ie.webdriver.WebDriver sometimes returns these
        for bad_value in (None, {'': None}):
            for func_name in ('find_elements_by_id', 'find_elements_by_name',
                              'find_elements_by_xpath', 'find_elements_by_link_text',
                              'find_elements_by_css_selector', 'find_elements_by_tag_name'):
                when_find_func = getattr(when(ctx._browser), func_name)
                when_find_func(any()).thenReturn(bad_value)
            for locator in ("identifier=it", "id=it", "name=it", "xpath=//div",
                            "link=it", "css=div.it", "tag=div", "default"):
                result = finder.find(locator)
                self.assertEqual(result, [])
                result = finder.find(locator, tag='div')
                self.assertEqual(result, [])

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

        def set_attribute(name, value):
            element.attributes[name] = value
        element.set_attribute = set_attribute

        def get_attribute(name):
            return element.attributes[name]
        element.get_attribute = get_attribute

        return element
