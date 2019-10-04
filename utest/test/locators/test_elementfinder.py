import pytest
from mockito import any, mock, verify, when, unstub

from SeleniumLibrary.errors import ElementNotFound
from SeleniumLibrary.locators.elementfinder import ElementFinder


@pytest.fixture(scope='function')
def finder():
    ctx = mock()
    ctx.driver = mock()
    return ElementFinder(ctx)


def teardown_function():
    unstub()


def test_implicit_xpath():
    _verify_parse_locator('//foo', 'xpath', '//foo')
    _verify_parse_locator('(//foo)', 'xpath', '(//foo)')
    _verify_parse_locator('//id=bar', 'xpath', '//id=bar')


def test_no_separator():
    _verify_parse_locator('foo', 'default', 'foo')
    _verify_parse_locator('', 'default', '')


def test_equal_sign_as_separator():
    _verify_parse_locator('class=foo', 'class', 'foo')
    _verify_parse_locator('id=foo=bar', 'id', 'foo=bar')


def test_colon_as_separator():
    _verify_parse_locator('class:foo', 'class', 'foo')
    _verify_parse_locator('id:foo:bar', 'id', 'foo:bar')


def test_use_first_separator_when_both_are_used():
    _verify_parse_locator('id:foo=bar', 'id', 'foo=bar')
    _verify_parse_locator('id=foo:bar', 'id', 'foo:bar')


def test_preserve_trailing_whitespace():
    _verify_parse_locator('//foo/bar  ', 'xpath', '//foo/bar  ')
    _verify_parse_locator('class=foo  ', 'class', 'foo  ')


def test_remove_whitespace_around_prefix_and_separator():
    _verify_parse_locator('class = foo', 'class', 'foo')
    _verify_parse_locator('class : foo', 'class', 'foo')
    _verify_parse_locator('  id  = foo = bar  ', 'id', 'foo = bar  ')
    _verify_parse_locator('  id  : foo : bar  ', 'id', 'foo : bar  ')


def test_separator_without_matching_prefix_is_ignored():
    _verify_parse_locator('no=match', 'default', 'no=match')
    _verify_parse_locator('no:match', 'default', 'no:match')


def test_registered_strategy_can_be_used_as_prefix():
    _verify_parse_locator('registered=no', 'default', 'registered=no')
    _verify_parse_locator('registered:no', 'default', 'registered:no')
    finder = ElementFinder(None)
    finder.register('registered', lambda *args: None, persist=True)
    _verify_parse_locator('registered=yes!!', 'registered', 'yes!!', finder)
    _verify_parse_locator('registered:yes!!', 'registered', 'yes!!', finder)


def _verify_parse_locator(locator, prefix, criteria, finder=None):
    if not finder:
        finder = ElementFinder(None)
    parse_locator = finder._parse_locator
    assert parse_locator(locator), (prefix, criteria)


def test_parent_is_not_webelement(finder):
    with pytest.raises(ValueError):
        finder.find("//div", parent='//button')


def test_find_by_xpath_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('//div').thenReturn(False)
    when(webelement).find_elements_by_xpath('//div').thenReturn([mock()])
    finder.find('//div', parent=webelement)
    verify(webelement).find_elements_by_xpath('//div')


def test_find_by_identifier_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('identifier=value').thenReturn(False)
    when(webelement).find_elements_by_id('value').thenReturn([mock()])
    when(webelement).find_elements_by_name('value').thenReturn([mock()])
    finder.find('identifier=value', parent=webelement)
    verify(webelement).find_elements_by_name('value')
    verify(webelement).find_elements_by_id('value')


def test_find_by_id_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('id=value').thenReturn(False)
    when(webelement).find_elements_by_id('value').thenReturn([mock()])
    finder.find('id=value', parent=webelement)
    verify(webelement).find_elements_by_id("value")


def test_find_by_name_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('name=value').thenReturn(False)
    when(webelement).find_elements_by_name('value').thenReturn([mock()])
    finder.find('name=value', parent=webelement)
    verify(webelement).find_elements_by_name("value")


def test_find_by_dom__parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('dom=value').thenReturn(False)
    when(finder)._disallow_webelement_parent(webelement).thenRaise(
        ValueError('This method does not allow webelement as parent'))
    with pytest.raises(ValueError) as error:
        finder.find('dom=value', parent=webelement)
    assert 'not allow webelement as parent' in str(error.value)


def test_find_by_sizzle_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('sizzle=div.class').thenReturn(False)
    when(finder)._disallow_webelement_parent(webelement).thenRaise(
        ValueError('This method does not allow webelement as parent'))
    with pytest.raises(ValueError) as error:
        finder.find('sizzle=div.class', parent=webelement)
    assert 'not allow webelement as parent' in str(error.value)


