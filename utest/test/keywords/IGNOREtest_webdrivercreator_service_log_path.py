import os
from collections import namedtuple

import pytest

from mockito import mock, when, unstub, ANY
from selenium import webdriver
from selenium.webdriver import chrome
#from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome import service as chromeservice

from SeleniumLibrary.keywords import WebDriverCreator
from SeleniumLibrary.utils import WINDOWS


@pytest.fixture(scope="module")
def creator():
    curr_dir = os.path.dirname(os.path.abspath(__file__))
    output_dir = os.path.abspath(os.path.join(curr_dir, "..", "..", "output_dir"))
    creator = WebDriverCreator(output_dir)
    Creator = namedtuple("Creator", "creator, output_dir")
    return Creator(creator, output_dir)


def teardown_function():
    unstub()


def test_no_log_file(creator):
    assert creator.creator._get_log_path(None) is None


def test_log_file_with_rf_file_separator(creator):
    log_file = "C:\\path\\to\\own_name.txt" if WINDOWS else "/path/to/own_name.txt"
    file_name = creator.creator._get_log_path(log_file)
    log_file = log_file.replace("/", os.sep)
    assert file_name == log_file


def test_log_file_with_index(creator):
    log_file = os.path.join(creator.output_dir, "firefox-{index}.log")
    file_name = creator.creator._get_log_path(log_file)
    assert file_name == log_file.format(index="1")


def test_log_file_with_index_exist(creator):
    log_file = os.path.join(creator.output_dir, "firefox-{index}.log")
    with open(
        os.path.join(creator.output_dir, log_file.format(index="1")), "w"
    ) as file:
        file.close()
    file_name = creator.creator._get_log_path(log_file)
    assert file_name == log_file.format(index="2")


def test_create_chrome_with_service_log_path_none(creator):
    expected_webdriver = mock()
    service = mock()
    when(chromeservice).Service(log_path=None, executable_path="chromedriver").thenReturn(service)
    # when(chrome).service(log_path=None, executable_path="chromedriver").thenReturn(service)
    # service = ChromeService(log_path=None, executable_path="chromedriver")
    # service = Service(log_path=None, executable_path="chromedriver")
    # service = mock()
    # when(webdriver).chrome.service().thenReturn(service)
    when(webdriver).Chrome(
        # options=None, service_log_path=None, executable_path="chromedriver"
        options=None, service=ANY,
        # options=None, service=service,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_chrome({}, None, service_log_path=None)
    assert driver == expected_webdriver


def test_create_chrome_with_service_log_path_real_path(creator):
    log_file = os.path.join(creator.output_dir, "firefox-{index}.log")
    expected_webdriver = mock()
    when(webdriver).Chrome(
        options=None, service=ANY,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_chrome({}, None, service_log_path=log_file)
    assert driver == expected_webdriver


def test_create_headlesschrome_with_service_log_path_real_path(creator):
    log_file = os.path.join(creator.output_dir, "firefox-{index}.log")
    expected_webdriver = mock()
    options = mock()
    when(webdriver).ChromeOptions().thenReturn(options)
    when(webdriver).Chrome(
        options=options, service=ANY,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_headless_chrome({}, None, service_log_path=log_file)
    assert driver == expected_webdriver


def test_create_firefox_with_service_log_path_none(creator):
    log_file = os.path.join(creator.output_dir, "geckodriver-1.log")
    expected_webdriver = mock()
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    when(webdriver).Firefox(
        options=options,
        service=ANY,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_firefox({}, None, None, service_log_path=None)
    assert driver == expected_webdriver


def test_create_firefox_with_service_log_path_real_path(creator):
    log_file = os.path.join(creator.output_dir, "firefox-{index}.log")
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    expected_webdriver = mock()
    when(webdriver).Firefox(
        options=options,
        service=ANY,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_firefox(
        {}, None, ff_profile_dir=None, service_log_path=log_file
    )
    assert driver == expected_webdriver


def test_create_headlessfirefox_with_service_log_path_real_path(creator):
    log_file = os.path.join(creator.output_dir, "firefox-{index}.log")
    expected_webdriver = mock()
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    when(webdriver).Firefox(
        options=options,
        service=ANY,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_headless_firefox(
        {}, None, ff_profile_dir=None, service_log_path=log_file
    )
    assert driver == expected_webdriver


def test_create_firefox_from_create_driver(creator):
    log_file = os.path.join(creator.output_dir, "firefox-1.log")
    expected_webdriver = mock()
    profile = mock()
    when(webdriver).FirefoxProfile().thenReturn(profile)
    options = mock()
    when(webdriver).FirefoxOptions().thenReturn(options)
    executable_path = "geckodriver"
    when(creator.creator)._get_executable_path(ANY).thenReturn(executable_path)
    when(webdriver).Firefox(
        options=options,
        service=ANY,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_driver(
        "firefox ", {}, remote_url=None, profile_dir=None, service_log_path=log_file
    )
    assert driver == expected_webdriver


def test_create_ie_with_service_log_path_real_path(creator):
    log_file = os.path.join(creator.output_dir, "ie-1.log")
    expected_webdriver = mock()
    when(webdriver).Ie(
        options=None, service=ANY,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_ie({}, None, service_log_path=log_file)
    assert driver == expected_webdriver


def test_create_edge_with_service_log_path_real_path(creator):
    executable_path = "msedgedriver"
    log_file = os.path.join(creator.output_dir, "edge-1.log")
    expected_webdriver = mock()
    when(webdriver).Edge(
        options=None, service=ANY,
    ).thenReturn(expected_webdriver)
    driver = creator.creator.create_edge({}, None, service_log_path=log_file)
    assert driver == expected_webdriver


# def test_create_safari_no_support_for_service_log_path(creator):
#     log_file = os.path.join(creator.output_dir, "safari-1.log")
#     expected_webdriver = mock()
#     executable_path = "/usr/bin/safaridriver"
#     when(webdriver).Safari(executable_path=executable_path).thenReturn(
#         expected_webdriver
#     )
#     driver = creator.creator.create_safari({}, None, service_log_path=log_file)
#     assert driver == expected_webdriver

# def test_create_safari_with_service_log_path_none(creator):
#     log_file = os.path.join(creator.output_dir, "safari-1.log")
#     expected_webdriver = mock()
#     executable_path = "/usr/bin/safaridriver"
#     when(webdriver).Safari(options=None, service=ANY).thenReturn(
#         expected_webdriver
#     )
#     driver = creator.creator.create_safari({}, None, service_log_path=log_file)
#     assert driver == expected_webdriver