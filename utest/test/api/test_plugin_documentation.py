import inspect
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
        if not JYTHON:
            factory = GenericDiffReporterFactory()
            factory.load(reporter_json)
            self.reporter = factory.get_first_working()

    def test_no_plugin(self):
        sl = SeleniumLibrary()
        intro = sl.get_keyword_documentation('__intro__')
        init = sl.get_keyword_documentation('__init__')
        sl_intro = inspect.getdoc(sl)
        sl_init = inspect.getdoc(sl.__init__)
        self.assertEqual(intro, sl_intro)
        self.assertEqual(init, sl_init)

    def test_plugin_doc(self):
        sl = SeleniumLibrary(plugins=self.plugin_2)
        intro = sl.get_keyword_documentation('__intro__')
        init = sl.get_keyword_documentation('__init__')
        sl_init = inspect.getdoc(sl.__init__)

        self.assertEqual(init, sl_init)

        count = intro.count('Plugin: plugin_with_event_firing_webdriver')
        self.assertEqual(count, 2)

        self.assertIn('This is example plugin documentation.', intro)
        self.assertIn('This is chapter in heading 2', intro)

    def test_parse_plugin_doc(self):
        sl = SeleniumLibrary(plugins=self.plugin_2)
        plugin_docs = sl._parse_plugin_doc()
        index = 0
        for doc in plugin_docs:
            self.assertIn('This is example plugin documentation.', doc.doc)
            self.assertIn('plugin_with_event_firing_webdriver', doc.name)
            index += 1
        self.assertEqual(index, 1)

    def test_parse_plugin_no_doc(self):
        sl = SeleniumLibrary(plugins='{};arg1=Text1;arg2=Text2'.format(self.plugin_3))
        plugin_docs = sl._parse_plugin_doc()
        index = 0
        for doc in plugin_docs:
            self.assertEqual(doc.doc, 'No plugin documentation found.')
            self.assertEqual(doc.name, 'my_lib_args')
            index += 1
        self.assertEqual(index, 1)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_many_plugins(self):
        sl = SeleniumLibrary(plugins='%s, %s' % (self.plugin_1, self.plugin_2))
        verify(sl.get_keyword_documentation('__intro__'), self.reporter)

    @unittest.skipIf(JYTHON, 'ApprovalTest does not work with Jython')
    def test_no_doc(self):
        sl = SeleniumLibrary(plugins='{};arg1=Text1;arg2=Text2'.format(self.plugin_3))
        verify(sl.get_keyword_documentation('__intro__'), self.reporter)
