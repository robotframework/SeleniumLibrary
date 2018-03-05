import unittest

from mockito import when, mock, verify, verifyNoMoreInteractions, unstub
from selenium import webdriver

from SeleniumLibrary.keywords import BrowserManagementKeywords
from SeleniumLibrary.utils import SELENIUM_VERSION


class BrowserManagementTests(unittest.TestCase):

    def test_set_selenium_timeout_only_affects_open_browsers(self):
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
        unstub()

    def test_bad_browser_name(self):
        ctx = mock()
        bm = BrowserManagementKeywords(ctx)
        try:
            bm._make_driver("fireox")
            self.fail("Exception not raised")
        except ValueError as e:
            self.assertEquals(str(e), "fireox is not a supported browser.")

    def test_create_webdriver(self):
        ctx = mock()
        bm = BrowserManagementKeywords(ctx)
        FakeWebDriver = mock()
        driver = mock()
        when(FakeWebDriver).__call__(some_arg=1).thenReturn(driver)
        when(FakeWebDriver).__call__(some_arg=2).thenReturn(driver)
        when(ctx).register_driver(driver, 'fake1').thenReturn(0)
        webdriver.FakeWebDriver = FakeWebDriver
        try:
            index = bm.create_webdriver('FakeWebDriver', 'fake1', some_arg=1)
            verify(ctx).register_driver(driver, 'fake1')
            self.assertEqual(index, 0)
            my_kwargs = {'some_arg': 2}
            bm.create_webdriver('FakeWebDriver', 'fake2', kwargs=my_kwargs)
            verify(ctx).register_driver(driver, 'fake2')
        finally:
            del webdriver.FakeWebDriver
        unstub()

    def test_open_browser_speed(self):
        ctx = mock()
        ctx.speed = 5.0
        browser = mock()
        caps = webdriver.DesiredCapabilities.CHROME
        if SELENIUM_VERSION.major >= 3 and SELENIUM_VERSION.minor >= 8:
            when(webdriver).Chrome(desired_capabilities=caps,
                                   options=None).thenReturn(browser)
        else:
            when(webdriver).Chrome(desired_capabilities=caps).thenReturn(browser)
        bm = BrowserManagementKeywords(ctx)
        bm.open_browser('http://robotframework.org/', 'chrome')
        self.assertEqual(browser._speed, 5.0)
        unstub()

    def test_create_webdriver_speed(self):
        ctx = mock()
        ctx.speed = 0.0
        browser = mock()
        caps = webdriver.DesiredCapabilities.CHROME
        if SELENIUM_VERSION.major >= 3 and SELENIUM_VERSION.minor >= 8:
            when(webdriver).Chrome(desired_capabilities=caps,
                                   options=None).thenReturn(browser)
        else:
            when(webdriver).Chrome(desired_capabilities=caps).thenReturn(browser)
        bm = BrowserManagementKeywords(ctx)
        bm.open_browser('http://robotframework.org/', 'chrome')
        verify(browser, times=0).__call__('_speed')
        unstub()
