import os
import unittest

from approvaltests.approvals import verify
from approvaltests.reporters.generic_diff_reporter_factory import (
    GenericDiffReporterFactory,
)
from robot.utils import WINDOWS

from SeleniumLibrary import SeleniumLibrary


class PluginDocumentation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        root_dir = os.path.dirname(os.path.abspath(__file__))
        cls.plugin_1 = os.path.join(root_dir, "my_lib.py")
        cls.plugin_3 = os.path.join(root_dir, "my_lib_args.py")

    def setUp(self):
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(
            os.path.join(path, "..", "approvals_reporters.json")
        )
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        self.reporter = factory.get_first_working()

    @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
    def test_many_plugins(self):
        sl = SeleniumLibrary(
            plugins=f"{self.plugin_1}, {self.plugin_3};arg1=Text1;arg2=Text2"
        )
        verify(sl.get_keyword_documentation("__intro__"), self.reporter)

    @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
    def test_parse_plugin_init_doc(self):
        sl = SeleniumLibrary(plugins=f"{self.plugin_3};arg1=Text1;arg2=Text2")
        verify(sl.get_keyword_documentation("__init__"), self.reporter)

    @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
    def test_parse_plugin_kw_doc(self):
        sl = SeleniumLibrary(plugins=f"{self.plugin_3};arg1=Text1;arg2=Text2")
        verify(sl.get_keyword_documentation("execute_javascript"), self.reporter)
