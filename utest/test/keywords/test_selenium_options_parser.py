import unittest
import os

from robot.utils import JYTHON

try:
    from approvaltests.approvals import verify_all
    from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
except ImportError:
    if JYTHON:
        verify = None
        GenericDiffReporterFactory = None
    else:
        raise

from SeleniumLibrary.keywords.webdrivertools import SeleniumOptions
from SeleniumLibrary.utils import PY3


class ElementKeywordsPessKeys(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.options = SeleniumOptions()

    def setUp(self):
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(os.path.join(path, '..', 'approvals_reporters.json'))
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        self.reporter = factory.get_first_working()
        self.results = []

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_parse_options(self):
        self.results.append(self.options.parse('method:arg1'))
        self.results.append(self.options.parse('method:arg1:arg2'))
        self.results.append(self.options.parse('method:arg1,method:arg2'))
        self.results.append(self.options.parse('method'))
        self.results.append(self.options.parse('method1,method2'))
        self.results.append(self.options.parse('method,method'))
        self.results.append(self.options.parse('add_argument:--disable-dev-shm-usage'))
        self.results.append(self.options.parse('add_argument:--proxy-server=66.97.38.58\:80'))
        self.result_formatter()
        verify_all('Selenium options string to dict', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_options_escape(self):
        self.results.append(self.options._options_escape('--proxy-server=66.97.38.58\:80'.split(':')))
        self.results.append(self.options._options_escape('arg1:arg2'.split(':')))
        self.results.append(self.options._options_escape('arg1'.split(':')))
        self.result_formatter()
        verify_all('Selenium options escape string to dict', self.results, reporter=self.reporter)

    def result_formatter(self):
        if PY3:
            pass
        for index, result in enumerate(self.results):
            result = str(result)
            self.results[index] = result.replace("=u'", "='")
