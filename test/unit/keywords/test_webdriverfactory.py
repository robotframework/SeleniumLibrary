import unittest

from selenium import webdriver
from mockito import mock, unstub, when, verify

from SeleniumLibrary.utils import WebDriverFactory
from SeleniumLibrary.utils.webdriverfactory import (CreateAndroid, CreateBase,
                                                    CreateChrome, CreateEdge,
                                                    CreateFirefox, CreateIe, CreateiPhone,
                                                    CreateOpera, CreateSafari,
                                                    CreateHtmlUnit, CreateHtmlUnitWithJS,
                                                    CreatePhantomJS,)


class WebDriverFactoryTest(unittest.TestCase):

    def test_parse_chrome_not_headless(self):
        browsers = ['cHroMe', 'gOOglechRome  ', '  GC  ', 'google_chrome',
                    'google chrome']
        for chrome in browsers:
            headless, driver = WebDriverFactory(chrome).parse_browser()
            self.assertFalse(headless)
            self.assertEqual(driver, CreateChrome)

    def test_parse_chrome_headless(self):
        for chrome in ['headlesschrome', 'headless chrome', 'headless_chrome']:
            headless, driver = WebDriverFactory(chrome).parse_browser()
            self.assertTrue(headless)
            self.assertEqual(driver, CreateChrome)

    def test_strip_headless(self):
        headless, driver = WebDriverFactory('HEADLESSCHROME')._headless('HEADLESSCHROME')
        self.assertTrue(headless)
        self.assertEqual(driver, 'CHROME')

        headless, driver = WebDriverFactory('HEADLESSFIREFOX')._headless('HEADLESSFIREFOX')
        self.assertTrue(headless)
        self.assertEqual(driver, 'FIREFOX')

    def test_parse_firefox(self):
        for ff in ['ff', 'firefox']:
            headless, driver = WebDriverFactory(ff).parse_browser()
            self.assertFalse(headless)
            self.assertEqual(driver, CreateFirefox)
        headless, driver = WebDriverFactory('headlessfirefox').parse_browser()
        self.assertTrue(headless)
        self.assertEqual(driver, CreateFirefox)

    def test_parse_ie(self):
        for ie in ['IE', 'internetexplorer']:
            headless, driver = WebDriverFactory(ie).parse_browser()
            self.assertFalse(headless)
            self.assertEqual(driver, CreateIe)

    def test_parse_opera(self):
        headless, driver = WebDriverFactory('opera').parse_browser()
        self.assertFalse(headless)
        self.assertEqual(driver, CreateOpera)

    def test_parse_phantomjs(self):
        headless, driver = WebDriverFactory('phantomjs').parse_browser()
        self.assertFalse(headless)
        self.assertEqual(driver, CreatePhantomJS)

    def test_parse_edge(self):
        headless, driver = WebDriverFactory('edge').parse_browser()
        self.assertFalse(headless)
        self.assertEqual(driver, CreateEdge)

    def test_parse_safari(self):
        headless, driver = WebDriverFactory('safari').parse_browser()
        self.assertFalse(headless)
        self.assertEqual(driver, CreateSafari)

    def test_parse_android(self):
        headless, driver = WebDriverFactory('android').parse_browser()
        self.assertFalse(headless)
        self.assertEqual(driver, CreateAndroid)

    def test_parse_remote_drivers(self):
        headless, driver = WebDriverFactory('htmlunit').parse_browser()
        self.assertFalse(headless)
        self.assertEqual(driver, CreateHtmlUnit)

        headless, driver = WebDriverFactory('htmlunitwithjs').parse_browser()
        self.assertFalse(headless)
        self.assertEqual(driver, CreateHtmlUnitWithJS)

        headless, driver = WebDriverFactory('iphone').parse_browser()
        self.assertFalse(headless)
        self.assertEqual(driver, CreateiPhone)

    def test_parse_error(self):
        with self.assertRaisesRegexp(ValueError, 'headless_ie'):
            WebDriverFactory('headless_ie').parse_browser()
        with self.assertRaisesRegexp(ValueError, 'headless_opera'):
            WebDriverFactory('headless_opera').parse_browser()
        with self.assertRaisesRegexp(ValueError, 'headless_phantomjs'):
            WebDriverFactory('headless_phantomjs').parse_browser()
        with self.assertRaisesRegexp(ValueError, 'headless_edge'):
            WebDriverFactory('headless_edge').parse_browser()
        with self.assertRaisesRegexp(ValueError, 'headless_safari'):
            WebDriverFactory('headless_safari').parse_browser()
        with self.assertRaisesRegexp(ValueError, 'headless_android'):
            WebDriverFactory('headless_android').parse_browser()
        with self.assertRaisesRegexp(ValueError, 'headless_htmlunit'):
            WebDriverFactory('headless_htmlunit').parse_browser()
        with self.assertRaisesRegexp(ValueError, 'Foo is not a supported browser.'):
            WebDriverFactory('Foo').parse_browser()


