from pathlib import Path
import sys

import pytest

from SeleniumLibrary import SeleniumLibrary


@pytest.fixture()
def sl() -> SeleniumLibrary:
    sys.path.append(str(Path(__file__).parent.parent.absolute()))
    return SeleniumLibrary(language="FI")


def test_translation(sl: SeleniumLibrary):
    spec = sl.keywords_spec["__init__"]
    assert spec.argument_specification
    doc: str = spec.documentation
    assert doc.startswith(
        "00 SeleniumLibrary is a web testing library for Robot Framework"
    )

    spec = sl.keywords_spec["hallinnoi_hälytys"]
    doc: str = spec.documentation
    assert doc == "Hallinnoi hälytyksen uusi dokkari\n\nToinen rivi"


def test_provide_translation_as_list(sl: SeleniumLibrary):
    lang_plugin = "robotframework_seleniumlibrary_translation_list"
    file_path = Path(__file__).parent.parent / lang_plugin / "translate2.json"
    received_path = sl._get_translation("swe")
    assert received_path == file_path, received_path.relative_to(file_path)
    assert sl._get_translation("wrong") is None
    received_path = sl._get_translation("Eng")
    file_path = Path(__file__).parent.parent / lang_plugin / "translate1.json"
    assert received_path == file_path, received_path.relative_to(file_path)
