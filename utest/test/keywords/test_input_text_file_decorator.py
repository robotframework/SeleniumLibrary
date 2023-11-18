import unittest

from mockito import unstub, when
from SeleniumLibrary.keywords.webdrivertools.sl_file_detector import (
    SelLibLocalFileDetector,
)


class InputTextFileDecorator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.file = SelLibLocalFileDetector()

    def tearDown(self):
        unstub()

    def test_file_decorator_not_file(self):
        when(self.file).choose_file().thenReturn(False)
        assert self.file.is_local_file("some string") is None

    def test_file_decodator_is_file_choose_file(self):
        when(self.file).choose_file().thenReturn(True)
        assert self.file.is_local_file("some_file") is None
