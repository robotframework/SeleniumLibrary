import os
import unittest

from approvaltests.approvals import verify
from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory

from SeleniumLibrary.keywords import JavaScriptKeywords


class JavaScriptKeywordsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.javascript = JavaScriptKeywords(None)
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(os.path.join(path, '..', 'approvals_reporters.json'))
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        cls.reporter = factory.get_first_working()

    def test_get_javascript(self):
        code = self.javascript._get_javascript_to_execute('code here')
        verify(code, self.reporter)