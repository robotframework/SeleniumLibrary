import json
from pathlib import Path
import sys

from approvaltests import verify_all

from SeleniumLibrary.entry.get_versions import get_version
from SeleniumLibrary.entry.translation import (
    compare_translatoin,
    get_library_translaton,
)


def test_version():
    lines = get_version().splitlines()
    python_version = (
        f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    )
    assert len(lines) == 6
    assert "Used Python is: " in lines[1], lines[1]
    assert python_version in lines[2], lines[2]
    assert 'Robot Framework version: "' in lines[3], lines[3]
    assert "Installed SeleniumLibrary version is: " in lines[4], lines[4]
    assert "Installed selenium version is: " in lines[5], lines[5]


def test_get_translation():
    data = get_library_translaton()
    for item in data.values():
        assert item["name"], item["name"]
        assert item["doc"], item["doc"]
        assert item["sha256"], item["sha256"]


def test_compare_translation(tmp_path: Path):
    translation = tmp_path / "translation.json"
    data = get_library_translaton()
    with translation.open("w") as file:
        json.dump(data, file, indent=4)
    table = compare_translatoin(translation, data)
    verify_all("No changes", table)


def test_compare_translation_changes(tmp_path: Path):
    translation = tmp_path / "translation.json"
    data = get_library_translaton()
    data.pop("handle_alert", None)
    data["alert_should_be_present"]["sha256"] = "foo"
    with translation.open("w") as file:
        json.dump(data, file, indent=4)
    table = compare_translatoin(translation, get_library_translaton())
    verify_all("Changes", table)
