import unittest

from mockito import mock, unstub, when, verify
from mockito.matchers import ANY

from SeleniumLibrary.keywords import ScreenshotKeywords
from SeleniumLibrary.utils import events


class KeywordArgumentsElementTest(unittest.TestCase):

    def setUp(self):
        ctx = mock()
        ctx._browser = mock()
        self.screen = ScreenshotKeywords(ctx)
        self.ctx = ctx

    def tearDown(self):
        unstub()

    def test_set_screenshot_directory(self):
        when(events).on(ANY, ANY, ANY)
        self.screen.set_screenshot_directory('/foo')
        self.screen.set_screenshot_directory('/foo', None)
        self.screen.set_screenshot_directory('/foo', 'None')
        self.screen.set_screenshot_directory('/foo', 'False')
        verify(events, times=4).on(ANY, ANY, ANY)
        self.screen.set_screenshot_directory('/foo', True)
        self.screen.set_screenshot_directory('/foo', 'True')
        self.screen.set_screenshot_directory('/foo', 'Yes')
        verify(events, times=4).on(ANY, ANY, ANY)
