import inspect
import os
import unittest

import pytest
from approvaltests.approvals import verify_all
from approvaltests.reporters.generic_diff_reporter_factory import (
    GenericDiffReporterFactory,
)
from mockito import mock, when, unstub, ANY
from robot.utils import WINDOWS
from selenium import webdriver

from SeleniumLibrary.keywords.webdrivertools import SeleniumOptions, WebDriverCreator


@pytest.fixture(scope="module")
def options():
    return SeleniumOptions()


@pytest.fixture(scope="module")
def reporter():
    path = os.path.dirname(__file__)
    reporter_json = os.path.abspath(
        os.path.join(path, "..", "approvals_reporters.json")
    )
    factory = GenericDiffReporterFactory()
    factory.load(reporter_json)
    return factory.get_first_working()


def teardown_function():
    unstub()


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_parse_options_string(options, reporter):
    results = []
    results.append(options._parse('method("arg1")'))
    results.append(options._parse('method("arg1", "arg2")'))
    results.append(options._parse("method(True)"))
    results.append(options._parse("method(1)"))
    results.append(options._parse('method("arg1", 2, None, False, "arg2")'))
    results.append(options._parse('method ( " arg1 " , 2 , None , False , " arg2 " )'))
    results.append(options._parse('attribute="arg1"'))
    results.append(options._parse("  attribute = True  "))
    results.append(options._parse('method("arg1");attribute=True'))
    results.append(options._parse('method("arg1") ; attribute=True ; method("arg2")'))
    results.append(options._parse("attribute"))
    results.append(options._parse("method()"))
    results.append(options._parse("method(None)"))
    results.append(options._parse('method("--proxy 10.10.1.3:2345")'))
    results.append(options._parse('method(";arg1")'))
    results.append(options._parse('method  (   "arg1"  ,    2    ,"arg2"   )'))
    results.append(options._parse("method('arg1')"))
    results.append(
        options._parse(
            'add_argument("-profile"); add_argument("C:\\\\path\\to\\\\profile")'
        )
    )
    results.append(
        options._parse(
            r'add_argument("-profile"); add_argument("C:\\path\\to\\profile")'
        )
    )
    results.append(options._parse("attribute=None"))
    results.append(
        options._parse(
            'method("foo", {"key": False});attribute=True;method("bar", {"key": None})'
        )
    )
    verify_all("Selenium options string to dict", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_index_of_separator(options, reporter):
    results = []
    results.append(options._get_arument_index('method({"key": "value"})'))
    results.append(options._get_arument_index('attribute={"key": "value"}'))
    results.append(options._get_arument_index('method(foo={"key": "value"})'))
    results.append(options._get_arument_index('attribute=("value1", "value2")'))
    verify_all("Get argument index", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_parse_complex_object(options, reporter):
    results = []
    results.append(options._parse_to_tokens('method({"key": "value"})'))
    results.append(options._parse_to_tokens('attribute={"key": "value"}'))
    results.append(options._parse_to_tokens('attribute=("value1", "value2")'))
    results.append(options._parse_to_tokens('method("foo", {"key": "value"})'))
    verify_all("Parse complex Python object", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_parse_arguemnts(options, reporter):
    results = []
    results.append(options._parse_arguments(("arg1",), True))
    results.append(options._parse_arguments("arg1", False))
    results.append(options._parse_arguments({"key": "value"}, False))
    results.append(options._parse_arguments(["value1", "value2"], False))
    results.append(options._parse_arguments(("foo", {"key": "value"}), False))
    verify_all("Parse arguments from complex object", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_parse_options_string_errors(options, reporter):
    results = []
    results.append(error_formatter(options._parse, 'method("arg1)', True))
    results.append(error_formatter(options._parse, 'method(arg1")', True))
    results.append(error_formatter(options._parse, "method(arg1)", True))
    results.append(error_formatter(options._parse, "attribute=arg1", True))
    results.append(error_formatter(options._parse, "attribute=webdriver", True))
    results.append(error_formatter(options._parse, 'method(argument="value")', True))
    verify_all("Selenium options string errors", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_split_options(options, reporter):
    results = []
    results.append(options._split('method("arg1");method("arg2")'))
    results.append(options._split('method("arg1")'))
    results.append(options._split("attribute=True"))
    results.append(
        options._split('attribute="semi;colons;middle";other_attribute=True')
    )
    results.append(options._split('method("arg1;");method(";arg2;")'))
    results.append(options._split(' method ( " arg1 ") ; method ( " arg2 " ) '))
    verify_all("Selenium options string splitting", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_options_create(options, reporter):
    results = []
    options_str = 'add_argument("--disable-dev-shm-usage")'
    sel_options = options.create("chrome", options_str)
    results.append(sel_options.arguments)

    options_str = f'{options_str};add_argument("--headless")'
    sel_options = options.create("chrome", options_str)
    results.append(sel_options.arguments)

    options_str = f'{options_str};add_argument("--proxy-server=66.97.38.58:80")'
    sel_options = options.create("chrome", options_str)
    results.append(sel_options.arguments)

    options_str = f'{options_str};binary_location("too", "many", "args")'
    try:
        options.create("chrome", options_str)
    except Exception as error:
        results.append(error.__str__()[:7])

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument("--disable-dev-shm-usage")
    sel_options = options.create("chrome", chrome_options)
    results.append(sel_options.arguments)

    sel_options = options.create("chrome", None)
    results.append(sel_options)

    verify_all("Selenium options", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_create_with_android(options, reporter):
    results = []
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_experimental_option("androidPackage", "com.android.chrome")
    sel_options = options.create("android", chrome_options)
    results.append([sel_options.arguments, sel_options.experimental_options])
    verify_all("Selenium options with android", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_get_options(options, reporter):
    options_str = 'add_argument("--proxy-server=66.97.38.58:80")'
    sel_options = options.create("chrome", options_str)
    results = [sel_options.arguments]
    verify_all("Selenium options with string.", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_importer(options, reporter):
    results = []
    results.append(options._import_options("firefox"))
    results.append(options._import_options("headless_firefox"))
    results.append(options._import_options("chrome"))
    results.append(options._import_options("headless_chrome"))
    results.append(options._import_options("ie"))
    results.append(options._import_options("opera"))
    results.append(options._import_options("edge"))
    results.append(error_formatter(options._import_options, "phantomjs"))
    results.append(error_formatter(options._import_options, "safari"))
    results.append(error_formatter(options._import_options, "htmlunit"))
    results.append(error_formatter(options._import_options, "htmlunit_with_js"))
    results.append(options._import_options("android"))
    results.append(error_formatter(options._import_options, "iphone"))
    verify_all("Selenium options import", results, reporter=reporter)


def error_formatter(method, arg, full=False):
    try:
        return method(arg)
    except Exception as error:
        if full:
            return f"{arg} {error}"
        return "{} {}".format(arg, error.__str__()[:15])


@pytest.fixture(scope="module")
def creator():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", "output_dir"))
    return WebDriverCreator(output_dir)


@pytest.fixture(scope="module")
def output_dir():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", "output_dir"))
    return output_dir


def test_create_chrome_with_options(creator):
    options = mock()
    expected_webdriver = mock()
    when(webdriver).Chrome(
        service_log_path=None, options=options, executable_path="chromedriver"
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({}, None, options=options)
    assert driver == expected_webdriver


def test_create_chrome_with_options_and_remote_url(creator):
    url = "http://localhost:4444/wd/hub"
    caps = webdriver.DesiredCapabilities.CHROME.copy()
    options = mock()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        desired_capabilities=caps,
        browser_profile=None,
        options=options,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({}, url, options=options)
    assert driver == expected_webdriver


def test_create_headless_chrome_with_options(creator):
    options = mock()
    expected_webdriver = mock()
    when(webdriver).Chrome(
        service_log_path=None, options=options, executable_path="chromedriver"
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_chrome({}, None, options=options)
    assert driver == expected_webdriver


def test_create_firefox_with_options(creator, output_dir):
    log_file = os.path.join(output_dir, "geckodriver-1.log")
    options = mock()
    profile = mock()
    expected_webdriver = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    when(webdriver).Firefox(
        options=options,
        firefox_profile=profile,
        executable_path="geckodriver",
        service_log_path=log_file,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox({}, None, None, options=options)
    assert driver == expected_webdriver


def test_create_firefox_with_options_and_remote_url(creator):
    url = "http://localhost:4444/wd/hub"
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    caps = webdriver.DesiredCapabilities.FIREFOX.copy()
    options = mock()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        desired_capabilities=caps,
        browser_profile=profile,
        options=options,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox({}, url, None, options=options)
    assert driver == expected_webdriver


def test_create_headless_firefox_with_options(creator, output_dir):
    log_file = os.path.join(output_dir, "geckodriver-1.log")
    options = mock()
    profile = mock()
    expected_webdriver = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    when(webdriver).Firefox(
        options=options,
        firefox_profile=profile,
        executable_path="geckodriver",
        service_log_path=log_file,
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_firefox({}, None, None, options=options)
    assert driver == expected_webdriver


def test_create_ie_with_options(creator):
    options = mock()
    expected_webdriver = mock()
    when(webdriver).Ie(
        service_log_path=None, options=options, executable_path="IEDriverServer.exe"
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({}, None, options=options)
    assert driver == expected_webdriver


def test_create_ie_with_options_and_remote_url(creator):
    url = "http://localhost:4444/wd/hub"
    caps = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
    options = mock()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        desired_capabilities=caps,
        browser_profile=None,
        options=options,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({}, url, options=options)
    assert driver == expected_webdriver


def test_create_ie_with_options_and_log_path(creator):
    options = mock()
    expected_webdriver = mock()
    when(webdriver).Ie(
        options=options, service_log_path=None, executable_path="IEDriverServer.exe"
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({}, None, options=options)
    assert driver == expected_webdriver


def test_has_options(creator):
    assert creator._has_options(webdriver.Chrome)
    assert creator._has_options(webdriver.Firefox)
    assert creator._has_options(webdriver.Ie)
    assert creator._has_options(webdriver.Edge) is False
    assert creator._has_options(webdriver.Opera)
    assert creator._has_options(webdriver.Safari) is False


def test_create_opera_with_options(creator):
    options = mock()
    expected_webdriver = mock()
    executable_path = "operadriver"
    when(webdriver).Opera(
        options=options, service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_opera({}, None, options=options)
    assert driver == expected_webdriver


def test_create_opera_with_options_and_remote_url(creator):
    url = "http://localhost:4444/wd/hub"
    caps = webdriver.DesiredCapabilities.OPERA.copy()
    options = mock()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        desired_capabilities=caps,
        browser_profile=None,
        options=options,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_opera({}, url, options=options)
    assert driver == expected_webdriver


def test_create_safari_no_options_support(creator):
    options = mock()
    expected_webdriver = mock()
    executable_path = "/usr/bin/safaridriver"
    when(webdriver).Safari(executable_path=executable_path).thenReturn(
        expected_webdriver
    )
    driver = creator.create_safari({}, None, options=options)
    assert driver == expected_webdriver


def test_create_phantomjs_no_options_support(creator):
    options = mock()
    expected_webdriver = mock()
    executable_path = "phantomjs"
    when(webdriver).PhantomJS(
        service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_phantomjs({}, None, options=options)
    assert driver == expected_webdriver


def test_create_htmlunit_no_options_support(creator):
    caps = webdriver.DesiredCapabilities.HTMLUNIT.copy()
    options = mock()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=options,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_htmlunit(
        {"desired_capabilities": caps}, None, options=options
    )
    assert driver == expected_webdriver


def test_create_htmlunit_with_js_no_options_support(creator):
    caps = webdriver.DesiredCapabilities.HTMLUNITWITHJS.copy()
    options = mock()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=options,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_htmlunit_with_js({}, None, options=options)
    assert driver == expected_webdriver


def test_android_options_support(creator):
    caps = webdriver.DesiredCapabilities.ANDROID.copy()
    options = mock()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=options,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_android({}, None, options=options)
    assert driver == expected_webdriver


def test_iphone_options_support(creator):
    caps = webdriver.DesiredCapabilities.IPHONE.copy()
    options = mock()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=options,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_iphone({}, None, options=options)
    assert driver == expected_webdriver


def test_create_driver_chrome(creator):
    str_options = "add_argument:--disable-dev-shm-usage"
    options = mock()
    expected_webdriver = mock()
    when(creator.selenium_options).create("chrome", str_options).thenReturn(options)
    executable_path = "chromedriver"
    when(creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(webdriver).Chrome(
        service_log_path=None, options=options, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_driver(
        "Chrome", desired_capabilities={}, remote_url=None, options=str_options
    )
    assert driver == expected_webdriver


def test_create_driver_firefox(creator, output_dir):
    log_file = os.path.join(output_dir, "geckodriver-1.log")
    str_options = "add_argument:--disable-dev-shm-usage"
    options = mock()
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    expected_webdriver = mock()
    when(creator.selenium_options).create("firefox", str_options).thenReturn(options)
    executable_path = "geckodriver"
    when(creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(webdriver).Firefox(
        options=options,
        firefox_profile=profile,
        executable_path=executable_path,
        service_log_path=log_file,
    ).thenReturn(expected_webdriver)
    driver = creator.create_driver(
        "FireFox", desired_capabilities={}, remote_url=None, options=str_options
    )
    assert driver == expected_webdriver


def mock_file_detector(creator):
    file_detector = mock()
    when(creator)._get_sl_file_detector().thenReturn(file_detector)
    return file_detector
