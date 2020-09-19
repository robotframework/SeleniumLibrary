import os

import pytest
from approvaltests.approvals import verify_all
from approvaltests.reporters.generic_diff_reporter_factory import (
    GenericDiffReporterFactory,
)
from robot.utils import WINDOWS

from SeleniumLibrary.utils import escape_xpath_value


@pytest.fixture(scope="module")
def reporter():
    path = os.path.dirname(__file__)
    reporter_json = os.path.abspath(
        os.path.join(path, "..", "approvals_reporters.json")
    )
    factory = GenericDiffReporterFactory()
    factory.load(reporter_json)
    return factory.get_first_working()


@pytest.mark.skipif(WINDOWS, reason="ApprovalTest do not support different line feeds")
def test_string(reporter):
    results = []
    results.append(escape_xpath_value("tidii"))
    results.append(escape_xpath_value('"tidii"'))
    results.append(escape_xpath_value("'tidii'"))
    results.append(escape_xpath_value("\"'tidii'"))
    results.append(escape_xpath_value("\"'tidii'\""))
    results.append(escape_xpath_value('"\'t"id"ii\'"'))
    results.append(escape_xpath_value("\"'tidii'\""))
    results.append(escape_xpath_value("\"'ti'd'ii'\""))
    verify_all("Escape xpath value", results, reporter=reporter)
