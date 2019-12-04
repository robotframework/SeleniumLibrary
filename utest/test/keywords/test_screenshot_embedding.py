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
    embed_decision = screenshot.screenshot_should_be_embedded('EMBED')
    assert embed_decision == True
    embed_decision = screenshot.screenshot_should_be_embedded("screenshot.png")
    assert embed_decision == False
    embed_decision = screenshot.screenshot_should_be_embedded(ScreenshotKeywords.DEFAULT_FILENAME_CAPTURE_PAGE_SCREENSHOT)
    assert embed_decision == False
    embed_decision = screenshot.screenshot_should_be_embedded(ScreenshotKeywords.DEFAULT_FILENAME_CAPTURE_ELEMENT_SCREENSHOT)
    assert embed_decision == False

def test_embed_screenshot_root_directory(screenshot):
    screenshot.ctx.screenshot_root_directory = ScreenshotKeywords.EMBED_FLAG
    embed_decision = screenshot.screenshot_should_be_embedded('EMBED')
    assert embed_decision == True
    embed_decision = screenshot.screenshot_should_be_embedded("screenshot.png")
    assert embed_decision == False
    embed_decision = screenshot.screenshot_should_be_embedded(ScreenshotKeywords.DEFAULT_FILENAME_CAPTURE_PAGE_SCREENSHOT)
    assert embed_decision == True
    embed_decision = screenshot.screenshot_should_be_embedded(ScreenshotKeywords.DEFAULT_FILENAME_CAPTURE_ELEMENT_SCREENSHOT)
    assert embed_decision == True

def test_custom_screenshot_root_directory(screenshot):
    screenshot.ctx.screenshot_root_directory = "/tmp/custom_root_dir"
    embed_decision = screenshot.screenshot_should_be_embedded('EMBED')
    assert embed_decision == True
    embed_decision = screenshot.screenshot_should_be_embedded("screenshot.png")
    assert embed_decision == False
    embed_decision = screenshot.screenshot_should_be_embedded(ScreenshotKeywords.DEFAULT_FILENAME_CAPTURE_PAGE_SCREENSHOT)
    assert embed_decision == False
    embed_decision = screenshot.screenshot_should_be_embedded(ScreenshotKeywords.DEFAULT_FILENAME_CAPTURE_ELEMENT_SCREENSHOT)
    assert embed_decision == False