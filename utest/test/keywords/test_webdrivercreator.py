import os
import unittest

from mockito import mock, verify, when, unstub
from selenium import webdriver

from SeleniumLibrary.keywords import WebDriverCreator


class WebDriverCreatorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log_dir = '/log/dir'
        cls.creator = WebDriverCreator(cls.log_dir)

    def tearDown(self):
        unstub()

    def test_get_creator_method(self):
        method = self.creator._get_creator_method('chrome')
        self.assertTrue(method)

        method = self.creator._get_creator_method('Chrome')
        self.assertTrue(method)

        method = self.creator._get_creator_method('Fire Fox')
        self.assertTrue(method)

        with self.assertRaisesRegexp(ValueError, 'foobar is not a supported browser.'):
            self.creator._get_creator_method('foobar')

    def test_parse_capabilities(self):
        caps = self.creator._parse_capabilities('key1:value1,key2:value2')
        expected = {'desired_capabilities': {'key1': 'value1', 'key2': 'value2'}}
        self.assertDictEqual(caps, expected)

        caps = self.creator._parse_capabilities('key1:value1,key2:value2', 'ie')
        expected = {'capabilities': {'key1': 'value1', 'key2': 'value2'}}
        self.assertDictEqual(caps, expected)

        caps = self.creator._parse_capabilities('key1:value1,key2:value2', 'firefox')
        self.assertDictEqual(caps, expected)

        caps = self.creator._parse_capabilities('key1:value1,key2:value2', 'ff')
        self.assertDictEqual(caps, expected)

        caps = self.creator._parse_capabilities('key1:value1,key2:value2', 'edge')
        self.assertDictEqual(caps, expected)

        parsing_caps = expected.copy()
        caps = self.creator._parse_capabilities(parsing_caps)
        self.assertDictEqual(caps, {'desired_capabilities': expected})

        caps = self.creator._parse_capabilities('key1 : value1 , key2: value2')
        expected = {'desired_capabilities': {'key1': 'value1', 'key2': 'value2'}}
        self.assertDictEqual(caps, expected)

        caps = self.creator._parse_capabilities(' key 1 : value 1 , key2:value2')
        expected = {'desired_capabilities': {'key 1': 'value 1', 'key2': 'value2'}}
        self.assertDictEqual(caps, expected)

        caps = self.creator._parse_capabilities('')
        self.assertDictEqual(caps, {})

        caps = self.creator._parse_capabilities({})
        self.assertDictEqual(caps, {})

        caps = self.creator._parse_capabilities(None)
        self.assertDictEqual(caps, {})

        for browser in [None, 'safari', 'headlesschrome', 'foobar']:
            caps = self.creator._parse_capabilities({'key1': 'value1', 'key2': 'value2'}, browser)
            expected = {'desired_capabilities': {'key1': 'value1', 'key2': 'value2'}}
            self.assertDictEqual(caps, expected)

        for browser in ['ie', 'firefox', 'edge']:
            caps = self.creator._parse_capabilities({'key1': 'value1', 'key2': 'value2'}, browser)
            expected = {'capabilities': {'key1': 'value1', 'key2': 'value2'}}
            self.assertDictEqual(caps, expected)

    def test_chrome(self):
        expected_webdriver = mock()
        when(webdriver).Chrome(options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_with_desired_capabilities(self):
        expected_webdriver = mock()
        when(webdriver).Chrome(desired_capabilities={'key': 'value'}, options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({'desired_capabilities': {'key': 'value'}}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_remote(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_healdless(self):
        expected_webdriver = mock()
        options = mock()
        when(webdriver).ChromeOptions().thenReturn(options)
        when(webdriver).Chrome(options=options).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_chrome({}, None)
        verify(options).set_headless()
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_healdless_with_grid(self):
        expected_webdriver = mock()
        options = mock()
        when(webdriver).ChromeOptions().thenReturn(options)
        remote_url = 'localhost:4444'
        when(webdriver).Remote(command_executor=remote_url,
                               options=options, browser_profile=None).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_chrome({}, remote_url)
        verify(options).set_headless()
        self.assertEqual(driver, expected_webdriver)

    def test_firefox(self):
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        log_file = self.get_geckodriver_log()
        when(webdriver).Firefox(options=None,
                                firefox_profile=profile,
                                log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({}, None, None)
        self.assertEqual(driver, expected_webdriver)
        verify(webdriver).FirefoxProfile()

    def test_firefox_remote(self):
        url = 'http://localhost:4444/wd/hub'
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=profile,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({}, url, None)
        self.assertEqual(driver, expected_webdriver)

    def test_firefox_profile(self):
        expected_webdriver = mock()
        profile = mock()
        profile_dir = '/profile/dir'
        when(webdriver).FirefoxProfile(profile_dir).thenReturn(profile)
        log_file = self.get_geckodriver_log()
        when(webdriver).Firefox(options=None, log_path=log_file,
                                firefox_profile=profile).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({}, None, profile_dir)
        self.assertEqual(driver, expected_webdriver)

    def test_firefox_headless(self):
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        options = mock()
        when(webdriver).FirefoxOptions().thenReturn(options)
        log_file = self.get_geckodriver_log()
        when(webdriver).Firefox(options=options, log_path=log_file,
                                firefox_profile=profile).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_firefox({}, None, None)
        self.assertEqual(driver, expected_webdriver)

    def test_firefox_healdless_with_grid(self):
        expected_webdriver = mock()
        options = mock()
        when(webdriver).FirefoxOptions().thenReturn(options)
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        remote_url = 'localhost:4444'
        when(webdriver).Remote(command_executor=remote_url, options=options,
                               desired_capabilities={'key': 'value'},
                               browser_profile=profile,).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_firefox({'capabilities': {'key': 'value'}}, remote_url, None)
        verify(options).set_headless()
        self.assertEqual(driver, expected_webdriver)

        when(webdriver).Remote(command_executor=remote_url, options=options,
                               browser_profile=profile, ).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_firefox({}, remote_url, None)
        self.assertEqual(driver, expected_webdriver)
        verify(options, times=2).set_headless()

    def test_ie(self):
        expected_webdriver = mock()
        when(webdriver).Ie().thenReturn(expected_webdriver)
        driver = self.creator.create_ie({}, None)
        self.assertEqual(driver, expected_webdriver)

        when(webdriver).Ie(capabilities={'key': 'value'}).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({'capabilities': {'key': 'value'}}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_ie_remote(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_edge(self):
        expected_webdriver = mock()
        when(webdriver).Edge().thenReturn(expected_webdriver)
        driver = self.creator.create_edge({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_edge_remote(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_edge({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_opera(self):
        expected_webdriver = mock()
        when(webdriver).Opera().thenReturn(expected_webdriver)
        driver = self.creator.create_opera({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_opera_remote(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_opera({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_safari(self):
        expected_webdriver = mock()
        when(webdriver).Safari().thenReturn(expected_webdriver)
        driver = self.creator.create_safari({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_safari_remote(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_safari({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_phantomjs(self):
        expected_webdriver = mock()
        when(webdriver).PhantomJS().thenReturn(expected_webdriver)
        driver = self.creator.create_phantomjs({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_phantomjs_remote(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_phantomjs({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_htmlunit(self):
        caps = webdriver.DesiredCapabilities.HTMLUNIT
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_htmlunit_with_js(self):
        caps = webdriver.DesiredCapabilities.HTMLUNITWITHJS
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit_with_js({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_android(self):
        caps = webdriver.DesiredCapabilities.ANDROID
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_android({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_iphone(self):
        caps = webdriver.DesiredCapabilities.IPHONE
        expected_webdriver = mock()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None,
                               options=None).thenReturn(expected_webdriver)
        driver = self.creator.create_iphone({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_create_driver_chrome(self):
        expected_webdriver = mock()
        when(webdriver).Chrome(options=None).thenReturn(expected_webdriver)
        for browser in ['chrome', 'googlechrome', 'gc']:
            driver = self.creator.create_driver(browser, None, None)
            self.assertEqual(driver, expected_webdriver)

    def test_create_driver_firefox(self):
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        log_file = self.get_geckodriver_log()
        when(webdriver).Firefox(options=None, log_path=log_file,
                                firefox_profile=profile).thenReturn(expected_webdriver)
        for browser in ['ff', 'firefox']:
            driver = self.creator.create_driver(browser, None, None, None)
            self.assertEqual(driver, expected_webdriver)

    def test_create_driver_ie(self):
        expected_webdriver = mock()
        when(webdriver).Ie().thenReturn(expected_webdriver)
        for browser in ['ie', 'Internet Explorer']:
            driver = self.creator.create_driver(browser, None, None)
            self.assertEqual(driver, expected_webdriver)

    def get_geckodriver_log(self):
        return os.path.join(self.log_dir, 'geckodriver.log')
