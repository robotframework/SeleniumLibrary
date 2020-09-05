import pytest
from mockito import mock, unstub, when

from SeleniumLibrary.keywords import FormElementKeywords


FALSES = ["False", False, "", None, "NONE"]


@pytest.fixture(scope="function")
def form():
    ctx = mock()
    ctx.driver = mock()
    return FormElementKeywords(ctx)


def teardown_function():
    unstub()


def test_submit_form_false(form):
    element = mock()
    when(form).find_element("tag:form", tag="form").thenReturn(element)
    for false in FALSES:
        form.submit_form()
    form.submit_form()


def test_submit_form_true(form):
    element = mock()
    when(form).find_element("//form", tag="form").thenReturn(element)
    form.submit_form("//form")


def test_textfield_should_contain(form):
    locator = "//input"
    element = mock()
    when(form).find_element(locator, "text field").thenReturn(element)
    when(element).get_attribute("value").thenReturn("no")
    with pytest.raises(AssertionError) as error:
        form.textfield_should_contain(locator, "text")
    assert "should have contained" in str(error.value)

    with pytest.raises(AssertionError) as error:
        form.textfield_should_contain(locator, "text", "foobar")
    assert "foobar" in str(error.value)


def test_textfield_value_should_be(form):
    locator = "//input"
    element = mock()
    when(form).find_element(locator, "text field").thenReturn(element)
    when(element).get_attribute("value").thenReturn("no")
    with pytest.raises(AssertionError) as error:
        form.textfield_value_should_be(locator, "value")
    assert "text field" in str(error.value)

    with pytest.raises(AssertionError) as error:
        form.textfield_value_should_be(locator, "value", "foobar err")
    assert "foobar" in str(error.value)


def test_textarea_should_contain(form):
    locator = "//input"
    element = mock()
    when(form).find_element(locator, "text area").thenReturn(element)
    when(element).get_attribute("value").thenReturn("no")
    with pytest.raises(AssertionError) as error:
        form.textarea_should_contain(locator, "value")
    assert "should have contained" in str(error.value)

    with pytest.raises(AssertionError) as error:
        form.textarea_should_contain(locator, "value", "foobar error")
    assert "foobar error" in str(error.value)


def test_textarea_value_should_be(form):
    locator = "//input"
    element = mock()
    when(form).find_element(locator, "text area").thenReturn(element)
    when(element).get_attribute("value").thenReturn("no")
    with pytest.raises(AssertionError) as error:
        form.textarea_value_should_be(locator, "value")
    assert "should have had" in str(error.value)

    with pytest.raises(AssertionError) as error:
        form.textarea_value_should_be(locator, "value", "foobar")
    assert "foobar" in str(error.value)
