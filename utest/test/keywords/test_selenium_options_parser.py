import inspect
import unittest
import os

from mockito import mock, when, unstub, ANY
from robot.utils import JYTHON
from selenium import webdriver

try:
    from approvaltests.approvals import verify_all
    from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
except ImportError:
    if JYTHON:
        verify = None
        GenericDiffReporterFactory = None
    else:
        raise

from SeleniumLibrary.keywords.webdrivertools import SeleniumOptions, WebDriverCreator


class SeleniumOptionsParserTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.options = SeleniumOptions()

    def setUp(self):
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(os.path.join(path, '..', 'approvals_reporters.json'))
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        self.reporter = factory.get_first_working()
        self.results = []

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_parse_options_string(self):
        self.results.append(self.options._parse('method("arg1")'))
        self.results.append(self.options._parse('method("arg1", "arg2")'))
        self.results.append(self.options._parse('method(True)'))
        self.results.append(self.options._parse('method(1)'))
        self.results.append(self.options._parse('method("arg1", 2, None, False, "arg2")'))
        self.results.append(self.options._parse('method ( " arg1 " , 2 , None , False , " arg2 " )'))
        self.results.append(self.options._parse('attribute="arg1"'))
        self.results.append(self.options._parse('attribute = True'))
        self.results.append(self.options._parse('method("arg1");attribute=True'))
        self.results.append(self.options._parse('method("arg1") ; attribute=True ; method("arg2")'))
        self.results.append(self.options._parse('attribute'))
        self.results.append(self.options._parse('method()'))
        self.results.append(self.options._parse('method("--proxy 10.10.1.3:2345")'))
        self.results.append(self.options._parse('method(";arg1")'))
        self.results.append(self.options._parse('method  (   "arg1"  ,    2    ,"arg2"   )'))
        self.results.append(self.options._parse("method('arg1')"))
        verify_all('Selenium options string to dict', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_parse_options_string_errors(self):
        self.results.append(self.error_formatter(self.options._parse, 'method("arg1)', True))
        self.results.append(self.error_formatter(self.options._parse, 'method(arg1")', True))
        self.results.append(self.error_formatter(self.options._parse, 'method(arg1)', True))
        self.results.append(self.error_formatter(self.options._parse, 'attribute=arg1', True))
        self.results.append(self.error_formatter(self.options._parse, 'attribute=webdriver', True))
        self.results.append(self.error_formatter(self.options._parse, 'method(argument="value")', True))
        self.results.append(self.error_formatter(self.options._parse, 'method({"key": "value"})', True))
        verify_all('Selenium options string errors', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_split_options(self):
        self.results.append(self.options._split('method("arg1");method("arg2")'))
        self.results.append(self.options._split('method("arg1")'))
        self.results.append(self.options._split('attribute=True'))
        self.results.append(self.options._split('attribute="semi;colons;middle";other_attribute=True'))
        self.results.append(self.options._split('method("arg1;");method(";arg2;")'))
        self.results.append(self.options._split(' method ( " arg1 ") ; method ( " arg2 " ) '))
        verify_all('Selenium options string splitting', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_options_create(self):
        options = 'add_argument("--disable-dev-shm-usage")'
        sel_options = self.options.create('chrome', options)
        self.results.append(sel_options.arguments)

        options = '%s;add_argument("--headless")' % options
        sel_options = self.options.create('chrome', options)
        self.results.append(sel_options.arguments)

        options = '%s;add_argument("--proxy-server=66.97.38.58:80")' % options
        sel_options = self.options.create('chrome', options)
        self.results.append(sel_options.arguments)

        options = '%s;binary_location("too", "many", "args")' % options
        try:
            self.options.create('chrome', options)
        except Exception as error:
            self.results.append(error.__str__()[:7])

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--disable-dev-shm-usage')
        sel_options = self.options.create('chrome', chrome_options)
        self.results.append(sel_options.arguments)

        sel_options = self.options.create('chrome', None)
        self.results.append(sel_options)

        sel_options = self.options.create('chrome', 'None')
        self.results.append(sel_options)

        verify_all('Selenium options', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_create_with_android(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option('androidPackage', 'com.android.chrome')
        sel_options = self.options.create('android', chrome_options)
        self.results.append([sel_options.arguments, sel_options.experimental_options])
        verify_all('Selenium options with android', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_get_options(self):
        options = 'add_argument("--proxy-server=66.97.38.58:80")'
        sel_options = self.options.create('chrome', options)
        self.results.append(sel_options.arguments)
        verify_all('Selenium options with string.', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_importer(self):
        self.results.append(self.options._import_options('firefox'))
        self.results.append(self.options._import_options('headless_firefox'))
        self.results.append(self.options._import_options('chrome'))
        self.results.append(self.options._import_options('headless_chrome'))
        self.results.append(self.options._import_options('ie'))
        self.results.append(self.options._import_options('opera'))
        self.results.append(self.options._import_options('edge'))
        self.results.append(self.error_formatter(self.options._import_options, 'phantomjs'))
        self.results.append(self.error_formatter(self.options._import_options, 'safari'))
        self.results.append(self.error_formatter(self.options._import_options, 'htmlunit'))
        self.results.append(self.error_formatter(self.options._import_options, 'htmlunit_with_js'))
        self.results.append(self.options._import_options('android'))
        self.results.append(self.error_formatter(self.options._import_options, 'iphone'))
        verify_all('Selenium options import', self.results, reporter=self.reporter)

    def error_formatter(self, method, arg, full=False):
        try:
            return method(arg)
        except Exception as error:
            if full:
                return '%s %s' % (arg, error)
            return '%s %s' % (arg, error.__str__()[:15])


class UsingSeleniumOptionsTests(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        curr_dir = os.path.dirname(os.path.abspath(__file__))
        cls.output_dir = os.path.abspath(
            os.path.join(curr_dir, '..', '..', 'output_dir'))
        cls.creator = WebDriverCreator(cls.output_dir)

    def tearDown(self):
        unstub()

    def test_create_chrome_with_options(self):
        options = mock()
        expected_webdriver = mock()
        when(webdriver).Chrome(service_log_path=None, options=options).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_chrome_with_options_and_remote_url(self):
        url = 'http://localhost:4444/wd/hub'
        caps = webdriver.DesiredCapabilities.CHROME.copy()
        options = mock()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               desired_capabilities=caps,
                               browser_profile=None, options=options,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_chrome({}, url, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_headless_chrome_with_options(self):
        options = mock()
        expected_webdriver = mock()
        when(webdriver).Chrome(service_log_path=None, options=options).thenReturn(expected_webdriver)
        driver = self.creator.create_headless_chrome({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_firefox_with_options(self):
        log_file = os.path.join(self.output_dir, 'geckodriver-1.log')
        options = mock()
        profile = mock()
        expected_webdriver = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        when(webdriver).Firefox(options=options, firefox_profile=profile,
                                service_log_path=log_file).thenReturn(expected_webdriver)
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        driver = self.creator.create_firefox({}, None, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_firefox_with_options_and_remote_url(self):
        url = 'http://localhost:4444/wd/hub'
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        caps = webdriver.DesiredCapabilities.FIREFOX.copy()
        options = mock()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               desired_capabilities=caps,
                               browser_profile=profile, options=options,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_firefox({}, url, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_headless_firefox_with_options(self):
        log_file = os.path.join(self.output_dir, 'geckodriver-1.log')
        options = mock()
        profile = mock()
        expected_webdriver = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        when(webdriver).Firefox(options=options, firefox_profile=profile,
                                service_log_path=log_file).thenReturn(expected_webdriver)
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        driver = self.creator.create_headless_firefox({}, None, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_ie_with_options(self):
        options = mock()
        expected_webdriver = mock()
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        when(self.creator)._has_options(ANY).thenReturn(True)
        when(webdriver).Ie(service_log_path=None, options=options).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_ie_with_options_and_remote_url(self):
        url = 'http://localhost:4444/wd/hub'
        caps = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
        options = mock()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               desired_capabilities=caps,
                               browser_profile=None, options=options,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({}, url, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_ie_with_options_and_log_path(self):
        options = mock()
        expected_webdriver = mock()
        when(self.creator)._has_service_log_path(ANY).thenReturn(False)
        when(self.creator)._has_options(ANY).thenReturn(True)
        when(webdriver).Ie(options=options).thenReturn(expected_webdriver)
        driver = self.creator.create_ie({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_has_options(self):
        self.assertTrue(self.creator._has_options(webdriver.Chrome))
        self.assertTrue(self.creator._has_options(webdriver.Firefox))
        self.assertTrue(self.creator._has_options(webdriver.Ie))
        self.assertFalse(self.creator._has_options(webdriver.Edge))
        self.assertTrue(self.creator._has_options(webdriver.Opera))
        self.assertFalse(self.creator._has_options(webdriver.Safari))

    @unittest.skipIf('options' not in inspect.getargspec(webdriver.Edge.__init__), "Requires Selenium 4.0.")
    def test_create_edge_with_options(self):
        # TODO: This test requires Selenium 4.0 in Travis
        options = mock()
        expected_webdriver = mock()
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        when(self.creator)._has_options(ANY).thenReturn(True)
        when(webdriver).Edge(service_log_path=None, options=options).thenReturn(expected_webdriver)
        driver = self.creator.create_edge({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_opera_with_options(self):
        options = mock()
        expected_webdriver = mock()
        when(webdriver).Opera(options=options, service_log_path=None).thenReturn(expected_webdriver)
        driver = self.creator.create_opera({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_opera_with_options_and_remote_url(self):
        url = 'http://localhost:4444/wd/hub'
        caps = webdriver.DesiredCapabilities.OPERA.copy()
        options = mock()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor=url,
                               desired_capabilities=caps,
                               browser_profile=None, options=options,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_opera({}, url, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_safari_no_options_support(self):
        options = mock()
        expected_webdriver = mock()
        when(webdriver).Safari().thenReturn(expected_webdriver)
        driver = self.creator.create_safari({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_phantomjs_no_options_support(self):
        options = mock()
        expected_webdriver = mock()
        when(webdriver).PhantomJS(service_log_path=None).thenReturn(expected_webdriver)
        driver = self.creator.create_phantomjs({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_htmlunit_no_options_support(self):
        caps = webdriver.DesiredCapabilities.HTMLUNIT.copy()
        options = mock()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=options,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit({'desired_capabilities': caps}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_htmlunit_with_js_no_options_support(self):
        caps = webdriver.DesiredCapabilities.HTMLUNITWITHJS.copy()
        options = mock()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=options,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_htmlunit_with_js({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_android_options_support(self):
        caps = webdriver.DesiredCapabilities.ANDROID.copy()
        options = mock()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=options,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_android({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_iphone_options_support(self):
        caps = webdriver.DesiredCapabilities.IPHONE.copy()
        options = mock()
        expected_webdriver = mock()
        file_detector = self.mock_file_detector()
        when(webdriver).Remote(command_executor='None',
                               desired_capabilities=caps,
                               browser_profile=None, options=options,
                               file_detector=file_detector).thenReturn(expected_webdriver)
        driver = self.creator.create_iphone({}, None, options=options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_driver_chrome(self):
        str_options = 'add_argument:--disable-dev-shm-usage'
        options = mock()
        expected_webdriver = mock()
        when(self.creator.selenium_options).create('chrome', str_options).thenReturn(options)
        when(webdriver).Chrome(service_log_path=None, options=options).thenReturn(expected_webdriver)
        driver = self.creator.create_driver('Chrome', desired_capabilities={}, remote_url=None,
                                            options=str_options)
        self.assertEqual(driver, expected_webdriver)

    def test_create_driver_firefox(self):
        log_file = os.path.join(self.output_dir, 'geckodriver-1.log')
        str_options = 'add_argument:--disable-dev-shm-usage'
        options = mock()
        profile = mock()
        when(webdriver).FirefoxProfile().thenReturn(profile)
        expected_webdriver = mock()
        when(self.creator.selenium_options).create('firefox', str_options).thenReturn(options)
        when(self.creator)._has_service_log_path(ANY).thenReturn(True)
        when(webdriver).Firefox(options=options, firefox_profile=profile,
                                service_log_path=log_file).thenReturn(expected_webdriver)
        driver = self.creator.create_driver('FireFox', desired_capabilities={}, remote_url=None,
                                            options=str_options)
        self.assertEqual(driver, expected_webdriver)

    def mock_file_detector(self):
        file_detector = mock()
        when(self.creator)._get_sl_file_detector().thenReturn(file_detector)
        return file_detector
