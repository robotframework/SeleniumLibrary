import unittest

from mockito import when, unstub, verify

from SeleniumLibrary import SeleniumLibrary


class SeleniumLibraryRunOnFailureTest(unittest.TestCase):
    def tearDown(self):
        unstub()

    def test_failure_occurred(self):
        when(SeleniumLibrary).failure_occurred().thenReturn(True)
        sl = SeleniumLibrary()
        sl.failure_occurred()
        verify(SeleniumLibrary, times=1).failure_occurred()
