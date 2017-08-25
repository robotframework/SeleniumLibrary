import unittest

from mockito import when, unstub, verify

from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.keywords import RunOnFailureKeywords


class SeleniumLibraryRunOnFailureTest(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_run_on_failure(self):
        when(RunOnFailureKeywords).run_on_failure().thenReturn(True)
        sl = SeleniumLibrary()
        sl.run_on_failure()
        verify(RunOnFailureKeywords, times=1).run_on_failure()

    def test_underscore_run_on_failure(self):
        when(RunOnFailureKeywords).run_on_failure().thenReturn(True)
        sl = SeleniumLibrary()
        sl._run_on_failure()
        verify(RunOnFailureKeywords, times=1).run_on_failure()
