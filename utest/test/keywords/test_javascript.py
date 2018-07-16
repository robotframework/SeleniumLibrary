import os
import unittest

from approvaltests.approvals import verify_all
from approvaltests.reporters.generic_diff_reporter_factory import \
    GenericDiffReporterFactory

from SeleniumLibrary.keywords import JavaScriptKeywords


class JavaScriptKeywordsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.javascript = JavaScriptKeywords(None)
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(
            os.path.join(path, '..', 'approvals_reporters.json'))
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        cls.reporter = factory.get_first_working()

    def test_get_javascript_with_args(self):
        code, args = self.javascript._parse_javascript_and_arguments(
            ['ARGUMENTS', 'argument1', 'argument2', 'JAVASCRIPT',
             'my.first.line.of.JS.code;', 'my.second.line.of.JS.code;'])
        combined = code.split("\n") + args
        verify_all("INPUT", combined)

    def test_get_javascript_with_args_first(self):
        code, args = self.javascript._parse_javascript_and_arguments(
            ['JAVASCRIPT', 'my.first.line.of.JS.code;',
             'my.second.line.of.JS.code', 'ARGUMENTS', 'argument1',
             'argument2'])
        combined = code.split("\n") + args
        verify_all("INPUT", combined)

    def test_get_javascript_no_markers(self):
        code, args = self.javascript._parse_javascript_and_arguments(
            ['my.first.line.of.JS.code;', 'my.second.line.of.JS.code;',
             'my.third.line.of.JS.code;'])
        combined = code.split("\n") + args
        verify_all("INPUT", combined)

    def test_get_javascript_no_code_marker(self):
        code, args = self.javascript._parse_javascript_and_arguments(
            ['my.first.line.of.JS.code;', 'my.second.line.of.JS.code;',
             'my.third.line.of.JS.code;', 'ARGUMENTS', 'argument1',
             'argument2', 'argument3'])
        combined = code.split("\n") + args
        verify_all("INPUT", combined)

