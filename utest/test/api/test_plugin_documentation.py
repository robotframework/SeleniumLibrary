import os
import unittest

from robot.utils import JYTHON

from SeleniumLibrary import SeleniumLibrary

try:
    from approvaltests.approvals import verify
    from approvaltests.reporters.generic_diff_reporter_factory import GenericDiffReporterFactory
except ImportError:
    if JYTHON:
        verify = None
        GenericDiffReporterFactory = None
    else:
        raise


class PluginDocumentation(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cls.plugin_1 = os.path.join(root_dir, 'my_lib.py')
        cls.plugin_2 = os.path.join(root_dir, 'plugin_with_event_firing_webdriver.py')
        cls.plugin_3 = os.path.join(root_dir, 'my_lib_args.py')

    def setUp(self):
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(os.path.join(path, '..', 'approvals_reporters.json'))
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        self.reporter = factory.get_first_working()

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_parse_plugin_no_doc(self):
        sl = SeleniumLibrary(plugins='{};arg1=Text1;arg2=Text2'.format(self.plugin_3))
        verify(sl.get_keyword_documentation('__intro__'), self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_many_plugins(self):
        sl = SeleniumLibrary(plugins='%s, %s' % (self.plugin_1, self.plugin_2))
        verify(sl.get_keyword_documentation('__intro__'), self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_no_doc(self):
        sl = SeleniumLibrary(plugins='{};arg1=Text1;arg2=Text2'.format(self.plugin_3))
        verify(sl.get_keyword_documentation('__intro__'), self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_create_toc(self):
        sl = SeleniumLibrary()
        verify(sl.get_keyword_documentation('__intro__'), self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_parse_plugin_init_doc(self):
        sl = SeleniumLibrary(plugins='{};arg1=Text1;arg2=Text2'.format(self.plugin_3))
        verify(sl.get_keyword_documentation('__init__'), self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_parse_plugin_kw_doc(self):
        sl = SeleniumLibrary(plugins='{};arg1=Text1;arg2=Text2'.format(self.plugin_3))
        verify(sl.get_keyword_documentation('execute_javascript'), self.reporter)
