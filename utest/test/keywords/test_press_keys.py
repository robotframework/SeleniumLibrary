import unittest
import os

from approvaltests.approvals import verify_all
from approvaltests.reporters.generic_diff_reporter_factory import (
    GenericDiffReporterFactory,
)
from robot.utils import WINDOWS

from SeleniumLibrary.keywords import ElementKeywords


class ElementKeywordsPessKeys(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.element_keywords = ElementKeywords(None)

    def setUp(self):
        path = os.path.dirname(__file__)
        reporter_json = os.path.abspath(
            os.path.join(path, "..", "approvals_reporters.json")
        )
        factory = GenericDiffReporterFactory()
        factory.load(reporter_json)
        self.reporter = factory.get_first_working()

    @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
    def test_parse_keys(self):
        results = []
        results.append(self.element_keywords._parse_keys("A", "B", "C"))
        results.append(self.element_keywords._parse_keys("AAA", "CONTROL", "C"))
        results.append(self.element_keywords._parse_keys("AAA", "CONTROL+B", "C"))
        results.append(self.element_keywords._parse_keys("CONTROL+A", "ALT+B"))
        results.append(self.element_keywords._parse_keys("CONTROL+ALT+b"))
        results.append(self.element_keywords._parse_keys("Press CTRL+C to"))
        results.append(self.element_keywords._parse_keys("Press CTRL++C to"))
        results.append(self.element_keywords._parse_keys("END+E+N+D"))
        results.append(self.element_keywords._parse_keys("AALTO"))
        results.append(self.element_keywords._parse_keys("alt"))
        results.append(self.element_keywords._parse_keys("IS ALT HERE"))
        results.append(self.element_keywords._parse_keys("IS", "ALT", "HERE"))
        verify_all("index", results, reporter=self.reporter)

    @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
    def test_parse_keys_aliases(self):
        results = []
        results.append(self.element_keywords._parse_aliases("CTRL"))
        results.append(self.element_keywords._parse_aliases("ESC"))
        results.append(self.element_keywords._parse_aliases("CONTROL"))
        results.append(self.element_keywords._parse_aliases("BB"))
        results.append(self.element_keywords._parse_aliases("END"))
        verify_all("Alias testing", results, reporter=self.reporter)

    @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
    def test_separate_key(self):
        results = []
        results.append(self.element_keywords._separate_key("BB"))
        results.append(self.element_keywords._separate_key("ALT+B"))
        results.append(self.element_keywords._separate_key("A+B+C"))
        results.append(self.element_keywords._separate_key("A++"))
        results.append(self.element_keywords._separate_key("A+++"))
        results.append(self.element_keywords._separate_key("A+++C"))
        results.append(self.element_keywords._separate_key("+"))
        results.append(self.element_keywords._separate_key("++"))
        results.append(self.element_keywords._separate_key("+++"))
        verify_all("Separate key", results, reporter=self.reporter)

    @unittest.skipIf(WINDOWS, reason="ApprovalTest do not support different line feeds")
    def test_convert_key(self):
        results = []
        results.append(self.element_keywords._convert_special_keys(["B"]))
        results.append(self.element_keywords._convert_special_keys(["AA", "CCC"]))
        results.append(self.element_keywords._convert_special_keys(["ALT", "B"]))
        results.append(self.element_keywords._convert_special_keys(["ALT", "CTRL"]))
        verify_all("To Selenium Special Keys", results, reporter=self.reporter)
