import pytest
from mockito import mock, unstub
from selenium.webdriver.common.keys import Keys

from SeleniumLibrary.keywords import ElementKeywords


@pytest.fixture(scope="module")
def element():
    ctx = mock()
    return ElementKeywords(ctx)


def teardown_module():
    unstub()


def test_parsing_one_modifier(element):
    parsed = element.parse_modifier("CTRL")
    assert parsed == [Keys.CONTROL]
    parsed = element.parse_modifier("esc")
    assert parsed == [Keys.ESCAPE]
    parsed = element.parse_modifier("ESCAPE")
    assert parsed == [Keys.ESCAPE]
    parsed = element.parse_modifier("control")
    assert parsed == [Keys.CONTROL]
    parsed = element.parse_modifier("alt")
    assert parsed == [Keys.ALT]
    parsed = element.parse_modifier("sHifT")
    assert parsed == [Keys.SHIFT]


def test_parsing_multiple_modifiers(element):
    parsed = element.parse_modifier("ctrl+shift")
    assert parsed == [Keys.CONTROL, Keys.SHIFT]
    parsed = element.parse_modifier("ctrl+alt+shift")
    assert parsed == [Keys.CONTROL, Keys.ALT, Keys.SHIFT]
    parsed = element.parse_modifier(" ctrl + alt +shift ")
    assert parsed == [Keys.CONTROL, Keys.ALT, Keys.SHIFT]


def test_invalid_modifier(element):
    with pytest.raises(ValueError, match="'FOO' modifier "):
        element.parse_modifier("FOO")

    with pytest.raises(ValueError, match="'FOO' modifier "):
        element.parse_modifier("FOO+CTRL")

    with pytest.raises(ValueError, match="'FOO' modifier "):
        element.parse_modifier("CTRL+FOO")

    with pytest.raises(ValueError, match="'CTRLFOO' modifier "):
        element.parse_modifier("CTRLFOO")


def test_invalid_key_separator(element):
    with pytest.raises(ValueError, match="'CTRL-CTRL' modifier "):
        element.parse_modifier("CTRL-CTRL")
