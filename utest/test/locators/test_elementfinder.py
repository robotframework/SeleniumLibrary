import unittest

from mockito import any, mock, verify, when, unstub

from SeleniumLibrary.errors import ElementNotFound
from SeleniumLibrary.locators.elementfinder import ElementFinder


class ParseLocatorTests(unittest.TestCase):

    def setUp(self):
        self.finder = ElementFinder(None)

    def test_implicit_xpath(self):
        self._verify_parse_locator('//foo', 'xpath', '//foo')
        self._verify_parse_locator('(//foo)', 'xpath', '(//foo)')
        self._verify_parse_locator('//id=bar', 'xpath', '//id=bar')

    def test_no_separator(self):
        self._verify_parse_locator('foo', 'default', 'foo')
        self._verify_parse_locator('', 'default', '')

    def test_equal_sign_as_separator(self):
        self._verify_parse_locator('class=foo', 'class', 'foo')
        self._verify_parse_locator('id=foo=bar', 'id', 'foo=bar')

    def test_colon_as_separator(self):
        self._verify_parse_locator('class:foo', 'class', 'foo')
        self._verify_parse_locator('id:foo:bar', 'id', 'foo:bar')

    def test_use_first_separator_when_both_are_used(self):
        self._verify_parse_locator('id:foo=bar', 'id', 'foo=bar')
        self._verify_parse_locator('id=foo:bar', 'id', 'foo:bar')

    def test_preserve_trailing_whitespace(self):
        self._verify_parse_locator('//foo/bar  ', 'xpath', '//foo/bar  ')
        self._verify_parse_locator('class=foo  ', 'class', 'foo  ')

    def test_remove_whitespace_around_prefix_and_separator(self):
        self._verify_parse_locator('class = foo', 'class', 'foo')
        self._verify_parse_locator('class : foo', 'class', 'foo')
        self._verify_parse_locator('  id  = foo = bar  ', 'id', 'foo = bar  ')
        self._verify_parse_locator('  id  : foo : bar  ', 'id', 'foo : bar  ')

    def test_separator_without_matching_prefix_is_ignored(self):
        self._verify_parse_locator('no=match', 'default', 'no=match')
        self._verify_parse_locator('no:match', 'default', 'no:match')

    def test_registered_strategy_can_be_used_as_prefix(self):
        self._verify_parse_locator('registered=no', 'default', 'registered=no')
        self._verify_parse_locator('registered:no', 'default', 'registered:no')
        self.finder.register('registered', lambda *args: None, persist=True)
        self._verify_parse_locator('registered=yes!!', 'registered', 'yes!!')
        self._verify_parse_locator('registered:yes!!', 'registered', 'yes!!')

    def _verify_parse_locator(self, locator, prefix, criteria):
        parse_locator = self.finder._parse_locator
        self.assertEqual(parse_locator(locator), (prefix, criteria))


