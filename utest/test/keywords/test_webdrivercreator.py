import os

import pytest
from mockito import mock, verify, when, unstub, ANY
from selenium import webdriver

from SeleniumLibrary.keywords import WebDriverCreator

LOG_DIR = "/log/dir"


@pytest.fixture(scope="module")
def creator():
    return WebDriverCreator(LOG_DIR)


def teardown_function():
    unstub()


def test_normalise_browser_name(creator):
    browser = creator._normalise_browser_name("chrome")
    assert browser == "chrome"

    browser = creator._normalise_browser_name("ChrOmE")
    assert browser == "chrome"

    browser = creator._normalise_browser_name(" Ch rO mE ")
    assert browser == "chrome"


def test_get_creator_method(creator):
    method = creator._get_creator_method("chrome")
    assert method

    method = creator._get_creator_method("firefox")
    assert method

    with pytest.raises(ValueError) as error:
        creator._get_creator_method("foobar")
    assert "foobar is not a supported browser." in str(error.value)


def test_parse_capabilities(creator):
    caps = creator._parse_capabilities("key1:value1,key2:value2")
    expected = {"desired_capabilities": {"key1": "value1", "key2": "value2"}}
    assert caps == expected

    caps = creator._parse_capabilities("key1:value1,key2:value2", "ie")
    expected = {"capabilities": {"key1": "value1", "key2": "value2"}}
    assert caps == expected

    caps = creator._parse_capabilities("key1:value1,key2:value2", "firefox")
    assert caps == expected

    caps = creator._parse_capabilities("key1:value1,key2:value2", "ff")
    assert caps == expected

    caps = creator._parse_capabilities("key1:value1,key2:value2", "edge")
    assert caps == expected

    parsing_caps = expected.copy()
    caps = creator._parse_capabilities(parsing_caps)
    assert caps == {"desired_capabilities": expected}

    caps = creator._parse_capabilities("key1 : value1 , key2: value2")
    expected = {"desired_capabilities": {"key1": "value1", "key2": "value2"}}
    assert caps == expected

    caps = creator._parse_capabilities(" key 1 : value 1 , key2:value2")
    expected = {"desired_capabilities": {"key 1": "value 1", "key2": "value2"}}
    assert caps == expected

    caps = creator._parse_capabilities("")
    assert caps == {}

    caps = creator._parse_capabilities({})
    assert caps == {}

    caps = creator._parse_capabilities(None)
    assert caps == {}

    for browser in [None, "safari", "headlesschrome", "foobar"]:
        caps = creator._parse_capabilities(
            {"key1": "value1", "key2": "value2"}, browser
        )
        expected = {"desired_capabilities": {"key1": "value1", "key2": "value2"}}
        assert caps == expected

    for browser in ["ie", "firefox", "edge"]:
        caps = creator._parse_capabilities(
            {"key1": "value1", "key2": "value2"}, browser
        )
        expected = {"capabilities": {"key1": "value1", "key2": "value2"}}
        assert caps == expected


def test_capabilities_resolver_firefox(creator):
    default_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    expected_caps = {
        "desired_capabilities": {"version": "66.02", "browserName": "firefox"}
    }
    caps_in = {"capabilities": {"version": "66.02"}}
    resolved_caps = creator._remote_capabilities_resolver(caps_in, default_capabilities)
    assert resolved_caps == expected_caps

    caps_in = {"capabilities": {"version": "66.02", "browserName": "firefox"}}
    resolved_caps = creator._remote_capabilities_resolver(caps_in, default_capabilities)
    assert resolved_caps == expected_caps


def test_capabilities_resolver_no_set_caps(creator):
    default_capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    resolved_caps = creator._remote_capabilities_resolver({}, default_capabilities)
    assert resolved_caps == {"desired_capabilities": default_capabilities}


def test_capabilities_resolver_chrome(creator):
    default_capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    expected_caps = {
        "desired_capabilities": {"version": "73.0.3683.86", "browserName": "chrome"}
    }
    resolved_caps = creator._remote_capabilities_resolver(
        {"capabilities": {"version": "73.0.3683.86"}}, default_capabilities
    )
    assert resolved_caps == expected_caps

    caps_in = {
        "desired_capabilities": {"version": "73.0.3683.86", "browserName": "chrome"}
    }
    resolved_caps = creator._remote_capabilities_resolver(caps_in, default_capabilities)
    assert resolved_caps == expected_caps


