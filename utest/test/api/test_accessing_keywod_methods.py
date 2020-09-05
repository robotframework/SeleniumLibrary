import unittest

from SeleniumLibrary import SeleniumLibrary


class KeywordsMethodsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selib = SeleniumLibrary()

    def test_kw_with_method_name(self):
        self.assertTrue(self.selib.keywords["add_cookie"])
        self.assertTrue(self.selib.attributes["add_cookie"])
        self.assertTrue(self.selib.keywords["page_should_contain_image"])
        self.assertTrue(self.selib.attributes["page_should_contain_image"])

    def test_kw_with_methods_name_do_not_have_kw_name(self):
        with self.assertRaises(KeyError):
            self.selib.keywords["Add Cookie"]
        with self.assertRaises(KeyError):
            self.selib.keywords["Page Should Contain Image"]

    def test_kw_with_decorated_name(self):
        self.assertTrue(self.selib.attributes["get_webelement"])
        self.assertTrue(self.selib.keywords["Get WebElement"])
        self.assertTrue(self.selib.attributes["get_webelements"])
        self.assertTrue(self.selib.keywords["Get WebElements"])
