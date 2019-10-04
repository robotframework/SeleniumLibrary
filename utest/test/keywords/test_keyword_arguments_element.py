import pytest
from mockito import mock, unstub, when

from SeleniumLibrary.keywords import ElementKeywords


@pytest.fixture(scope='function')
def element():
    ctx = mock()
    ctx._browser = mock()
    return ElementKeywords(ctx)


def teardown_function():
    unstub()


def test_locator_should_match_x_times(element):
    locator = '//div'
    when(element).find_elements(locator).thenReturn([])
    with pytest.raises(AssertionError) as error:
        element.locator_should_match_x_times(locator, 1)
    assert 'should have matched' in str(error.value)

    with pytest.raises(AssertionError) as error:
        element.locator_should_match_x_times(locator, 1, 'foobar')
    assert 'foobar' in str(error.value)


def test_element_text_should_be(element):
    locator = '//div'
    webelement = mock()
    webelement.text = 'text'
    when(element).find_element(locator).thenReturn(webelement)
    with pytest.raises(AssertionError) as error:
        element.element_text_should_be(locator, 'not text')
    assert 'should have been' in str(error.value)

    with pytest.raises(AssertionError) as error:
        element.element_text_should_be(locator, 'not text', 'foobar')
    assert 'foobar' in str(error.value)
