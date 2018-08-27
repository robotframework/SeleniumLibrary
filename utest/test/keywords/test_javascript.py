import os
import unittest

from SeleniumLibrary.utils.platform import JYTHON
try:
    from approvaltests.approvals import verify, verify_all
    from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
except ImportError:
    if JYTHON:
        verify = None
        GenericDiffReporterFactory = None
    else:
        raise

from SeleniumLibrary.keywords import JavaScriptKeywords


class JavaScriptKeywordsTest(unittest.TestCase):

    @classmethod
    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def setUpClass(cls):
        cls.js = JavaScriptKeywords(None)
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(os.path.join(path, '..', 'approvals_reporters.json'))
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        cls.reporter = factory.get_first_working()

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_get_javascript(self):
        code, args = self.js._get_javascript_to_execute(('code', 'here'))
        result = '%s + %s' % (code, args)
        verify(result, self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_get_javascript_no_code(self):
        code = ('ARGUMENTS', 'arg1', 'arg1')
        try:
            self.js._get_javascript_to_execute(code)
        except Exception as error:
            result = str(error)
        verify(str(result), self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_separate_code_and_args(self):
        all_results = []
        code_examples = [
            ('code1',), ('code1', 'code2'),
            ('JAVASCRIPT', 'code1', 'code2'),
            ('javascript', 'code1', 'code2'),
            ('JAVASCRIPT', 'code1', 'code2', 'ARGUMENTS'),
            ('JAVASCRIPT', 'code1', 'code2', 'argUMENTs'),
            ('ARGUMENTS', 'JAVASCRIPT', 'code1', 'code2'),
            ('JAVASCRIPT', 'code1', 'code2', 'ARGUMENTS', 'arg1', 'arg2'),
            ('ARGUMENTS', 'arg1', 'arg2', 'JAVASCRIPT', 'code1', 'code2'),
            ('aRGUMENTS', 'arg1', 'arg2', 'jAVASCRIPT', 'code1', 'code2'),]
        for code in code_examples:
            all_results.append(self.js_reporter(code))
        verify_all('code and args', all_results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_separate_code_and_args_errors(self):
        code_examples = [
            (),
            ('ARGUMENTS', 'arg1', 'ARGUMENTS', 'arg1', 'JAVASCRIPT',
             'code1', 'JAVASCRIPT', 'code2'),
            ('JAVASCRIPT', 'code1', 'JAVASCRIPT', 'code2'),
            ('JAVASCRIPT', 'code1', 'ARGUMENTS', 'arg1', 'ARGUMENTS', 'arg1'),
            ('code1', 'JAVASCRIPT', 'code1' 'ARGUMENTS', 'arg1',),
            ('ARGUMENTS', 'arg1', 'ARGUMENTS', 'arg1', 'JAVASCRIPT', 'code1'),
            ('aRGUMENtS', 'arg1', 'arg2', 'JAVASCRIPT', 'code1', 'code2'),
        ]
        all_results = []
        for code in code_examples:
            all_results.append(self.js_reporter(code))
        verify_all('error', all_results, reporter=self.reporter)

    def js_reporter(self, code):
        try:
            return self.js._separate_code_and_args(code)
        except Exception as error:
            return error
