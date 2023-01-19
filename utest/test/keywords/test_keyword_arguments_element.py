import pytest
from mockito import mock, unstub, when, matchers
from SeleniumLibrary.keywords import ElementKeywords
import SeleniumLibrary.keywords.element as SUT


@pytest.fixture(scope="function")
def element():
    ctx = mock()
    ctx._browser = mock()
    ctx.action_chain_delay = 251
    return ElementKeywords(ctx)


def teardown_function():
    unstub()


def test_element_text_should_be(element):
    locator = "//div"
    webelement = mock()
    webelement.text = "text"
    when(element).find_element(locator).thenReturn(webelement)
    with pytest.raises(AssertionError) as error:
        element.element_text_should_be(locator, "not text")
    assert "should have been" in str(error.value)

    with pytest.raises(AssertionError) as error:
        element.element_text_should_be(locator, "not text", "foobar")
    assert "foobar" in str(error.value)



def test_action_chain_delay_in_elements(element):
    locator = "//div"
    webelement = mock()
    when(element).find_element(locator).thenReturn(webelement)

    chain_mock = mock()
    expected_delay_in_ms = 1000
    element.ctx.action_chain_delay = expected_delay_in_ms
    when(chain_mock).move_to_element(matchers.ANY).thenReturn(mock())
    when(SUT).ActionChains(matchers.ANY, duration=expected_delay_in_ms).thenReturn(chain_mock)
    element.scroll_element_into_view(locator)