def test_chrome(creator):
    expected_webdriver = mock()
    when(webdriver).Chrome(
        options=None, service_log_path=None, executable_path="chromedriver"
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({}, None)
    assert driver == expected_webdriver


def test_chrome_with_desired_capabilities(creator):
    expected_webdriver = mock()
    when(webdriver).Chrome(
        desired_capabilities={"key": "value"},
        options=None,
        service_log_path=None,
        executable_path="chromedriver",
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({"desired_capabilities": {"key": "value"}}, None)
    assert driver == expected_webdriver


def test_chrome_remote_no_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({}, url)
    assert driver == expected_webdriver


def test_chrome_remote_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "chrome"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({"desired_capabilities": capabilities}, url)
    assert driver == expected_webdriver


def test_chrome_remote_caps_no_browser_name(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "chrome", "key": "value"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({"desired_capabilities": {"key": "value"}}, url)
    assert driver == expected_webdriver


def test_chrome_healdless(creator):
    expected_webdriver = mock()
    options = mock()
    when(webdriver).ChromeOptions().thenReturn(options)
    when(webdriver).Chrome(
        options=options, service_log_path=None, executable_path="chromedriver"
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_chrome({}, None)
    assert options.headless is True
    assert driver == expected_webdriver


def test_chrome_healdless_with_grid(creator):
    expected_webdriver = mock()
    options = mock()
    when(webdriver).ChromeOptions().thenReturn(options)
    remote_url = "localhost:4444"
    capabilities = webdriver.DesiredCapabilities.CHROME.copy()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=remote_url,
        options=options,
        browser_profile=None,
        desired_capabilities=capabilities,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_chrome({}, remote_url)
    assert options.headless is True
    assert driver == expected_webdriver


def test_firefox(creator):
    expected_webdriver = mock()
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    log_file = get_geckodriver_log()
    when(webdriver).Firefox(
        options=None,
        firefox_profile=profile,
        executable_path="geckodriver",
        service_log_path=log_file,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox({}, None, None)
    assert driver == expected_webdriver
    verify(webdriver).FirefoxProfile()


def test_get_ff_profile_real_path(creator):
    profile_path = "/path/to/profile"
    profile_mock = mock()
    when(webdriver).FirefoxProfile(profile_path).thenReturn(profile_mock)
    profile = creator._get_ff_profile(profile_path)
    assert profile == profile_mock


def test_get_ff_profile_no_path(creator):
    profile_mock = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile_mock)
    profile = creator._get_ff_profile(None)
    assert profile == profile_mock


def test_get_ff_profile_instance_FirefoxProfile(creator):
    input_profile = webdriver.FirefoxProfile()
    profile = creator._get_ff_profile(input_profile)
    assert profile == input_profile


def test_firefox_remote_no_caps(creator):
    url = "http://localhost:4444/wd/hub"
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    expected_webdriver = mock()
    capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=profile,
        options=None,
        desired_capabilities=capabilities,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox({}, url, None)
    assert driver == expected_webdriver


def test_firefox_remote_caps(creator):
    url = "http://localhost:4444/wd/hub"
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    expected_webdriver = mock()
    capabilities = {"browserName": "firefox"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=profile,
        options=None,
        desired_capabilities=capabilities,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox({"desired_capabilities": capabilities}, url, None)
    assert driver == expected_webdriver


def test_firefox_remote_caps_no_browsername(creator):
    url = "http://localhost:4444/wd/hub"
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    expected_webdriver = mock()
    capabilities = {"browserName": "firefox", "version": "66.02"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=profile,
        options=None,
        desired_capabilities=capabilities,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox({"capabilities": {"version": "66.02"}}, url, None)
    assert driver == expected_webdriver


def test_firefox_profile(creator):
    expected_webdriver = mock()
    profile = mock()
    profile_dir = "/profile/dir"
    when(webdriver).FirefoxProfile(profile_dir).thenReturn(profile)
    log_file = get_geckodriver_log()
    when(webdriver).Firefox(
        options=None,
        service_log_path=log_file,
        executable_path="geckodriver",
        firefox_profile=profile,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox({}, None, profile_dir)
    assert driver == expected_webdriver


def test_firefox_headless(creator):
    expected_webdriver = mock()
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    log_file = get_geckodriver_log()
    when(webdriver).Firefox(
        options=options,
        service_log_path=log_file,
        executable_path="geckodriver",
        firefox_profile=profile,
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_firefox({}, None, None)
    assert driver == expected_webdriver


def test_firefox_headless_with_grid_caps(creator):
    expected_webdriver = mock()
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    remote_url = "localhost:4444"
    capabilities = {"browserName": "firefox", "key": "value"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=remote_url,
        options=options,
        desired_capabilities=capabilities,
        browser_profile=profile,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_firefox(
        {"capabilities": {"key": "value"}}, remote_url, None
    )
    assert driver == expected_webdriver
    assert options.headless is True


def test_firefox_headless_with_grid_no_caps(creator):
    expected_webdriver = mock()
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    remote_url = "localhost:4444"
    capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=remote_url,
        options=options,
        desired_capabilities=capabilities,
        browser_profile=profile,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_firefox({}, remote_url, None)
    assert driver == expected_webdriver
    assert options.headless is True


def test_ie(creator):
    expected_webdriver = mock()
    when(webdriver).Ie(
        options=None, service_log_path=None, executable_path="IEDriverServer.exe"
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({}, None)
    assert driver == expected_webdriver

    when(webdriver).Ie(
        capabilities={"key": "value"},
        options=None,
        service_log_path=None,
        executable_path="IEDriverServer.exe",
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie(
        desired_capabilities={"capabilities": {"key": "value"}},
        remote_url=None,
        options=None,
        service_log_path=None,
    )
    assert driver == expected_webdriver


def test_ie_remote_no_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = webdriver.DesiredCapabilities.INTERNETEXPLORER.copy()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({}, url)
    assert driver == expected_webdriver


def test_ie_remote_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "internet explorer"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({"capabilities": capabilities}, url)
    assert driver == expected_webdriver


def test_ie_no_browser_name(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "internet explorer", "key": "value"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({"capabilities": {"key": "value"}}, url)
    assert driver == expected_webdriver


def test_edge(creator):
    executable_path = "MicrosoftWebDriver.exe"
    expected_webdriver = mock()
    when(webdriver).Edge(
        service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    when(creator)._has_options(ANY).thenReturn(False)
    driver = creator.create_edge({}, None)
    assert driver == expected_webdriver


def test_edge_remote_no_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = webdriver.DesiredCapabilities.EDGE.copy()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_edge({}, url)
    assert driver == expected_webdriver


def test_edge_remote_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "MicrosoftEdge"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_edge({"capabilities": capabilities}, url)
    assert driver == expected_webdriver


def test_edge_no_browser_name(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "MicrosoftEdge", "key": "value"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_edge({"capabilities": {"key": "value"}}, url)
    assert driver == expected_webdriver


def test_opera(creator):
    expected_webdriver = mock()
    executable_path = "operadriver"
    when(webdriver).Opera(
        options=None, service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_opera({}, None)
    assert driver == expected_webdriver


def test_opera_remote_no_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = webdriver.DesiredCapabilities.OPERA.copy()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_opera({}, url)
    assert driver == expected_webdriver


def test_opera_remote_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "opera"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_opera({"desired_capabilities": capabilities}, url)
    assert driver == expected_webdriver


def test_opera_no_browser_name(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "opera", "key": "value"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_opera({"desired_capabilities": {"key": "value"}}, url)
    assert driver == expected_webdriver


def test_safari(creator):
    expected_webdriver = mock()
    executable_path = "/usr/bin/safaridriver"
    when(webdriver).Safari(executable_path=executable_path).thenReturn(
        expected_webdriver
    )
    driver = creator.create_safari({}, None)
    assert driver == expected_webdriver


def test_safari_remote_no_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    capabilities = webdriver.DesiredCapabilities.SAFARI.copy()
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_safari({}, url)
    assert driver == expected_webdriver


def test_safari_remote_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "safari"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_safari({"desired_capabilities": capabilities}, url)
    assert driver == expected_webdriver


def test_safari_no_broser_name(creator):
    file_detector = mock_file_detector(creator)
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "safari", "key": "value"}
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_safari({"desired_capabilities": {"key": "value"}}, url)
    assert driver == expected_webdriver


def test_phantomjs(creator):
    expected_webdriver = mock()
    executable_path = "phantomjs"
    when(webdriver).PhantomJS(
        service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_phantomjs({}, None)
    assert driver == expected_webdriver


def test_phantomjs_remote_no_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = webdriver.DesiredCapabilities.PHANTOMJS.copy()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_phantomjs({}, url)
    assert driver == expected_webdriver


def test_phantomjs_remote_caps(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "phantomjs"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_phantomjs({"desired_capabilities": capabilities}, url)
    assert driver == expected_webdriver


def test_phantomjs_no_browser_name(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = {"browserName": "phantomjs", "key": "value"}
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=None,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_phantomjs({"desired_capabilities": {"key": "value"}}, url)
    assert driver == expected_webdriver


def test_htmlunit_no_caps(creator):
    caps = webdriver.DesiredCapabilities.HTMLUNIT
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_htmlunit({}, None)
    assert driver == expected_webdriver


def test_htmlunit_remote_caps(creator):
    caps = {"browserName": "htmlunit"}
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_htmlunit({"desired_capabilities": caps}, None)
    assert driver == expected_webdriver


def test_htmlunit_no_browser_name(creator):
    capabilities = {"browserName": "htmlunit", "key": "value"}
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=capabilities,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_htmlunit({"desired_capabilities": {"key": "value"}}, None)
    assert driver == expected_webdriver


def test_htmlunit_with_js(creator):
    caps = webdriver.DesiredCapabilities.HTMLUNITWITHJS.copy()
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_htmlunit_with_js({}, None)
    assert driver == expected_webdriver


def test_htmlunit_with_js_no_browser_name(creator):
    capabilities = {"browserName": "htmlunit", "key": "value"}
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=capabilities,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_htmlunit_with_js(
        {"desired_capabilities": {"key": "value"}}, None
    )
    assert driver == expected_webdriver


def test_android(creator):
    caps = webdriver.DesiredCapabilities.ANDROID
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_android({}, None)
    assert driver == expected_webdriver


def test_android_no_browser_name(creator):
    capabilities = {"browserName": "android", "key": "value"}
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=capabilities,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_android({"desired_capabilities": {"key": "value"}}, None)
    assert driver == expected_webdriver


def test_iphone(creator):
    caps = webdriver.DesiredCapabilities.IPHONE
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=caps,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_iphone({}, None)
    assert driver == expected_webdriver


def test_iphone_no_browser_name(creator):
    capabilities = {"browserName": "iPhone", "key": "value"}
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor="None",
        desired_capabilities=capabilities,
        browser_profile=None,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_iphone({"desired_capabilities": {"key": "value"}}, None)
    assert driver == expected_webdriver


def test_create_driver_chrome(creator):
    expected_webdriver = mock()
    executable_path = "chromedriver"
    when(creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(webdriver).Chrome(
        options=None, service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    for browser in ["chrome", "googlechrome", "gc"]:
        driver = creator.create_driver(browser, None, None)
        assert driver == expected_webdriver


def test_create_driver_firefox(creator):
    expected_webdriver = mock()
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    log_file = get_geckodriver_log()
    executable_path = "geckodriver"
    when(creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(webdriver).Firefox(
        options=None,
        service_log_path=log_file,
        executable_path=executable_path,
        firefox_profile=profile,
    ).thenReturn(expected_webdriver)
    for browser in ["ff", "firefox"]:
        driver = creator.create_driver(browser, None, None, None)
        assert driver == expected_webdriver


def test_create_driver_ie(creator):
    expected_webdriver = mock()
    executable_path = "IEDriverServer.exe"
    when(creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(webdriver).Ie(
        options=None, service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    for browser in ["ie", "Internet Explorer"]:
        driver = creator.create_driver(browser, None, None)
        assert driver == expected_webdriver


def get_geckodriver_log():
    return os.path.join(LOG_DIR, "geckodriver-1.log")


def mock_file_detector(creator):
    file_detector = mock()
    when(creator)._get_sl_file_detector().thenReturn(file_detector)
    return file_detector
