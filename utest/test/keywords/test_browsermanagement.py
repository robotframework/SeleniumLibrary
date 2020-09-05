import pytest
from mockito import when, mock, verify, verifyNoMoreInteractions, ANY
from selenium import webdriver

from SeleniumLibrary.keywords import BrowserManagementKeywords
from SeleniumLibrary import SeleniumLibrary


def test_set_selenium_timeout_only_affects_open_browsers():
    ctx = mock()
    ctx.timeout = 5.0
    _drivers = mock()
    ctx._drivers = _drivers
    first_browser, second_browser = mock(), mock()
    ctx._drivers.active_drivers = [first_browser, second_browser]
    bm = BrowserManagementKeywords(ctx)
    bm.set_selenium_timeout("10 seconds")
    verify(first_browser).set_script_timeout(10.0)
    verify(second_browser).set_script_timeout(10.0)
    ctx._drivers.active_drivers = []
    bm.set_selenium_timeout("20 seconds")
    verifyNoMoreInteractions(first_browser)
    verifyNoMoreInteractions(second_browser)


def test_selenium_implicit_wait_default():
    sl = SeleniumLibrary()
    assert sl.implicit_wait == 0.0, "Wait should have 0.0"


def test_set_selenium_implicit_wait():
    sl = SeleniumLibrary()
    sl.set_selenium_implicit_wait("5.0")
    assert sl.implicit_wait == 5.0

    sl.set_selenium_implicit_wait("1 min")
    assert sl.implicit_wait == 60.0


def test_selenium_implicit_wait_error():
    with pytest.raises(ValueError):
        SeleniumLibrary(implicit_wait="False")
    sl = SeleniumLibrary(implicit_wait="3")
    with pytest.raises(ValueError):
        sl.set_selenium_implicit_wait("1 vuosi")


def test_selenium_implicit_wait_get():
    sl = SeleniumLibrary(implicit_wait="3")
    assert sl.get_selenium_implicit_wait() == "3 seconds"

    org_value = sl.set_selenium_implicit_wait("1 min")
    assert sl.get_selenium_implicit_wait() == "1 minute"
    assert org_value == "3 seconds"


def test_bad_browser_name():
    ctx = mock()
    bm = BrowserManagementKeywords(ctx)
    try:
        bm._make_driver("fireox")
        raise ValueError("Exception not raised")
    except ValueError as e:
        assert str(e) == "fireox is not a supported browser."


def test_create_webdriver():
    ctx = mock()
    ctx.event_firing_webdriver = None
    bm = BrowserManagementKeywords(ctx)
    FakeWebDriver = mock()
    driver = mock()
    when(FakeWebDriver).__call__(some_arg=1).thenReturn(driver)
    when(FakeWebDriver).__call__(some_arg=2).thenReturn(driver)
    when(ctx).register_driver(driver, "fake1").thenReturn(0)
    webdriver.FakeWebDriver = FakeWebDriver
    try:
        index = bm.create_webdriver("FakeWebDriver", "fake1", some_arg=1)
        verify(ctx).register_driver(driver, "fake1")
        assert index == 0
        my_kwargs = {"some_arg": 2}
        bm.create_webdriver("FakeWebDriver", "fake2", kwargs=my_kwargs)
        verify(ctx).register_driver(driver, "fake2")
    finally:
        del webdriver.FakeWebDriver


def test_open_browser_speed():
    ctx = mock()
    ctx._drivers = mock()
    ctx.event_firing_webdriver = None
    ctx.speed = 5.0
    browser = mock()
    executable_path = "chromedriver"
    when(webdriver).Chrome(
        options=None, service_log_path=None, executable_path=executable_path
    ).thenReturn(browser)
    bm = BrowserManagementKeywords(ctx)
    when(bm._webdriver_creator)._get_executable_path(ANY).thenReturn(executable_path)
    bm.open_browser("http://robotframework.org/", "chrome")
    assert browser._speed == 5.0


def test_create_webdriver_speed():
    ctx = mock()
    ctx._drivers = mock()
    ctx.event_firing_webdriver = None
    ctx.speed = 0.0
    browser = mock()
    executable_path = "chromedriver"
    when(webdriver).Chrome(
        options=None, service_log_path=None, executable_path=executable_path
    ).thenReturn(browser)
    bm = BrowserManagementKeywords(ctx)
    when(bm._webdriver_creator)._get_executable_path(ANY).thenReturn(executable_path)
    bm.open_browser("http://robotframework.org/", "chrome")
    verify(browser, times=0).__call__("_speed")
