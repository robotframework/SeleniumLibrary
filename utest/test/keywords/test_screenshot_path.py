import pytest
from mockito import mock, unstub
from SeleniumLibrary.keywords import ScreenshotKeywords


@pytest.fixture(scope='module')
def screenshot():
    ctx = mock()
    ctx.screenshot_root_directory = None
    return ScreenshotKeywords(ctx)


def teardown_module():
    unstub()


def test_undefined_screenshot_root_directory(screenshot):
    screenshot.ctx.screenshot_root_directory = None
    assert screenshot._get_screenshot_path('/tmp/screenshot.png') == "/tmp/screenshot.png"
    assert screenshot._get_screenshot_path('screenshot.png') == screenshot.log_dir + "/screenshot.png"

def test_embed_screenshot_root_directory(screenshot):
    screenshot.ctx.screenshot_root_directory = ScreenshotKeywords.EMBED_FLAG
    assert screenshot._get_screenshot_path('/tmp/screenshot.png') == "/tmp/screenshot.png"
    assert screenshot._get_screenshot_path('screenshot.png') == screenshot.log_dir + "/screenshot.png"

def test_custom_screenshot_root_directory(screenshot):
    custom_root_dir = "/tmp/custom_root_dir"
    screenshot.ctx.screenshot_root_directory = custom_root_dir
    assert screenshot._get_screenshot_path('/tmp/screenshot.png') == "/tmp/screenshot.png"
    assert screenshot._get_screenshot_path('screenshot.png') == custom_root_dir + "/screenshot.png"