class WebDriverFactoryChromeTest(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_create_with_default(self):
        mock_driver = mock()
        when(webdriver).Chrome(desired_capabilities={},
                               options=None).thenReturn(mock_driver)
        driver = WebDriverFactory('chrome').create(remote_url=None,
                                                   desired_capabilities=None,
                                                   ff_profile_dir=None)
        self.assertEqual(driver, mock_driver)

        driver = WebDriverFactory('chrome').create(remote_url='None',
                                                   desired_capabilities='None',
                                                   ff_profile_dir='None')
        self.assertEqual(driver, mock_driver)

    def test_create_with_caps(self):
        mock_driver = mock()
        caps = 'browserName:chrome'
        when(webdriver).Chrome(
            desired_capabilities={'browserName': 'chrome'},
            options=None).thenReturn(mock_driver)
        driver = WebDriverFactory('chrome').create(remote_url=None,
                                                   desired_capabilities=caps,
                                                   ff_profile_dir=None)
        self.assertEqual(driver, mock_driver)

    def test_create_with_headless(self):
        options = mock()
        when(webdriver).ChromeOptions().thenReturn(options)
        mock_driver = mock()
        when(webdriver).Chrome(desired_capabilities={},
                               options=options).thenReturn(mock_driver)
        driver = WebDriverFactory('headlesschrome').create(remote_url=None,
                                                           desired_capabilities=None,
                                                           ff_profile_dir=None)
        self.assertEqual(driver, mock_driver)
        verify(options).set_headless()

    def test_create_with_remote_url(self):
        mock_driver = mock()
        url = 'http://127.0.0.1:4444/wd/hub'
        caps = {'platform': 'ANY', 'browserName': 'chrome', 'version': ''}
        when(webdriver).Remote(command_executor=url,
                               desired_capabilities=caps,
                               browser_profile=None).thenReturn(mock_driver)
        driver = WebDriverFactory('chrome').create(remote_url=url,
                                                   desired_capabilities=None,
                                                   ff_profile_dir=None)
        self.assertEqual(driver, mock_driver)


class WebDriverFactoryFirefoxTest(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_create_with_default(self):
        mock_driver = mock()
        when(webdriver).Firefox(firefox_profile=None, capabilities={},
                                options=None).thenReturn(mock_driver)
        driver = WebDriverFactory('Firefox').create(remote_url=None,
                                                    desired_capabilities=None,
                                                    ff_profile_dir=None)
        self.assertEqual(driver, mock_driver)

    def test_create_with_caps(self):
        mock_driver = mock()
        caps = 'browserName:firefox'
        when(webdriver).Firefox(firefox_profile=None,
                                capabilities={'browserName': 'firefox'},
                                options=None).thenReturn(mock_driver)
        driver = WebDriverFactory('Firefox').create(remote_url=None,
                                                    desired_capabilities=caps,
                                                    ff_profile_dir=None)
        self.assertEqual(driver, mock_driver)

    def not_test_create_with_headless(self):
        options = mock()
        when(webdriver).ChromeOptions().thenReturn(options)
        mock_driver = mock()
        when(webdriver).Chrome(desired_capabilities={},
                               options=options).thenReturn(mock_driver)
        driver = WebDriverFactory('headlesschrome').create(remote_url=None,
                                                           desired_capabilities=None,
                                                           ff_profile_dir=None)
        self.assertEqual(driver, mock_driver)
        verify(options).set_headless()


class CreateBaseTest(unittest.TestCase):

    def test_desired_capabilities_none(self):
        caps = CreateBase().parse_desired_capabilities(None)
        self.assertEqual(caps, {})

        caps = CreateBase().parse_desired_capabilities('None')
        self.assertEqual(caps, {})

    def test_desired_capabilities_dict(self):
        caps_dict = {'platform': 'ANY', 'browserName': 'chrome', 'version': ''}
        caps = CreateBase().parse_desired_capabilities(caps_dict)
        self.assertEqual(caps, caps_dict)

    def test_desired_capabilities_str(self):
        caps_dict = {'key1': 'val1', 'key2': 'val2'}
        caps = CreateBase().parse_desired_capabilities('key1:val1,key2:val2')
        self.assertEqual(caps, caps_dict)

        caps = CreateBase().parse_desired_capabilities(' key1 : val1 , key2 : val2 ')
        self.assertEqual(caps, caps_dict)

        caps_dict = {'key 1': 'val 1', 'key 2': 'val 2'}
        caps = CreateBase().parse_desired_capabilities(' key 1 : val 1 , key 2 : val 2 ')
        self.assertEqual(caps, caps_dict)
