import unittest

from mockito import when, unstub, verify

from Selenium2Library import Selenium2Library
from Selenium2Library.keywords import RunOnFailureKeywords


class Selenium2LibraryRunOnFailureTest(unittest.TestCase):

    def tearDown(self):
        unstub()

    def test_run_on_failure(self):
        when(RunOnFailureKeywords).run_on_failure().thenReturn(True)
        s2l = Selenium2Library()
        s2l.run_on_failure()
        verify(RunOnFailureKeywords, times=1).run_on_failure()

    def test_underscore_run_on_failure(self):
        when(RunOnFailureKeywords).run_on_failure().thenReturn(True)
        s2l = Selenium2Library()
        s2l._run_on_failure()
        verify(RunOnFailureKeywords, times=1).run_on_failure()
