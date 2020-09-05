import unittest

from mockito import mock, unstub, when, verify, ANY

from SeleniumLibrary.keywords import BrowserManagementKeywords


class KeywordArgumentsElementTest(unittest.TestCase):
    def setUp(self):
        ctx = mock()
        ctx.event_firing_webdriver = None
        ctx._browser = mock()
        ctx._drivers = mock()
        self.ctx = ctx
        self.brorser = BrowserManagementKeywords(ctx)

    def tearDown(self):
        unstub()

    def test_open_browser(self):
        url = "https://github.com/robotframework"
        remote_url = '"http://localhost:4444/wd/hub"'
        browser = mock()
        when(self.brorser)._make_driver(
            "firefox", None, None, False, None, None, None
        ).thenReturn(browser)
        alias = self.brorser.open_browser(url)
        self.assertEqual(alias, None)

        when(self.brorser)._make_driver(
            "firefox", None, None, remote_url, None, None, None
        ).thenReturn(browser)
        alias = self.brorser.open_browser(url, alias="None", remote_url=remote_url)
        self.assertEqual(alias, None)

    def test_same_alias(self):
        url = "https://github.com/robotframework"
        alias = "tidii"
        driver = mock()
        driver.session_id = "foobar"
        self.ctx.driver = driver
        when(self.ctx._drivers).get_index(alias).thenReturn(1)
        when(self.ctx._drivers).switch(1).thenReturn(driver)
        self.brorser.open_browser(url=url, alias=alias)
        verify(driver, times=1).get(url)

    def test_open_browser_no_get(self):
        browser = mock()
        when(self.brorser)._make_driver(
            "firefox", None, None, False, None, None, None
        ).thenReturn(browser)
        self.brorser.open_browser()
        verify(browser, times=0).get(ANY)

    def test_same_alias_and_not_get(self):
        alias = "tidii"
        driver = mock()
        driver.session_id = "foobar"
        self.ctx.driver = driver
        when(self.ctx._drivers).get_index(alias).thenReturn(1)
        when(self.ctx._drivers).switch(1).thenReturn(driver)
        self.brorser.open_browser(alias=alias)
        verify(driver, times=0).get(ANY)
