import os
import unittest

from mockito import mock, verify, when, unstub, ANY
from selenium import webdriver

from SeleniumLibrary.keywords import WebDriverCreator


class WebDriverCreatorTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.log_dir = '/log/dir'
        cls.creator = WebDriverCreator(cls.log_dir)

    def tearDown(self):
        unstub()

    def test_normalise_browser_name(self):
        browser = self.creator._normalise_browser_name('chrome')
        self.assertEqual(browser, 'chrome')

        browser = self.creator._normalise_browser_name('ChrOmE')
        self.assertEqual(browser, 'chrome')

        browser = self.creator._normalise_browser_name(' Ch rO mE ')
        self.assertEqual(browser, 'chrome')

    def test_get_creator_method(self):
        method = self.creator._get_creator_method('chrome')
        self.assertTrue(method)

        method = self.creator._get_creator_method('firefox')
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

    def test_capabilities_resolver_firefox(self):
        default_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        expected_caps = {'desired_capabilities': {'version': '66.02', 'browserName': 'firefox'}}
        caps_in = {'capabilities': {'version': '66.02'}}
        resolved_caps = self.creator._remote_capabilities_resolver(caps_in, default_capabilities)
        self.assertEqual(resolved_caps, expected_caps)

        caps_in = {'capabilities': {'version': '66.02', 'browserName': 'firefox'}}
        resolved_caps = self.creator._remote_capabilities_resolver(caps_in, default_capabilities)
        self.assertEqual(resolved_caps, expected_caps)

    def test_capabilities_resolver_no_set_caps(self):
        default_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        resolved_caps = self.creator._remote_capabilities_resolver({}, default_capabilities)
        self.assertEqual(resolved_caps, {'desired_capabilities': default_capabilities})

    def test_capabilities_resolver_chrome(self):
        default_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        expected_caps = {'desired_capabilities': {'version': '73.0.3683.86', 'browserName': 'chrome'}}
        resolved_caps = self.creator._remote_capabilities_resolver({'capabilities': {'version': '73.0.3683.86'}},
                                                                   default_capabilities)
        self.assertEqual(resolved_caps, expected_caps)

        caps_in = {'desired_capabilities': {'version': '73.0.3683.86', 'browserName': 'chrome'}}
        resolved_caps = self.creator._remote_capabilities_resolver(caps_in, default_capabilities)
        self.assertEqual(resolved_caps, expected_caps)

    def test_chrome(self):
        expected_webdriver = mock()
        when(webdriver).Chrome(options=None, service_log_path=None).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_with_desired_capabilities(self):
        expected_webdriver = mock()
        when(webdriver).Chrome(desired_capabilities={'key': 'value'},
                               options=None, service_log_path=None).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({'desired_capabilities': {'key': 'value'}}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_remote_no_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_remote_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {"browserName": "chrome"}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({'desired_capabilities': capabilities}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_remote_caps_no_browser_name(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {'browserName': 'chrome', 'key': 'value'}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({'desired_capabilities': {'key': 'value'}}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_healdless(self):
        expected_webdriver = mock()
        options = mock()
        when(webdriver).ChromeOptions().thenReturn(options)
        when(webdriver).Chrome(options=options, service_log_path=None).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_chrome({}, None)
        verify(options).set_headless()
        self.assertEqual(driver, expected_webdriver)

    def test_chrome_healdless_with_grid(self):
        expected_webdriver = mock()
        options = mock()
        when(webdriver).ChromeOptions().thenReturn(options)
        remote_url = 'localhost:4444'
        capabilities = webdriver.DesiredCapabilities.CHROME.copy()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=remote_url,
                               options=options, browser_profile=None,
                               desired_capabilities=capabilities,
                               file_detector=file_detector).thenReturn(expected_webdriver)
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
                                service_log_path=log_file).thenReturn(expected_webdriver)
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        driver = self.creator.create_firefox({}, None, None)
        self.assertEqual(driver, expected_webdriver)
        verify(webdriver).FirefoxProfile()

    def test_get_ff_profile_real_path(self):
        profile_path = '/path/to/profile'
        profile_mock = mock()
        when(webdriver).FirefoxProfile(profile_path).thenReturn(profile_mock)
        profile = self.creator._get_ff_profile(profile_path)
        self.assertEqual(profile, profile_mock)

    def test_get_ff_profile_no_path(self):
        profile_mock = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile_mock)
        profile = self.creator._get_ff_profile(None)
        self.assertEqual(profile, profile_mock)

    def test_get_ff_profile_instance_FirefoxProfile(self):
        input_profile = webdriver.FirefoxProfile()
        profile = self.creator._get_ff_profile(input_profile)
        self.assertEqual(profile, input_profile)

    def test_firefox_remote_no_caps(self):
        url = 'http://localhost:4444/wd/hub'
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        expected_webdriver = mock()
        capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=profile, options=None,
                               desired_capabilities=capabilities,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({}, url, None)
        self.assertEqual(driver, expected_webdriver)

    def test_firefox_remote_caps(self):
        url = 'http://localhost:4444/wd/hub'
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        expected_webdriver = mock()
        capabilities = {"browserName": "firefox"}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=profile, options=None,
                               desired_capabilities=capabilities,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({'desired_capabilities': capabilities}, url, None)
        self.assertEqual(driver, expected_webdriver)

    def test_firefox_remote_caps_no_browsername(self):
        url = 'http://localhost:4444/wd/hub'
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        expected_webdriver = mock()
        capabilities = {'browserName': 'firefox', 'version': '66.02'}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               browser_profile=profile, options=None,
                               desired_capabilities=capabilities,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({'capabilities': {"version": "66.02"}}, url, None)
        self.assertEqual(driver, expected_webdriver)

    def test_firefox_profile(self):
        expected_webdriver = mock()
        profile = mock()
        profile_dir = '/profile/dir'
        when(webdriver).FirefoxProfile(profile_dir).thenReturn(profile)
        log_file = self.get_geckodriver_log()
        when(webdriver).Firefox(options=None, service_log_path=log_file,
                                firefox_profile=profile).thenReturn(expected_webdriver)
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        driver = self.creator.create_firefox({}, None, profile_dir)
        self.assertEqual(driver, expected_webdriver)

    def test_firefox_headless(self):
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        options = mock()
        when(webdriver).FirefoxOptions().thenReturn(options)
        log_file = self.get_geckodriver_log()
        when(webdriver).Firefox(options=options, service_log_path=log_file,
                                firefox_profile=profile).thenReturn(expected_webdriver)
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        driver = self.creator.create_headless_firefox({}, None, None)
        self.assertEqual(driver, expected_webdriver)

    def test_firefox_healdless_with_grid_caps(self):
        expected_webdriver = mock()
        options = mock()
        when(webdriver).FirefoxOptions().thenReturn(options)
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        remote_url = 'localhost:4444'
        capabilities = {'browserName': 'firefox', 'key': 'value'}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=remote_url, options=options,
                               desired_capabilities=capabilities,
                               browser_profile=profile,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_firefox({'capabilities': {'key': 'value'}}, remote_url, None)
        verify(options).set_headless()
        self.assertEqual(driver, expected_webdriver)
        verify(options).set_headless()

    def test_firefox_healdless_with_grid_no_caps(self):
        expected_webdriver = mock()
        options = mock()
        when(webdriver).FirefoxOptions().thenReturn(options)
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        remote_url = 'localhost:4444'
        capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=remote_url, options=options,
                               desired_capabilities=capabilities,
                               browser_profile=profile,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_firefox({}, remote_url, None)
        self.assertEqual(driver, expected_webdriver)
        verify(options).set_headless()

    def test_ie(self):
        expected_webdriver = mock()
        when(webdriver).Ie().thenReturn(expected_webdriver)
        when(self.creator)._has_service_log_path(ANY).thenReturn(False)
        when(self.creator)._has_options(ANY).thenReturn(False)
        driver = self.creator.create_ie({}, None)
        self.assertEqual(driver, expected_webdriver)

        when(webdriver).Ie(capabilities={'key': 'value'}).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({'capabilities': {'key': 'value'}}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_ie_remote_no_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_ie_remote_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {"browserName": "internet explorer"}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({'capabilities': capabilities}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_ie_no_browser_name(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {'browserName': 'internet explorer', 'key': 'value'}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({'capabilities': {'key': 'value'}}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_edge(self):
        expected_webdriver = mock()
        when(webdriver).Edge(service_log_path=None).thenReturn(expected_webdriver)
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        when(self.creator)._has_options(ANY).thenReturn(False)
        driver = self.creator.create_edge({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_edge_remote_no_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = webdriver.DesiredCapabilities.EDGE.copy()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_edge({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_edge_remote_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {"browserName": "MicrosoftEdge"}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_edge({'capabilities': capabilities}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_edge_no_browser_name(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {'browserName': 'MicrosoftEdge', 'key': 'value'}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_edge({'capabilities': {'key': 'value'}}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_opera(self):
        expected_webdriver = mock()
        when(webdriver).Opera(options=None, service_log_path=None).thenReturn(expected_webdriver)
        driver = self.creator.create_opera({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_opera_remote_no_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = webdriver.DesiredCapabilities.OPERA.copy()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None, file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_opera({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_opera_remote_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {"browserName": "opera"}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None, file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_opera({'desired_capabilities': capabilities}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_opera_no_browser_name(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {'browserName': 'opera', 'key': 'value'}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None, file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_opera({'desired_capabilities': {'key': 'value'}}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_safari(self):
        expected_webdriver = mock()
        when(webdriver).Safari().thenReturn(expected_webdriver)
        driver = self.creator.create_safari({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_safari_remote_no_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        capabilities = webdriver.DesiredCapabilities.SAFARI.copy()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None, file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_safari({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_safari_remote_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {"browserName": "safari"}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None, file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_safari({'desired_capabilities': capabilities}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_safari_no_broser_name(self):
        file_detector = self.mock_file_detector()
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {'browserName': 'safari', 'key': 'value'}
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None, file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_safari({'desired_capabilities': {'key': 'value'}}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_phantomjs(self):
        expected_webdriver = mock()
        when(webdriver).PhantomJS(service_log_path=None).thenReturn(expected_webdriver)
        driver = self.creator.create_phantomjs({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_phantomjs_remote_no_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_phantomjs({}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_phantomjs_remote_caps(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {"browserName": "phantomjs"}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_phantomjs({'desired_capabilities': capabilities}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_phantomjs_no_browser_name(self):
        url = 'http://localhost:4444/wd/hub'
        expected_webdriver = mock()
        capabilities = {'browserName': 'phantomjs', 'key': 'value'}
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url, browser_profile=None,
                               desired_capabilities=capabilities,
                               options=None, file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_phantomjs({'desired_capabilities': {'key': 'value'}}, url)
        self.assertEqual(driver, expected_webdriver)

    def test_htmlunit_no_caps(self):
        caps = webdriver.DesiredCapabilities.HTMLUNIT
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_htmlunit_remote_caps(self):
        caps = {"browserName": "htmlunit"}
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit({'desired_capabilities': caps}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_htmlunit_no_browser_name(self):
        capabilities = {'browserName': 'htmlunit', 'key': 'value'}
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=capabilities,
                               browser_profile=None, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit({'desired_capabilities': {'key': 'value'}}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_htmlunit_with_js(self):
        caps = webdriver.DesiredCapabilities.HTMLUNITWITHJS.copy()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit_with_js({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_htmlunit_with_js_no_browser_name(self):
        capabilities = {'browserName': 'htmlunit', 'key': 'value'}
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=capabilities,
                               browser_profile=None, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit_with_js({'desired_capabilities': {'key': 'value'}}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_android(self):
        caps = webdriver.DesiredCapabilities.ANDROID
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_android({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_android_no_browser_name(self):
        capabilities = {'browserName': 'android', 'key': 'value'}
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=capabilities,
                               browser_profile=None, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_android({'desired_capabilities': {'key': 'value'}}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_iphone(self):
        caps = webdriver.DesiredCapabilities.IPHONE
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=None,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_iphone({}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_iphone_no_browser_name(self):
        capabilities = {'browserName': 'iPhone', 'key': 'value'}
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=capabilities,
                               browser_profile=None,
                               options=None, file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_iphone({'desired_capabilities': {'key': 'value'}}, None)
        self.assertEqual(driver, expected_webdriver)

    def test_create_driver_chrome(self):
        expected_webdriver = mock()
        when(webdriver).Chrome(options=None, service_log_path=None).thenReturn(expected_webdriver)
        for browser in ['chrome', 'googlechrome', 'gc']:
            driver = self.creator.create_driver(browser, None, None)
            self.assertEqual(driver, expected_webdriver)

    def test_create_driver_firefox(self):
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        log_file = self.get_geckodriver_log()
        when(webdriver).Firefox(options=None, service_log_path=log_file,
                                firefox_profile=profile).thenReturn(expected_webdriver)
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        for browser in ['ff', 'firefox']:
            driver = self.creator.create_driver(browser, None, None, None)
            self.assertEqual(driver, expected_webdriver)

    def test_create_driver_ie(self):
        expected_webdriver = mock()
        when(self.creator)._has_service_log_path(ANY).thenReturn(False)
        when(self.creator)._has_options(ANY).thenReturn(False)
        when(webdriver).Ie().thenReturn(expected_webdriver)
        for browser in ['ie', 'Internet Explorer']:
            driver = self.creator.create_driver(browser, None, None)
            self.assertEqual(driver, expected_webdriver)

    def get_geckodriver_log(self):
        return os.path.join(self.log_dir, 'geckodriver-1.log')

    def mock_file_detector(self):
        file_detector = mock()
        when(self.creator)._get_sl_file_detector().thenReturn(file_detector)
        return file_detector
