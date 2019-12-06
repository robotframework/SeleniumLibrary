import pytest
from mockito import mock, unstub

from SeleniumLibrary import ScreenshotKeywords

SCREENSHOT_FILE_NAME = 'selenium-screenshot-{index}.png'
ELEMENT_FILE_NAME = 'selenium-element-screenshot-{index}.png'
EMBED = 'EMBED'


@pytest.fixture(scope='module')
def screen_shot():
    ctx = mock()
    ctx.screenshot_root_directory = None
    return ScreenshotKeywords(ctx)


def teardown_function():
    unstub()


def test_defaults(screen_shot):
    assert screen_shot._decide_embedded(SCREENSHOT_FILE_NAME) is False
    assert screen_shot._decide_embedded(ELEMENT_FILE_NAME) is False


def test_screen_shotdir_embeded(screen_shot):
    screen_shot.ctx.screenshot_root_directory = EMBED
    assert screen_shot._decide_embedded(SCREENSHOT_FILE_NAME) is True
    assert screen_shot._decide_embedded(ELEMENT_FILE_NAME) is True
    assert screen_shot._decide_embedded('other.psn') is False


def test_file_name_embeded(screen_shot):
    assert screen_shot._decide_embedded(EMBED) is True
    assert screen_shot._decide_embedded('other.psn') is False
    screen_shot.ctx.screenshot_root_directory = EMBED
    assert screen_shot._decide_embedded(EMBED) is True
