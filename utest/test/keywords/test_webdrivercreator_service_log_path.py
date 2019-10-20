import os
import unittest

from mockito import mock, when, unstub, ANY
from selenium import webdriver

from SeleniumLibrary.keywords import WebDriverCreator


class WebDriverCreatorServiceLogPathTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        cls.output_dir = os.path.abspath(
            os.path.join(curr_dir, '..', '..', 'output_dir'))
        cls.creator = WebDriverCreator(cls.output_dir)

    def tearDown(self):
        unstub()

    def test_no_log_file(self):
        self.assertEqual(self.creator._get_log_path(None), None)
        self.assertEqual(self.creator._get_log_path('NoNe'), None)

    def test_log_file_with_rf_file_separator(self):
        log_file = '/path/to/own_name.txt'
        file_name = self.creator._get_log_path(log_file)
        log_file = log_file.replace('/', os.sep)
        self.assertEqual(file_name, log_file)

    def test_log_file_with_index(self):
        log_file = os.path.join(self.output_dir, 'firefox-{index}.log')
        file_name = self.creator._get_log_path(log_file)
        self.assertEqual(file_name, log_file.format(index='1'))

    def test_log_file_with_index_exist(self):
        log_file = os.path.join(self.output_dir, 'firefox-{index}.log')
        with open(os.path.join(self.output_dir, log_file.format(index='1')), 'w') as file:
            file.close()
        file_name = self.creator._get_log_path(log_file)
        self.assertEqual(file_name, log_file.format(index='2'))

    def test_create_chrome_with_service_log_path_none(self):
        expected_webdriver = mock()
        when(webdriver).Chrome(options=None, service_log_path=None).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({}, None, service_log_path=None)
        self.assertEqual(driver, expected_webdriver)

    def test_create_chrome_with_service_log_path_real_path(self):
        log_file = os.path.join(self.output_dir, 'firefox-{index}.log')
        expected_webdriver = mock()
        when(webdriver).Chrome(options=None, service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({}, None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)

    def test_create_headlesschrome_with_service_log_path_real_path(self):
        log_file = os.path.join(self.output_dir, 'firefox-{index}.log')
        expected_webdriver = mock()
        options = mock()
        when(webdriver).ChromeOptions().thenReturn(options)
        when(webdriver).Chrome(options=options, service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_chrome({}, None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)

    def test_create_firefox_with_service_log_path_none(self):
        log_file = os.path.join(self.output_dir, 'geckodriver-1.log')
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        when(webdriver).Firefox(options=None, firefox_profile=profile,
                                service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({}, None, None, service_log_path=None)
        self.assertEqual(driver, expected_webdriver)

    def test_create_firefox_with_service_log_path_real_path(self):
        log_file = os.path.join(self.output_dir, 'firefox-{index}.log')
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        when(webdriver).Firefox(options=None, firefox_profile=profile,
                                service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({}, None, ff_profile_dir=None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)


    def test_create_headlessfirefox_with_service_log_path_real_path(self):
        log_file = os.path.join(self.output_dir, 'firefox-{index}.log')
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        options = mock()
        when(webdriver).FirefoxOptions().thenReturn(options)
        when(webdriver).Firefox(options=options, firefox_profile=profile,
                                service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_firefox({}, None, ff_profile_dir=None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)

    def test_create_firefox_from_create_driver(self):
        log_file = os.path.join(self.output_dir, 'firefox-1.log')
        expected_webdriver = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        options = mock()
        when(webdriver).FirefoxOptions().thenReturn(options)
        when(webdriver).Firefox(options=None, firefox_profile=profile,
                                service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_driver('firefox ', {}, remote_url=None,  profile_dir=None,
                                            service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)

    def test_create_ie_with_service_log_path_real_path(self):
        log_file = os.path.join(self.output_dir, 'ie-1.log')
        expected_webdriver = mock()
        when(webdriver).Ie(options=None, service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({}, None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)

    def test_create_edge_with_service_log_path_real_path(self):
        log_file = os.path.join(self.output_dir, 'ie-1.log')
        expected_webdriver = mock()
        when(self.creator)._has_options(ANY).thenReturn(False)
        when(webdriver).Edge(service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_edge({}, None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)

    def test_create_opera_with_service_log_path_real_path(self):
        log_file = os.path.join(self.output_dir, 'ie-1.log')
        expected_webdriver = mock()
        when(webdriver).Opera(options=None, service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_opera({}, None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)

    def test_create_safari_no_support_for_service_log_path(self):
        log_file = os.path.join(self.output_dir, 'ie-1.log')
        expected_webdriver = mock()
        when(webdriver).Safari().thenReturn(expected_webdriver)
        driver = self.creator.create_safari({}, None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)

    def test_create_phantomjs_with_service_log_path_real_path(self):
        log_file = os.path.join(self.output_dir, 'ie-1.log')
        expected_webdriver = mock()
        when(webdriver).PhantomJS(service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_phantomjs({}, None, service_log_path=log_file)
        self.assertEqual(driver, expected_webdriver)
