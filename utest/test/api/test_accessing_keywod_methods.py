import unittest

from SeleniumLibrary import SeleniumLibrary


class KeywordsMethodsTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.selib = SeleniumLibrary()

    def test_kw_with_method_name(self):
        assert self.selib.keywords["add_cookie"]
        assert self.selib.attributes["add_cookie"]
        assert self.selib.keywords["page_should_contain_image"]
        assert self.selib.attributes["page_should_contain_image"]

    def test_kw_with_methods_name_do_not_have_kw_name(self):
        with self.assertRaises(KeyError):
            self.selib.keywords["Add Cookie"]
        with self.assertRaises(KeyError):
            self.selib.keywords["Page Should Contain Image"]

    def test_kw_with_decorated_name(self):
        assert self.selib.attributes["get_webelement"]
        assert self.selib.keywords["Get WebElement"]
        assert self.selib.attributes["get_webelements"]
        assert self.selib.keywords["Get WebElements"]
