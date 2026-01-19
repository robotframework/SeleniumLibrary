from os.path import dirname, abspath, join

import pytest
from mockito import mock, unstub

from SeleniumLibrary import ScreenshotKeywords, SeleniumLibrary

SCREENSHOT_FILE_NAME = "selenium-screenshot-{index}.png"
ELEMENT_FILE_NAME = "selenium-element-screenshot-{index}.png"
EMBED = "EMBED"
BASE64 = "BASE64"

@pytest.fixture(scope="module")
def screen_shot():
    ctx = mock()
    ctx.screenshot_root_directory = None
    return ScreenshotKeywords(ctx)


def teardown_function():
    unstub()


def test_defaults(screen_shot):
    assert screen_shot._decide_embedded(SCREENSHOT_FILE_NAME) == (False, None)
    assert screen_shot._decide_embedded(ELEMENT_FILE_NAME) == (False, None)


def test_screen_shotdir_embeded(screen_shot):
    screen_shot.ctx.screenshot_root_directory = EMBED
    assert screen_shot._decide_embedded(SCREENSHOT_FILE_NAME) == (True, EMBED)
    assert screen_shot._decide_embedded(SCREENSHOT_FILE_NAME.upper()) == (True, EMBED)
    assert screen_shot._decide_embedded(ELEMENT_FILE_NAME) == (True, EMBED)
    assert screen_shot._decide_embedded(ELEMENT_FILE_NAME.upper()) == (True, EMBED)
    assert screen_shot._decide_embedded("other.psn") == (False, None)


def test_screen_shotdir_return_base64(screen_shot):
    screen_shot.ctx.screenshot_root_directory = BASE64
    assert screen_shot._decide_embedded(SCREENSHOT_FILE_NAME) == (True, BASE64)
    assert screen_shot._decide_embedded(SCREENSHOT_FILE_NAME.upper()) == (True, BASE64)
    assert screen_shot._decide_embedded(ELEMENT_FILE_NAME) == (True, BASE64)
    assert screen_shot._decide_embedded(ELEMENT_FILE_NAME.upper()) == (True, BASE64)
    assert screen_shot._decide_embedded("other.psn") == (False, None)


def test_file_name_embeded(screen_shot):
    assert screen_shot._decide_embedded("other.psn") == (False, None)
    screen_shot.ctx.screenshot_root_directory = EMBED
    assert screen_shot._decide_embedded(EMBED) == (True, EMBED)
    screen_shot.ctx.screenshot_root_directory = BASE64
    assert screen_shot._decide_embedded(BASE64) == (True, BASE64)


def test_screenshot_path_embedded(screen_shot):
    screen_shot.ctx.screenshot_root_directory = EMBED
    assert screen_shot._get_screenshot_path("override.png") == join(
        screen_shot.log_dir, "override.png"
    )


def test_sl_init_embed():
    sl = SeleniumLibrary(screenshot_root_directory="EmBed")
    assert sl.screenshot_root_directory == EMBED

    sl = SeleniumLibrary(screenshot_root_directory=EMBED)
    assert sl.screenshot_root_directory == EMBED

    sl = SeleniumLibrary(screenshot_root_directory="bAsE64")
    assert sl.screenshot_root_directory == BASE64

    sl = SeleniumLibrary(screenshot_root_directory=BASE64)
    assert sl.screenshot_root_directory == BASE64


def test_sl_init_not_embed():
    sl = SeleniumLibrary(screenshot_root_directory=None)
    assert sl.screenshot_root_directory is None

    sl = SeleniumLibrary(screenshot_root_directory="None")
    assert sl.screenshot_root_directory == "None"

    sl = SeleniumLibrary(screenshot_root_directory="/path/to/folder")
    assert sl.screenshot_root_directory == "/path/to/folder"


def test_sl_set_screenshot_directory():
    sl = SeleniumLibrary()
    sl.set_screenshot_directory("EmBed")
    assert sl.screenshot_root_directory == EMBED

    sl.set_screenshot_directory(EMBED)
    assert sl.screenshot_root_directory == EMBED

    sl.set_screenshot_directory(BASE64)
    assert sl.screenshot_root_directory == BASE64

    sl.set_screenshot_directory("EEmBedD")
    assert "EEmBedD" in sl.screenshot_root_directory
    assert len("EEmBedD") < len(sl.screenshot_root_directory)

    cur_dir = dirname(abspath(__file__))
    sl.set_screenshot_directory(cur_dir)
    assert sl.screenshot_root_directory == cur_dir
