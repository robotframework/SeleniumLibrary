import hashlib
import inspect
import json
import sys
from pathlib import Path

from approvaltests import verify_all

from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.entry.get_versions import get_version
from SeleniumLibrary.entry.translation import (
    compare_translation,
    get_library_translation,
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
    data = get_library_translation()
    for item in data.values():
        assert item["name"], item["name"]
        assert item["doc"], item["doc"]
        assert item["sha256"], item["sha256"]


def test_translation_init_documents_import_arguments():
    data = get_library_translation()
    init_doc = data["__init__"]["doc"]
    assert init_doc == inspect.getdoc(SeleniumLibrary.__init__)
    assert init_doc != data["__intro__"]["doc"]
    assert (
        data["__init__"]["sha256"]
        == hashlib.sha256(init_doc.encode("utf-16")).hexdigest()
    )


def test_translation_intro_is_class_documentation():
    data = get_library_translation()
    intro_doc = data["__intro__"]["doc"]
    assert intro_doc == SeleniumLibrary.__doc__
    assert (
        data["__intro__"]["sha256"]
        == hashlib.sha256(intro_doc.encode("utf-16")).hexdigest()
    )


def test_compare_translation(tmp_path: Path):
    translation = tmp_path / "translation.json"
    data = get_library_translation()
    with translation.open("w") as file:
        json.dump(data, file, indent=4)
    table = compare_translation(translation, data)
    verify_all("No changes", table)


def test_compare_translation_changes(tmp_path: Path):
    translation = tmp_path / "translation.json"
    data = get_library_translation()
    data.pop("handle_alert", None)
    data["alert_should_be_present"]["sha256"] = "foo"
    with translation.open("w") as file:
        json.dump(data, file, indent=4)
    table = compare_translation(translation, get_library_translation())
    verify_all("Changes", table)
