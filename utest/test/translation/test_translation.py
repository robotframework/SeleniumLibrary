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
        "1 SeleniumLibrary is a web testing library for Robot Framework"
    )

    spec = sl.keywords_spec["hallinnoi_hälytys"]
    doc: str = spec.documentation
    assert doc == "Hallinnoi hälytyksen uusi dokkari\n\nToinen rivi"
