import os

import pytest
from approvaltests import verify_all
from approvaltests.reporters import GenericDiffReporterFactory

from SeleniumLibrary.utils.types import type_converter


@pytest.fixture(scope="module")
def reporter():
    path = os.path.dirname(__file__)
    reporter_json = os.path.abspath(
        os.path.join(path, "..", "approvals_reporters.json")
    )
    factory = GenericDiffReporterFactory()
    factory.load(reporter_json)
    return factory.get_first_working()


def test_type_converter(reporter):
    results = [
        type_converter("str"),
        type_converter(1),
        type_converter({"key": 1}),
    ]
    verify_all("Type converter", results, reporter=reporter)
