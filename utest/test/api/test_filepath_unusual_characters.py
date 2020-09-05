import os

import pytest
from approvaltests.approvals import verify_all
from approvaltests.reporters.generic_diff_reporter_factory import (
    GenericDiffReporterFactory,
)
from robot.utils import WINDOWS

from SeleniumLibrary.utils.path_formatter import _format_path


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
def test_normal_file_path(reporter):
    results = []
    results.append(_format_path("/foo/file.log", 1))
    results.append(_format_path("/foo/file-{index}.log", 1))
    results.append(_format_path("/foo/file-{index}.log", "0001"))
    results.append(_format_path("/foo/file-{foo}.log", 1))
    results.append(_format_path("/{foo}/file-{index}.log", 1))
    results.append(_format_path("/foo/file-{index:03}.log", 1))
    results.append(_format_path("/foo/{index}-file-{index}.log", "1234"))
    results.append(_format_path("/foo/file-{in dex}.log", "1234"))
    results.append(_format_path("/foo/file-{in@dex}.log", "1234"))
    verify_all("Different file paths.", results, reporter=reporter)