def test_find_by_link_text_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('link=My Link').thenReturn(False)
    when(webelement).find_elements_by_link_text(
        'My Link').thenReturn([mock()])
    finder.find('link=My Link', parent=webelement)
    verify(webelement).find_elements_by_link_text("My Link")


def test_find_by_partial_link_text_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('partial link=My L').thenReturn(False)
    when(webelement).find_elements_by_partial_link_text(
        'My L').thenReturn([mock()])
    finder.find('partial link=My L', parent=webelement)
    verify(webelement).find_elements_by_partial_link_text("My L")


def test_find_by_css_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('css=div').thenReturn(False)
    when(webelement).find_elements_by_css_selector(
        'div').thenReturn([mock()])
    finder.find('css=div', parent=webelement)
    verify(webelement).find_elements_by_css_selector("div")


def test_find_by_class_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('class=name').thenReturn(False)
    when(webelement).find_elements_by_class_name(
        'name').thenReturn([mock()])
    finder.find('class=name', parent=webelement)
    verify(webelement).find_elements_by_class_name("name")


def test_find_by_tag_name_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('tag=name').thenReturn(False)
    when(webelement).find_elements_by_tag_name(
        'name').thenReturn([mock()])
    finder.find('tag=name', parent=webelement)
    verify(webelement).find_elements_by_tag_name("name")


def test_find_sc_locator_parent_is_webelement(finder):
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('scLocator=div').thenReturn(False)
    when(finder)._disallow_webelement_parent(webelement).thenRaise(
        ValueError('This method does not allow webelement as parent'))
    with pytest.raises(ValueError) as error:
        finder.find('scLocator=div', parent=webelement)
    assert 'not allow webelement as parent' in str(error.value)


def test_find_by_default_parent_is_webelement(finder):
    xpath = "//*[(@id='name' or @name='name')]"
    webelement = mock()
    when(finder)._is_webelement(webelement).thenReturn(True)
    when(finder)._is_webelement('default=name').thenReturn(False)
    when(webelement).find_elements_by_xpath(
        xpath).thenReturn([mock()])
    finder.find('default=name', parent=webelement)
    verify(webelement).find_elements_by_xpath(xpath)


def test_non_existing_prefix(finder):
    with pytest.raises(ElementNotFound):
        finder.find("something=test1")

    with pytest.raises(ElementNotFound):
        finder.find("foo:bar")


def test_find_with_no_tag(finder):
    driver = _get_driver(finder)
    finder.find("test1", required=False)
    verify(driver).find_elements_by_xpath("//*[(@id='test1' or "
                                          "@name='test1')]")


def test_find_with_explicit_default_strategy(finder):
    driver = _get_driver(finder)
    finder.find("default=test1", required=False)
    verify(driver).find_elements_by_xpath("//*[(@id='test1' or "
                                          "@name='test1')]")


