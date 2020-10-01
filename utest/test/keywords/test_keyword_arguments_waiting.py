import pytest
from mockito import mock, unstub, when

from SeleniumLibrary.keywords import WaitingKeywords

TIMEOUT = 0.01


@pytest.fixture(scope="module")
def waiting():
    ctx = mock()
    ctx.driver = mock()
    ctx.timeout = TIMEOUT
    return WaitingKeywords(ctx)


def teardown_module():
    unstub()


def test_wait_for_condition(waiting):
    condition = 'return document.getElementById("intro")'
    error = "did not become true"
    with pytest.raises(AssertionError) as error:
        waiting.wait_for_condition(condition)
    assert "did not become true" in str(error.value)

    with pytest.raises(AssertionError) as error:
        waiting.wait_for_condition(condition, None, "foobar")
    assert "foobar" in str(error.value)


def test_wait_until_page_contains(waiting):
    text = "text"
    when(waiting).is_text_present(text).thenReturn(None)
    with pytest.raises(AssertionError) as error:
        waiting.wait_until_page_contains(text)
    assert "Text 'text' did not" in str(error.value)

    with pytest.raises(AssertionError) as error:
        waiting.wait_until_page_contains(text, None, "error")
    assert "error" in str(error.value)
