import os
import sys
import unittest

import pytest
from approvaltests.approvals import verify_all
from approvaltests.reporters.generic_diff_reporter_factory import (
    GenericDiffReporterFactory,
)
from mockito import mock, when, unstub, ANY
from robot.utils import WINDOWS
from selenium import webdriver

from SeleniumLibrary.keywords.webdrivertools import SeleniumService, WebDriverCreator


@pytest.fixture(scope="module")
def service():
    return SeleniumService()

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
def test_parse_service_string(service, reporter):
    results = []
    results.append(service._parse('attribute="arg1"'))
    # results.append(service._parse("  attribute = True  "))    # need to resolve issues with spaces in service string.
    results.append(service._parse('attribute="arg1";attribute=True'))
    results.append(service._parse('attribute=["arg1","arg2","arg3"] ; attribute=True ; attribute="arg4"'))
    results.append(
        service._parse(
            'attribute="C:\\\\path\\to\\\\profile"'
        )
    )
    results.append(
        service._parse(
            r'attribute="arg1"; attribute="C:\\path\\to\\profile"'
        )
    )
    results.append(service._parse("attribute=None"))
    verify_all("Selenium service string to dict", results, reporter=reporter)


# @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
# @unittest.skipIf(sys.version_info > (3, 11), reason="Errors change with Python 3.12")
@pytest.mark.skipif(WINDOWS, reason="ApprovalTest do not support different line feeds")
@pytest.mark.skipif(sys.version_info > (3, 11), reason="Errors change with Python 3.12")
def test_parse_service_string_errors(service, reporter):
    results = []
    results.append(error_formatter(service._parse, "attribute=arg1", True))
    results.append(error_formatter(service._parse, "attribute='arg1", True))
    results.append(error_formatter(service._parse, "attribute=['arg1'", True))
    results.append(error_formatter(service._parse, "attribute=['arg1';'arg2']", True))
    results.append(error_formatter(service._parse, "attribute['arg1']", True))
    results.append(error_formatter(service._parse, "attribute=['arg1'] attribute=['arg2']", True))
    verify_all("Selenium service string errors", results, reporter=reporter)


@pytest.mark.skipif(WINDOWS, reason="ApprovalTest do not support different line feeds")
@pytest.mark.skipif(sys.version_info < (3, 12), reason="Errors change with Python 3.12")
def test_parse_service_string_errors_py3_12(service, reporter):
    results = []
    results.append(error_formatter(service._parse, "attribute=arg1", True))
    results.append(error_formatter(service._parse, "attribute='arg1", True))
    results.append(error_formatter(service._parse, "attribute=['arg1'", True))
    results.append(error_formatter(service._parse, "attribute=['arg1';'arg2']", True))
    results.append(error_formatter(service._parse, "attribute['arg1']", True))
    results.append(error_formatter(service._parse, "attribute=['arg1'] attribute=['arg2']", True))
    verify_all("Selenium service string errors", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_split_service(service, reporter):
    results = []
    results.append(service._split("attribute='arg1'", ';'))
    results.append(service._split("attribute='arg1';attribute='arg2'", ';'))
    results.append(service._split("attribute=['arg1','arg2'];attribute='arg3'", ';'))
    results.append(service._split(" attribute = 'arg1' ; attribute = 'arg2' ", ';'))
    verify_all("Selenium service string splitting", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_split_attribute(service, reporter):
    results = []
    results.append(service._split("attribute='arg1'", '='))
    results.append(service._split("attribute=['arg1','arg2']", '='))
    results.append(service._split(" attribute = [ 'arg1' , 'arg2' ]", '='))
    verify_all("Selenium service attribute string splitting", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_service_create(service, reporter):
    results = []
    service_str = "service_args=['--log-level=DEBUG']"
    brwsr_service = service.create("chrome", service_str)
    results.append(brwsr_service.service_args)

    service_str = f"{service_str};service_args=['--append-log', '--readable-timestamp']"
    brwsr_service = service.create("chrome", service_str)
    results.append(brwsr_service.service_args)

    service_str = f"{service_str};service_args=['--disable-build-check']"
    brwsr_service = service.create("chrome", service_str)
    results.append(brwsr_service.service_args)

    verify_all("Selenium service", results, reporter=reporter)


@unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_importer(service, reporter):
    results = []
    results.append(service._import_service("firefox"))
    results.append(service._import_service("headless_firefox"))
    results.append(service._import_service("chrome"))
    results.append(service._import_service("headless_chrome"))
    results.append(service._import_service("ie"))
    results.append(service._import_service("edge"))
    results.append(service._import_service("safari"))
    verify_all("Selenium service import", results, reporter=reporter)


def error_formatter(method, arg, full=False):
    try:
        return method(arg)
    except Exception as error:
        if full:
            return f"{arg} {error}"
        return "{} {}".format(arg, error.__str__()[:15])