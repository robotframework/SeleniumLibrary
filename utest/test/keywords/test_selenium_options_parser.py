import unittest
import os

from robot.libraries.BuiltIn import BuiltIn
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


class SeleniumOptionsParserTests(unittest.TestCase):

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
    def test_parse_options_string(self):
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
    def test_parse_options_other_types(self):
        self.results.append(self.options.parse('None'))
        self.results.append(self.options.parse(None))
        self.results.append(self.options.parse(False))
        self.results.append(self.options.parse('False'))
        options = [{'add_argument': ['--disable-dev-shm-usage']}]
        self.results.append(self.options.parse(options))
        self.results.append(self.options.parse([]))
        self.result_formatter()
        verify_all('Selenium options other types to dict', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_options_escape(self):
        self.results.append(self.options._options_escape('--proxy-server=66.97.38.58\:80'.split(':')))
        self.results.append(self.options._options_escape('arg1:arg2'.split(':')))
        self.results.append(self.options._options_escape('arg1'.split(':')))
        self.result_formatter()
        verify_all('Selenium options escape string to dict', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_options_create(self):
        options = [{'add_argument': ['--disable-dev-shm-usage']}]
        sel_options = self.options.create('chrome', options)
        self.results.append(sel_options.arguments)

        options.append({'add_argument': ['--headless']})
        sel_options = self.options.create('chrome', options)
        self.results.append(sel_options.arguments)

        options.append({'add_argument': ['--proxy-server=66.97.38.58:80']})
        sel_options = self.options.create('chrome', options)
        self.results.append(sel_options.arguments)

        self.result_formatter()
        verify_all('Selenium options', self.results, reporter=self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_importer(self):
        self.results.append(self.options._import_options('firefox'))
        self.results.append(self.options._import_options('headless_firefox'))
        self.results.append(self.options._import_options('chrome'))
        self.results.append(self.options._import_options('headless_chrome'))
        self.results.append(self.options._import_options('ie'))
        self.results.append(self.options._import_options('opera'))
        self.results.append(self.options._import_options('edge'))
        self.results.append(self.error_formatter(self.options._import_options, 'phantomjs'))
        self.results.append(self.error_formatter(self.options._import_options, 'safari'))
        self.results.append(self.error_formatter(self.options._import_options, 'htmlunit'))
        self.results.append(self.error_formatter(self.options._import_options, 'htmlunit_with_js'))
        self.results.append(self.error_formatter(self.options._import_options, 'android'))
        self.results.append(self.error_formatter(self.options._import_options, 'iphone'))
        verify_all('Selenium options import', self.results, reporter=self.reporter)

    def result_formatter(self):
        if PY3:
            pass
        for index, result in enumerate(self.results):
            result = str(result)
            self.results[index] = result.replace("=u'", "='")

    def error_formatter(self, method, arg):
        try:
            method(arg)
        except Exception as error:
            return '%s %s' % (arg, error.__str__()[:15])
