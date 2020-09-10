import os
import unittest

from approvaltests.approvals import verify_all
from approvaltests.reporters.generic_diff_reporter_factory import (
    GenericDiffReporterFactory,
)
from robot.utils import WINDOWS
from selenium import webdriver

from SeleniumLibrary.keywords import WebDriverCreator


class FireFoxProfileParsingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.log_dir = "/log/dir"
        cls.creator = WebDriverCreator(cls.log_dir)
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(
            os.path.join(path, "..", "approvals_reporters.json")
        )
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        cls.reporter = factory.get_first_working()

    def setUp(self):
        self.results = []

    @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
    def test_single_method(self):
        self._parse_result(
            self.creator._get_ff_profile('set_preference("key1", "arg1")')
        )
        self._parse_result(
            self.creator._get_ff_profile(
                'set_preference("key1", "arg1");set_preference("key1", "arg1")'
            )
        )
        self._parse_result(
            self.creator._get_ff_profile(
                'set_preference("key1", "arg1") ; set_preference("key2", "arg2")'
            )
        )
        profile = self.creator._get_ff_profile("update_preferences()")
        self.results.append(isinstance(profile, webdriver.FirefoxProfile))
        try:
            self.creator._get_ff_profile('wrong_name("key1", "arg1")')
        except AttributeError as error:
            self.results.append(error)
        try:
            self.creator._get_ff_profile('set_proxy("foo")')
        except Exception as error:
            self.results.append(str(error))
        verify_all("Firefox profile parsing", self.results, reporter=self.reporter)

    def _parse_result(self, result):
        to_str = ""
        if "key1" in result.default_preferences:
            to_str = f"{to_str} key1 {result.default_preferences['key1']}"
        if "key2" in result.default_preferences:
            to_str = f"{to_str} key2 {result.default_preferences['key2']}"
        self.results.append(to_str)
