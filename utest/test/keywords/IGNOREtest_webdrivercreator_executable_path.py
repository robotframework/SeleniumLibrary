import os

import pytest
from mockito import mock, unstub, when, ANY
from selenium import webdriver

from SeleniumLibrary.keywords import WebDriverCreator


LOG_DIR = "/log/dir"


@pytest.fixture(scope="module")
def creator():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", "output_dir"))
    return WebDriverCreator(output_dir)


def teardown_function():
    unstub()


def test_create_chrome_executable_path_set(creator):
    expected_webdriver = mock()
    when(webdriver).Chrome(
        options=None, service=ANY,  # service_log_path=None, executable_path="/path/to/chromedriver"
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({}, None, executable_path="/path/to/chromedriver")
    assert driver == expected_webdriver


def test_create_chrome_executable_path_not_set(creator):
    expected_webdriver = mock()
    when(webdriver).Chrome(
        options=None, service=ANY,  # service_log_path=None, executable_path="chromedriver"
    ).thenReturn(expected_webdriver)
    when(creator)._get_executable_path(ANY).thenReturn("chromedriver")
    driver = creator.create_chrome({}, None, executable_path=None)
    assert driver == expected_webdriver


# def test_get_executable_path(creator):
#     executable_path = creator._get_executable_path(webdriver.Chrome)
#     assert executable_path == "chromedriver"

#     executable_path = creator._get_executable_path(webdriver.Firefox)
#     assert executable_path == "geckodriver"

#     executable_path = creator._get_executable_path(webdriver.Ie)
#     assert executable_path == "IEDriverServer.exe"

#     executable_path = creator._get_executable_path(webdriver.Edge)
#     assert executable_path == "msedgedriver"


def test_create_chrome_executable_path_and_remote(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    file_detector = mock_file_detector(creator)
    when(webdriver).Remote(
        command_executor=url,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_chrome({}, url, executable_path="/path/to/chromedriver")
    assert driver == expected_webdriver


def test_create_heasless_chrome_executable_path_set(creator):
    expected_webdriver = mock()
    options = mock()
    when(webdriver).ChromeOptions().thenReturn(options)
    when(webdriver).Chrome(
        options=options, service = ANY  # service_log_path=None, executable_path="/path/to/chromedriver"
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_chrome(
        {}, None, executable_path="/path/to/chromedriver"
    )
    assert driver == expected_webdriver


def test_create_firefox_executable_path_set(creator):
    executable = "/path/to/geckodriver"
    expected_webdriver = mock()
    # profile = mock()
    # when(webdriver).FirefoxProfile().thenReturn(profile)
    # log_file = get_geckodriver_log()
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    log_file = None
    when(webdriver).Firefox(
        options=options,
        # firefox_profile=profile,
        service = ANY,
        # service_log_path=log_file,
        # executable_path=executable,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox(
        {}, None, None, service_log_path=log_file, executable_path=executable
    )
    assert driver == expected_webdriver


def test_create_firefox_executable_path_not_set(creator):
    executable = "geckodriver"
    expected_webdriver = mock()
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    log_file = get_geckodriver_log()
    when(creator)._get_executable_path(ANY).thenReturn(executable)
    when(webdriver).Firefox(
        options=None,
        # firefox_profile=profile,
        service=ANY,
        # service_log_path=log_file,
        # executable_path=executable,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox(
        {}, None, None, service_log_path=log_file, executable_path=None
    )
    assert driver == expected_webdriver


def test_create_firefox_executable_path_and_remote(creator):
    url = "http://localhost:4444/wd/hub"
    expected_webdriver = mock()
    capabilities = webdriver.DesiredCapabilities.FIREFOX.copy()
    file_detector = mock_file_detector(creator)
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    when(webdriver).Remote(
        command_executor=url,
        browser_profile=profile,
        desired_capabilities=capabilities,
        options=None,
        file_detector=file_detector,
    ).thenReturn(expected_webdriver)
    driver = creator.create_firefox(
        {}, url, None, executable_path="/path/to/chromedriver"
    )
    assert driver == expected_webdriver


def test_create_headless_firefox_executable_path_set(creator):
    executable = "/path/to/geckodriver"
    expected_webdriver = mock()
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    log_file = get_geckodriver_log()
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    when(webdriver).Firefox(
        options=options,
        firefox_profile=profile,
        service_log_path=log_file,
        executable_path=executable,
    ).thenReturn(expected_webdriver)
    driver = creator.create_headless_firefox(
        {}, None, None, service_log_path=log_file, executable_path=executable
    )
    assert driver == expected_webdriver


def test_create_ie_executable_path_set(creator):
    executable_path = "/path/to/IEDriverServer.exe"
    expected_webdriver = mock()
    when(webdriver).Ie(
        options=None, service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({}, None, executable_path=executable_path)
    assert driver == expected_webdriver


def test_create_ie_executable_path_not_set(creator):
    executable_path = "IEDriverServer.exe"
    expected_webdriver = mock()
    when(creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(webdriver).Ie(
        options=None, service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_ie({}, None, executable_path=None)
    assert driver == expected_webdriver


def test_create_edge_executable_path_set(creator):
    executable_path = "/path/to/msedgedriver"
    expected_webdriver = mock()
    when(creator)._has_options(ANY).thenReturn(False)
    when(webdriver).Edge(
        service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_edge({}, None, executable_path=executable_path)
    assert driver == expected_webdriver


def test_create_edge_executable_path_not_set(creator):
    executable_path = "msedgedriver"
    expected_webdriver = mock()
    when(creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(creator)._has_options(ANY).thenReturn(False)
    when(webdriver).Edge(
        service_log_path=None, executable_path=executable_path
    ).thenReturn(expected_webdriver)
    driver = creator.create_edge({}, None, executable_path=None)
    assert driver == expected_webdriver


def test_create_safari_executable_path_set(creator):
    executable_path = "/path/to/safaridriver"
    expected_webdriver = mock()
    when(webdriver).Safari(executable_path=executable_path).thenReturn(
        expected_webdriver
    )
    driver = creator.create_safari({}, None, executable_path=executable_path)
    assert driver == expected_webdriver


def test_create_safari_executable_path_not_set(creator):
    executable_path = "/usr/bin/safaridriver"
    expected_webdriver = mock()
    when(creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(webdriver).Safari(executable_path=executable_path).thenReturn(
        expected_webdriver
    )
    driver = creator.create_safari({}, None, executable_path=None)
    assert driver == expected_webdriver


def test_open_browser_executable_path_set(creator):
    expected_webdriver = mock()
    when(webdriver).Chrome(
        options=None, service_log_path=None, executable_path="/path/to/chromedriver"
    ).thenReturn(expected_webdriver)
    driver = creator.create_driver(
        "Chrome", {}, None, executable_path="/path/to/chromedriver"
    )
    assert driver == expected_webdriver


def mock_file_detector(creator):
    file_detector = mock()
    when(creator)._get_sl_file_detector().thenReturn(file_detector)
    return file_detector


def get_geckodriver_log():
    # return os.path.join(LOG_DIR, "geckodriver-1.log")
    # print(f"{os.getcwd()}")
    cwd = os.getcwd()
    return cwd