class ElementFinderParentTests(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self.ctx.driver = self.driver = mock()
        self.finder = ElementFinder(self.ctx)

    def tearDown(self):
        unstub()

    def test_parent_is_not_webelement(self):
        with self.assertRaises(ValueError):
            self.finder.find("//div", parent='//button')

    def test_find_by_xpath_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('//div').thenReturn(False)
        when(webelement).find_elements_by_xpath('//div').thenReturn([mock()])
        self.finder.find('//div', parent=webelement)
        verify(webelement).find_elements_by_xpath('//div')

    def test_find_by_identifier_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('identifier=value').thenReturn(False)
        when(webelement).find_elements_by_id('value').thenReturn([mock()])
        when(webelement).find_elements_by_name('value').thenReturn([mock()])
        self.finder.find('identifier=value', parent=webelement)
        verify(webelement).find_elements_by_name('value')
        verify(webelement).find_elements_by_id('value')

    def test_find_by_id_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('id=value').thenReturn(False)
        when(webelement).find_elements_by_id('value').thenReturn([mock()])
        self.finder.find('id=value', parent=webelement)
        verify(webelement).find_elements_by_id("value")

    def test_find_by_name_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('name=value').thenReturn(False)
        when(webelement).find_elements_by_name('value').thenReturn([mock()])
        self.finder.find('name=value', parent=webelement)
        verify(webelement).find_elements_by_name("value")

    def test_find_by_dom__parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('dom=value').thenReturn(False)
        when(self.finder)._disallow_webelement_parent(webelement).thenRaise(
            ValueError('This method does not allow webelement as parent'))
        with self.assertRaisesRegexp(ValueError, 'not allow webelement as parent'):
            self.finder.find('dom=value', parent=webelement)

    def test_find_by_sizzle_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('sizzle=div.class').thenReturn(False)
        when(self.finder)._disallow_webelement_parent(webelement).thenRaise(
            ValueError('This method does not allow webelement as parent'))
        with self.assertRaisesRegexp(ValueError, 'not allow webelement as parent'):
            self.finder.find('sizzle=div.class', parent=webelement)

    def test_find_by_link_text_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('link=My Link').thenReturn(False)
        when(webelement).find_elements_by_link_text(
            'My Link').thenReturn([mock()])
        self.finder.find('link=My Link', parent=webelement)
        verify(webelement).find_elements_by_link_text("My Link")

    def test_find_by_partial_link_text_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('partial link=My L').thenReturn(False)
        when(webelement).find_elements_by_partial_link_text(
            'My L').thenReturn([mock()])
        self.finder.find('partial link=My L', parent=webelement)
        verify(webelement).find_elements_by_partial_link_text("My L")

    def test_find_by_css_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('css=div').thenReturn(False)
        when(webelement).find_elements_by_css_selector(
            'div').thenReturn([mock()])
        self.finder.find('css=div', parent=webelement)
        verify(webelement).find_elements_by_css_selector("div")

    def test_find_by_class_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('class=name').thenReturn(False)
        when(webelement).find_elements_by_class_name(
            'name').thenReturn([mock()])
        self.finder.find('class=name', parent=webelement)
        verify(webelement).find_elements_by_class_name("name")

    def test_find_by_tag_name_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('tag=name').thenReturn(False)
        when(webelement).find_elements_by_tag_name(
            'name').thenReturn([mock()])
        self.finder.find('tag=name', parent=webelement)
        verify(webelement).find_elements_by_tag_name("name")

    def test_find_sc_locator_parent_is_webelement(self):
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('scLocator=div').thenReturn(False)
        when(self.finder)._disallow_webelement_parent(webelement).thenRaise(
            ValueError('This method does not allow webelement as parent'))
        with self.assertRaisesRegexp(ValueError, 'not allow webelement as parent'):
            self.finder.find('scLocator=div', parent=webelement)

    def test_find_by_default_parent_is_webelement(self):
        xpath = "//*[(@id='name' or @name='name')]"
        webelement = mock()
        when(self.finder)._is_webelement(webelement).thenReturn(True)
        when(self.finder)._is_webelement('default=name').thenReturn(False)
        when(webelement).find_elements_by_xpath(
            xpath).thenReturn([mock()])
        self.finder.find('default=name', parent=webelement)
        verify(webelement).find_elements_by_xpath(xpath)


class ElementFinderTests(unittest.TestCase):

    def setUp(self):
        self.ctx = mock()
        self.ctx.driver = self.driver = mock()
        self.finder = ElementFinder(self.ctx)

    def tearDown(self):
        unstub()

    def test_non_existing_prefix(self):
        with self.assertRaises(ElementNotFound):
            self.finder.find("something=test1")
        with self.assertRaises(ElementNotFound):
            self.finder.find("foo:bar")

    def test_find_with_no_tag(self):
        self.finder.find("test1", required=False)
        verify(self.driver).find_elements_by_xpath("//*[(@id='test1' or "
                                                         "@name='test1')]")

    def test_find_with_explicit_default_strategy(self):
        self.finder.find("default=test1", required=False)
        verify(self.driver).find_elements_by_xpath("//*[(@id='test1' or "
                                                         "@name='test1')]")

    def test_find_with_explicit_default_strategy_and_equals(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("default=page.do?foo=bar", tag='a', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//a[(@id='page.do?foo=bar' or @name='page.do?foo=bar' or "
            "@href='page.do?foo=bar' or "
            "normalize-space(descendant-or-self::text())='page.do?foo=bar' or "
            "@href='http://localhost/page.do?foo=bar')]")

    def test_find_with_tag(self):
        self.finder.find("test1", tag='div', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//div[(@id='test1' or @name='test1')]")

    def test_find_with_locator_with_apos(self):
        self.finder.find("test '1'", required=False)
        verify(self.driver).find_elements_by_xpath(
            "//*[(@id=\"test '1'\" or @name=\"test '1'\")]")

    def test_find_with_locator_with_quote(self):
        self.finder.find("test \"1\"", required=False)
        verify(self.driver).find_elements_by_xpath(
            "//*[(@id='test \"1\"' or @name='test \"1\"')]")

    def test_find_with_locator_with_quote_and_apos(self):
        self.finder.find("test \"1\" and '2'", required=False)
        verify(self.driver).find_elements_by_xpath(
            "//*[(@id=concat('test \"1\" and ', \"'\", '2', \"'\", '') "
            "or @name=concat('test \"1\" and ', \"'\", '2', \"'\", ''))]")

    def test_find_with_a(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='a', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//a[(@id='test1' or @name='test1' or @href='test1' or "
            "normalize-space(descendant-or-self::text())='test1' or "
            "@href='http://localhost/test1')]")

    def test_find_with_link_synonym(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='link', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//a[(@id='test1' or @name='test1' or @href='test1' or "
            "normalize-space(descendant-or-self::text())='test1' or "
            "@href='http://localhost/test1')]")

    def test_find_with_img(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='img', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//img[(@id='test1' or @name='test1' or @src='test1' or "
            "@alt='test1' or @src='http://localhost/test1')]")

    def test_find_with_image_synonym(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='image', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//img[(@id='test1' or @name='test1' or @src='test1' or "
            "@alt='test1' or @src='http://localhost/test1')]")

    def test_find_with_input(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='input', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//input[(@id='test1' or @name='test1' or @value='test1' or "
            "@src='test1' or @src='http://localhost/test1')]")

    def test_find_with_radio_button_synonym(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='radio button', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//input[@type='radio' and (@id='test1' or @name='test1' or "
            "@value='test1' or @src='test1' or "
            "@src='http://localhost/test1')]")

    def test_find_with_checkbox_synonym(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='checkbox', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//input[@type='checkbox' and (@id='test1' or @name='test1' or "
            "@value='test1' or @src='test1' or "
            "@src='http://localhost/test1')]")

    def test_find_with_file_upload_synonym(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='file upload', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//input[@type='file' and (@id='test1' or @name='test1' or "
            "@value='test1' or @src='test1' or "
            "@src='http://localhost/test1')]")

    def test_find_with_text_field_synonym(self):
        self.driver.current_url = "http://localhost/mypage.html"
        self.finder.find("test1", tag='text field', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//input[@type[. = 'date' or . = 'datetime-local' or . = 'email' or "
            ". = 'month' or . = 'number' or . = 'password' or . = 'search' or "
            ". = 'tel' or . = 'text' or . = 'time' or . = 'url' or . = 'week' or . = 'file'] and "
            "(@id='test1' or @name='test1' or @value='test1' or @src='test1' or "
            "@src='http://localhost/test1')]")

    def test_find_with_button(self):
        self.finder.find("test1", tag='button', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//button[(@id='test1' or @name='test1' or @value='test1' or "
            "normalize-space(descendant-or-self::text())='test1')]")

    def test_find_with_select(self):
        self.finder.find("test1", tag='select', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//select[(@id='test1' or @name='test1')]")

    def test_find_with_list_synonym(self):
        self.finder.find("test1", tag='list', required=False)
        verify(self.driver).find_elements_by_xpath(
            "//select[(@id='test1' or @name='test1')]")

    def test_find_with_implicit_xpath(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_xpath(
            "//*[(@test='1')]").thenReturn(elements)
        result = self.finder.find("//*[(@test='1')]", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("//*[(@test='1')]", tag='a',
                                  first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_identifier(self):
        id_elements = self._make_mock_elements('div', 'a')
        name_elements = self._make_mock_elements('span', 'a')
        when(self.driver).find_elements_by_id("test1").thenReturn(
            list(id_elements)).thenReturn(list(id_elements))
        when(self.driver).find_elements_by_name("test1").thenReturn(
            list(name_elements)).thenReturn(list(name_elements))
        all_elements = list(id_elements)
        all_elements.extend(name_elements)
        result = self.finder.find("identifier=test1", first_only=False)
        self.assertEqual(result, all_elements)
        result = self.finder.find("identifier=test1", tag='a',
                                  first_only=False)
        self.assertEqual(result, [id_elements[1], name_elements[1]])

    def test_find_by_id(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_id("test1").thenReturn(
            elements)
        result = self.finder.find("id=test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("id=test1", tag='a', first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_name(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_name("test1").thenReturn(
            elements)
        result = self.finder.find("name=test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("name=test1", tag='a', first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_xpath(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_xpath(
            "//*[(@test='1')]").thenReturn(elements)
        result = self.finder.find("xpath=//*[(@test='1')]", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("xpath=//*[(@test='1')]", tag='a',
                                  first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_dom(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        elems = [elements[1], elements[3]]
        when(self.driver).execute_script(
            "return document.getElementsByTagName('a');").thenReturn(elems)
        result = self.finder.find("dom=document.getElementsByTagName('a')",
                                  first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_link_text(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_link_text(
            "my link").thenReturn(elements)
        result = self.finder.find("link=my link", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("link=my link", tag='a', first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_partial_link_text(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_partial_link_text(
            "my link").thenReturn(elements)
        result = self.finder.find("partial link=my link", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("partial link=my link", tag='a',
                                  first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_css_selector(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_css_selector(
            "#test1").thenReturn(elements)
        result = self.finder.find("css=#test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("css=#test1", tag='a', first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_class_names(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_class_name(
            "test1").thenReturn(elements)
        result = self.finder.find("class=test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("class=test1", tag='a', first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_by_tag_name(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_tag_name(
            "div").thenReturn(elements)
        result = self.finder.find("tag=div", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("tag=div", tag='a', first_only=False)
        self.assertEqual(result, [elements[1], elements[3]])

    def test_find_with_sloppy_prefix(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_id("test1").thenReturn(
            elements)
        when(self.driver).find_elements_by_partial_link_text(
            "test1").thenReturn(elements)
        result = self.finder.find("ID=test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("iD=test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("id=test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("  id =test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("  partiallink =test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("  p art iallin k =test1", first_only=False)
        self.assertEqual(result, elements)

    def test_find_with_sloppy_criteria(self):
        elements = self._make_mock_elements('div', 'a', 'span', 'a')
        when(self.driver).find_elements_by_id("test1  ").thenReturn(
            elements)
        result = self.finder.find("id= test1  ", first_only=False)
        self.assertEqual(result, elements)

    def test_find_by_id_with_synonym_and_constraints(self):
        elements = self._make_mock_elements('div', 'input', 'span', 'input',
                                            'a', 'input', 'div', 'input',
                                            'input')
        elements[1].set_attribute('type', 'radio')
        elements[3].set_attribute('type', 'checkbox')
        elements[5].set_attribute('type', 'text')
        elements[7].set_attribute('type', 'file')
        elements[8].set_attribute('type', 'email')
        when(self.driver).find_elements_by_id("test1").thenReturn(
            elements)
        result = self.finder.find("id=test1", first_only=False)
        self.assertEqual(result, elements)
        result = self.finder.find("id=test1", tag='input', first_only=False)
        self.assertEqual(result, [elements[1], elements[3], elements[5],
                                  elements[7], elements[8]])
        result = self.finder.find("id=test1", tag='radio button',
                                  first_only=False)
        self.assertEqual(result, [elements[1]])
        result = self.finder.find("id=test1", tag='checkbox', first_only=False)
        self.assertEqual(result, [elements[3]])
        result = self.finder.find("id=test1", tag='text field',
                                  first_only=False)
        self.assertEqual(result, [elements[5], elements[7], elements[8]])
        result = self.finder.find("id=test1", tag='file upload',
                                  first_only=False)
        self.assertEqual(result, [elements[7]])

    def test_find_returns_bad_values(self):
        # selenium.webdriver.ie.webdriver.WebDriver sometimes returns these
        # and ChromeDriver has also returned None:
        # https://github.com/SeleniumHQ/selenium/issues/4555
        locators = ('find_elements_by_id', 'find_elements_by_name',
                    'find_elements_by_xpath', 'find_elements_by_link_text',
                    'find_elements_by_css_selector',
                    'find_elements_by_tag_name')
        for bad_value in (None, {'': None}):
            for func_name in locators:
                when_find_func = getattr(when(self.driver), func_name)
                when_find_func(any()).thenReturn(bad_value)
            for locator in ("identifier=it", "id=it", "name=it", "xpath=//div",
                            "link=it", "css=div.it", "tag=div", "default"):
                result = self.finder.find(locator, required=False,
                                          first_only=False)
                self.assertEqual(result, [])
                result = self.finder.find(locator, tag='div', required=False,
                                          first_only=False)
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
