import unittest

from mockito import when, mock, verify, verifyNoMoreInteractions, unstub
from selenium import webdriver

from Selenium2Library.keywords.browsermanagement import BrowserManagementKeywords


class BrowserManagementTests(unittest.TestCase):

    def test_create_firefox_browser(self):
        test_browsers = (
            (webdriver.Firefox, "ff"),
            (webdriver.Firefox, "firEfOx")
        )

        for test_browser in test_browsers:
            self.verify_browser(*test_browser)

    def test_create_ie_browser(self):
        test_browsers = (
            (webdriver.Ie, "ie"),
            (webdriver.Ie, "Internet Explorer")
        )

        for test_browser in test_browsers:
            self.verify_browser(*test_browser)

    def test_create_chrome_browser(self):
        test_browsers = (
            (webdriver.Chrome, "gOOglEchrOmE"),
            (webdriver.Chrome, "gc"),
            (webdriver.Chrome, "chrome")
        )

        for test_browser in test_browsers:
            self.verify_browser(*test_browser)

    def test_create_opera_browser(self):
        self.verify_browser(webdriver.Opera, "OPERA")

    def test_create_phantomjs_browser(self):
        self.verify_browser(webdriver.PhantomJS, "PHANTOMJS")

    def test_create_remote_browser(self):
        self.verify_browser(
            webdriver.Remote, "chrome", remote="http://127.0.0.1/wd/hub"
        )

    def test_create_htmlunit_browser(self):
        self.verify_browser(webdriver.Remote, "htmlunit")

    def test_create_htmlunitwihtjs_browser(self):
        self.verify_browser(webdriver.Remote, "htmlunitwithjs")

    def test_parse_capabilities_string(self):
        ctx = mock()
        bm = BrowserManagementKeywords(ctx)
        expected_caps = "key1:val1,key2:val2"
        capabilities = bm._parse_capabilities_string(expected_caps)
        self.assertTrue("val1", capabilities["key1"])
        self.assertTrue("val2", capabilities["key2"])
        self.assertTrue(2, len(capabilities))
        unstub()

    def test_parse_complex_capabilities_string(self):
        ctx = mock()
        bm = BrowserManagementKeywords(ctx)
        expected_caps = "proxyType:manual,httpProxy:IP:port"
        capabilities = bm._parse_capabilities_string(expected_caps)
        self.assertTrue("manual", capabilities["proxyType"])
        self.assertTrue("IP:port", capabilities["httpProxy"])
        self.assertTrue(2, len(capabilities))
        unstub()

    def test_create_remote_browser_with_desired_prefs(self):
        expected_caps = {"key1": "val1", "key2": "val2"}
        self.verify_browser(
            webdriver.Remote, "chrome", remote="http://127.0.0.1/wd/hub",
            desired_capabilities=expected_caps
        )

    def test_create_remote_browser_with_string_desired_prefs(self):
        expected_caps = "key1:val1,key2:val2"
        self.verify_browser(
            webdriver.Remote, "chrome", remote="http://127.0.0.1/wd/hub",
            desired_capabilities=expected_caps)

    def test_capabilities_attribute_not_modified(self):
        expected_caps = {"some_cap": "42"}
        self.verify_browser(
            webdriver.Remote, "chrome", remote="http://127.0.0.1/wd/hub",
            desired_capabilities=expected_caps
        )
        self.assertFalse("some_cap" in webdriver.DesiredCapabilities.CHROME)

    def test_set_selenium_timeout_only_affects_open_browsers(self):
        ctx = mock()
        ctx._timeout_in_secs = 5.0
        _browsers = mock()
        ctx._browsers = _browsers
        first_browser, second_browser = mock(), mock()
        when(_browsers).get_open_browsers().thenReturn(
            [first_browser, second_browser]
        )
        bm = BrowserManagementKeywords(ctx)
        bm.set_selenium_timeout("10 seconds")
        verify(first_browser).set_script_timeout(10.0)
        verify(second_browser).set_script_timeout(10.0)
        when(_browsers).get_open_browsers().thenReturn(
            []
        )
        bm.set_selenium_timeout("20 seconds")
        verifyNoMoreInteractions(first_browser)
        verifyNoMoreInteractions(second_browser)
        unstub()

    def test_bad_browser_name(self):
        ctx = mock()
        bm = BrowserManagementKeywords(ctx)
        try:
            bm._make_browser("fireox")
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
        when(ctx).register_browser(driver, 'fake1').thenReturn(0)
        webdriver.FakeWebDriver = FakeWebDriver
        try:
            index = bm.create_webdriver('FakeWebDriver', 'fake1', some_arg=1)
            verify(ctx).register_browser(driver, 'fake1')
            self.assertEqual(index, 0)
            my_kwargs = {'some_arg': 2}
            bm.create_webdriver('FakeWebDriver', 'fake2', kwargs=my_kwargs)
            verify(ctx).register_browser(driver, 'fake2')
        finally:
            del webdriver.FakeWebDriver
        unstub()

    def verify_browser(self, webdriver_type, browser_name, **kw):
        # todo try lambda *x: was_called = true
        ctx = mock()
        bm = BrowserManagementKeywords(ctx)
        old_init = webdriver_type.__init__
        webdriver_type.__init__ = self.mock_init

        try:
            self.was_called = False
            bm._make_browser(browser_name, **kw)
        except AttributeError:
            pass  #kinda dangerous but I'm too lazy to mock out all the set_timeout calls
        finally:
            webdriver_type.__init__ = old_init
            self.assertTrue(self.was_called)
        unstub()

    def mock_init(self, *args, **kw):
        self.was_called = True