def test_find_with_explicit_default_strategy_and_equals(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("default=page.do?foo=bar", tag='a', required=False)
    verify(driver).find_elements_by_xpath(
        "//a[(@id='page.do?foo=bar' or @name='page.do?foo=bar' or "
        "@href='page.do?foo=bar' or "
        "normalize-space(descendant-or-self::text())='page.do?foo=bar' or "
        "@href='http://localhost/page.do?foo=bar')]")


def test_find_with_tag(finder):
    driver = _get_driver(finder)
    finder.find("test1", tag='div', required=False)
    verify(driver).find_elements_by_xpath(
        "//div[(@id='test1' or @name='test1')]")


def test_find_with_locator_with_apos(finder):
    driver = _get_driver(finder)
    finder.find("test '1'", required=False)
    verify(driver).find_elements_by_xpath(
        "//*[(@id=\"test '1'\" or @name=\"test '1'\")]")


def test_find_with_locator_with_quote(finder):
    driver = _get_driver(finder)
    finder.find("test \"1\"", required=False)
    verify(driver).find_elements_by_xpath(
        "//*[(@id='test \"1\"' or @name='test \"1\"')]")


def test_find_with_locator_with_quote_and_apos(finder):
    driver = _get_driver(finder)
    finder.find("test \"1\" and '2'", required=False)
    verify(driver).find_elements_by_xpath(
        "//*[(@id=concat('test \"1\" and ', \"'\", '2', \"'\", '') "
        "or @name=concat('test \"1\" and ', \"'\", '2', \"'\", ''))]")


def test_find_with_a(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='a', required=False)
    verify(driver).find_elements_by_xpath(
        "//a[(@id='test1' or @name='test1' or @href='test1' or "
        "normalize-space(descendant-or-self::text())='test1' or "
        "@href='http://localhost/test1')]")


def test_find_with_link_synonym(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='link', required=False)
    verify(driver).find_elements_by_xpath(
        "//a[(@id='test1' or @name='test1' or @href='test1' or "
        "normalize-space(descendant-or-self::text())='test1' or "
        "@href='http://localhost/test1')]")


def test_find_with_img(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='img', required=False)
    verify(driver).find_elements_by_xpath(
        "//img[(@id='test1' or @name='test1' or @src='test1' or "
        "@alt='test1' or @src='http://localhost/test1')]")


def test_find_with_image_synonym(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='image', required=False)
    verify(driver).find_elements_by_xpath(
        "//img[(@id='test1' or @name='test1' or @src='test1' or "
        "@alt='test1' or @src='http://localhost/test1')]")


def test_find_with_input(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='input', required=False)
    verify(driver).find_elements_by_xpath(
        "//input[(@id='test1' or @name='test1' or @value='test1' or "
        "@src='test1' or @src='http://localhost/test1')]")


def test_find_with_radio_button_synonym(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='radio button', required=False)
    verify(driver).find_elements_by_xpath(
        "//input[@type='radio' and (@id='test1' or @name='test1' or "
        "@value='test1' or @src='test1' or "
        "@src='http://localhost/test1')]")


def test_find_with_checkbox_synonym(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='checkbox', required=False)
    verify(driver).find_elements_by_xpath(
        "//input[@type='checkbox' and (@id='test1' or @name='test1' or "
        "@value='test1' or @src='test1' or "
        "@src='http://localhost/test1')]")


def test_find_with_file_upload_synonym(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='file upload', required=False)
    verify(driver).find_elements_by_xpath(
        "//input[@type='file' and (@id='test1' or @name='test1' or "
        "@value='test1' or @src='test1' or "
        "@src='http://localhost/test1')]")


def test_find_with_text_field_synonym(finder):
    driver = _get_driver(finder)
    driver.current_url = "http://localhost/mypage.html"
    finder.find("test1", tag='text field', required=False)
    verify(driver).find_elements_by_xpath(
        "//input[@type[. = 'date' or . = 'datetime-local' or . = 'email' or "
        ". = 'month' or . = 'number' or . = 'password' or . = 'search' or "
        ". = 'tel' or . = 'text' or . = 'time' or . = 'url' or . = 'week' or . = 'file'] and "
        "(@id='test1' or @name='test1' or @value='test1' or @src='test1' or "
        "@src='http://localhost/test1')]")


def test_find_with_button(finder):
    driver = _get_driver(finder)
    finder.find("test1", tag='button', required=False)
    verify(driver).find_elements_by_xpath(
        "//button[(@id='test1' or @name='test1' or @value='test1' or "
        "normalize-space(descendant-or-self::text())='test1')]")


def test_find_with_select(finder):
    driver = _get_driver(finder)
    finder.find("test1", tag='select', required=False)
    verify(driver).find_elements_by_xpath(
        "//select[(@id='test1' or @name='test1')]")


def test_find_with_list_synonym(finder):
    driver = _get_driver(finder)
    finder.find("test1", tag='list', required=False)
    verify(driver).find_elements_by_xpath(
        "//select[(@id='test1' or @name='test1')]")


def test_find_with_implicit_xpath(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_xpath(
        "//*[(@test='1')]").thenReturn(elements)
    result = finder.find("//*[(@test='1')]", first_only=False)
    assert result == elements

    result = finder.find("//*[(@test='1')]", tag='a',
                         first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_identifier(finder):
    driver = _get_driver(finder)
    id_elements = _make_mock_elements('div', 'a')
    name_elements = _make_mock_elements('span', 'a')
    when(driver).find_elements_by_id("test1").thenReturn(
        list(id_elements)).thenReturn(list(id_elements))
    when(driver).find_elements_by_name("test1").thenReturn(
        list(name_elements)).thenReturn(list(name_elements))
    all_elements = list(id_elements)
    all_elements.extend(name_elements)
    result = finder.find("identifier=test1", first_only=False)
    assert result == all_elements
    result = finder.find("identifier=test1", tag='a',
                         first_only=False)
    assert result == [id_elements[1], name_elements[1]]


def test_find_by_id(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_id("test1").thenReturn(
        elements)
    result = finder.find("id=test1", first_only=False)
    assert result == elements
    result = finder.find("id=test1", tag='a', first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_name(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_name("test1").thenReturn(elements)
    result = finder.find("name=test1", first_only=False)
    assert result == elements
    result = finder.find("name=test1", tag='a', first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_xpath(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_xpath(
        "//*[(@test='1')]").thenReturn(elements)
    result = finder.find("xpath=//*[(@test='1')]", first_only=False)
    assert result == elements
    result = finder.find("xpath=//*[(@test='1')]", tag='a',
                         first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_dom(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    elems = [elements[1], elements[3]]
    when(driver).execute_script(
        "return document.getElementsByTagName('a');").thenReturn(elems)
    result = finder.find("dom=document.getElementsByTagName('a')",
                         first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_link_text(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_link_text(
        "my link").thenReturn(elements)
    result = finder.find("link=my link", first_only=False)
    assert result == elements
    result = finder.find("link=my link", tag='a', first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_partial_link_text(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_partial_link_text(
        "my link").thenReturn(elements)
    result = finder.find("partial link=my link", first_only=False)
    assert result == elements
    result = finder.find("partial link=my link", tag='a',
                         first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_css_selector(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_css_selector(
        "#test1").thenReturn(elements)
    result = finder.find("css=#test1", first_only=False)
    assert result == elements
    result = finder.find("css=#test1", tag='a', first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_class_names(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_class_name(
        "test1").thenReturn(elements)
    result = finder.find("class=test1", first_only=False)
    assert result == elements
    result = finder.find("class=test1", tag='a', first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_by_tag_name(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_tag_name(
        "div").thenReturn(elements)
    result = finder.find("tag=div", first_only=False)
    assert result == elements
    result = finder.find("tag=div", tag='a', first_only=False)
    assert result == [elements[1], elements[3]]


def test_find_with_sloppy_prefix(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_id("test1").thenReturn(elements)
    when(driver).find_elements_by_partial_link_text(
        "test1").thenReturn(elements)
    result = finder.find("ID=test1", first_only=False)
    assert result == elements
    result = finder.find("iD=test1", first_only=False)
    assert result == elements
    result = finder.find("id=test1", first_only=False)
    assert result == elements
    result = finder.find("  id =test1", first_only=False)
    assert result == elements
    result = finder.find("  partiallink =test1", first_only=False)
    assert result == elements
    result = finder.find("  p art iallin k =test1", first_only=False)
    assert result == elements


def test_find_with_sloppy_criteria(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'a', 'span', 'a')
    when(driver).find_elements_by_id("test1  ").thenReturn(elements)
    result = finder.find("id= test1  ", first_only=False)
    assert result == elements


def test_find_by_id_with_synonym_and_constraints(finder):
    driver = _get_driver(finder)
    elements = _make_mock_elements('div', 'input', 'span', 'input',
                                        'a', 'input', 'div', 'input',
                                        'input')
    elements[1].set_attribute('type', 'radio')
    elements[3].set_attribute('type', 'checkbox')
    elements[5].set_attribute('type', 'text')
    elements[7].set_attribute('type', 'file')
    elements[8].set_attribute('type', 'email')
    when(driver).find_elements_by_id("test1").thenReturn(elements)
    result = finder.find("id=test1", first_only=False)
    assert result == elements
    result = finder.find("id=test1", tag='input', first_only=False)
    assert result == [elements[1], elements[3], elements[5],
                      elements[7], elements[8]]
    result = finder.find("id=test1", tag='radio button',
                         first_only=False)
    assert result == [elements[1]]
    result = finder.find("id=test1", tag='checkbox', first_only=False)
    assert result == [elements[3]]
    result = finder.find("id=test1", tag='text field',
                         first_only=False)
    assert result == [elements[5], elements[7], elements[8]]
    result = finder.find("id=test1", tag='file upload',
                         first_only=False)
    assert result == [elements[7]]


def test_find_returns_bad_values(finder):
    # selenium.webdriver.ie.webdriver.WebDriver sometimes returns these
    # and ChromeDriver has also returned None:
    # https://github.com/SeleniumHQ/selenium/issues/4555
    driver = _get_driver(finder)
    locators = ('find_elements_by_id', 'find_elements_by_name',
                'find_elements_by_xpath', 'find_elements_by_link_text',
                'find_elements_by_css_selector',
                'find_elements_by_tag_name')
    for bad_value in (None, {'': None}):
        for func_name in locators:
            when_find_func = getattr(when(driver), func_name)
            when_find_func(any()).thenReturn(bad_value)
        for locator in ("identifier=it", "id=it", "name=it", "xpath=//div",
                        "link=it", "css=div.it", "tag=div", "default"):
            result = finder.find(locator, required=False,
                                 first_only=False)
            assert result == []
            result = finder.find(locator, tag='div', required=False,
                                 first_only=False)
            assert result == []


def _make_mock_elements(*tags):
    elements = []
    for tag in tags:
        element = _make_mock_element(tag)
        elements.append(element)
    return elements


def _make_mock_element(tag):
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


def _get_driver(finder):
    return finder.ctx.driver
