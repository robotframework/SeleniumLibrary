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
        result_attr = self._get_preferences_attribute(result)
        if "key1" in result_attr:
            to_str = f"{to_str} key1 {result_attr['key1']}"
        if "key2" in result_attr:
            to_str = f"{to_str} key2 {result_attr['key2']}"
        self.results.append(to_str)

    def _get_preferences_attribute(self, result):
        # -- temporary fix to transition selenium to v4.17.2 from v4.16.0 and prior
        # from inspect import signature
        # sig = signature(result)
        if hasattr(result,'default_preferences'):
            return result.default_preferences
        elif hasattr(result,'_desired_preferences'):
            return result._desired_preferences
        else:
            return None
        # --
