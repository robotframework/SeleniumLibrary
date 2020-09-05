import pytest
from selenium.common.exceptions import StaleElementReferenceException
from mockito import mock, when, unstub

from SeleniumLibrary.keywords import WaitingKeywords

TIMEOUT = 0.5


def _raise(*a):
    raise StaleElementReferenceException("Darn")


@pytest.fixture(scope="module")
def waiting():
    ctx = mock()
    ctx.timeout = TIMEOUT
    return WaitingKeywords(mock())


def teardown_module():
    unstub()


def test_wait_until_element_is_visible(waiting):
    locator = "//div"
    element = mock()
    when(waiting).find_element(locator, required=False).thenReturn(element)
    when(element).is_displayed().thenRaise(StaleElementReferenceException()).thenReturn(
        True
    )
    waiting.wait_until_element_is_visible(locator, TIMEOUT)


def test_wait_until_element_is_visible_fails(waiting):
    locator = "//div"
    element = mock()
    when(waiting).find_element(locator, required=False).thenReturn(element)
    when(element).is_displayed().thenRaise(StaleElementReferenceException("foo"))
    with pytest.raises(AssertionError) as error:
        waiting.wait_until_element_is_visible(locator, TIMEOUT)
    assert "Message: foo" in str(error.value)


def test_wait_until_element_is_not_visible(waiting):
    locator = "//div"
    element = mock()
    when(waiting).find_element(locator, required=False).thenReturn(element)
    when(element).is_displayed().thenRaise(StaleElementReferenceException()).thenReturn(
        False
    )
    waiting.wait_until_element_is_not_visible(locator, TIMEOUT)


def test_wait_until_element_is_enabled(waiting):
    locator = "//div"
    element = mock()
    when(waiting).find_element(locator, None).thenReturn(element)
    when(element).is_enabled().thenRaise(StaleElementReferenceException()).thenReturn(
        True
    )
    waiting.wait_until_element_is_enabled(locator, TIMEOUT)


def test_wait_until_element_is_enabled_get_attribute_readonly(waiting):
    locator = "//div"
    element = mock()
    when(waiting).find_element(locator, None).thenReturn(element)
    when(element).is_enabled().thenReturn(True)
    when(element).get_attribute("readonly").thenRaise(
        StaleElementReferenceException()
    ).thenReturn(None)
    waiting.wait_until_element_is_enabled(locator, TIMEOUT)


def test_wait_until_element_is_enabled_fails(waiting):
    locator = "//div"
    element = mock()
    when(waiting).find_element(locator, None).thenReturn(element)
    when(element).is_enabled().thenRaise(StaleElementReferenceException("foo"))
    with pytest.raises(AssertionError) as error:
        waiting.wait_until_element_is_enabled(locator, TIMEOUT)
    assert "Message: foo" in str(error.value)


def test_wait_until_element_contains(waiting):
    locator = "//div"
    text = "foo"
    element1, element2 = mock(), mock({"text": "foobar"})
    element1.__class__.text = property(_raise)
    when(waiting).find_element(locator).thenReturn(element1).thenReturn(element2)
    waiting.wait_until_element_contains(locator, text, TIMEOUT)


def test_wait_until_element_does_not_contain(waiting):
    locator = "//div"
    text = "foo"
    element1, element2 = mock(), mock({"text": "tidii"})
    element1.__class__.text = property(_raise)
    when(waiting).find_element(locator).thenReturn(element1).thenReturn(element2)
    waiting.wait_until_element_does_not_contain(locator, text, TIMEOUT)
