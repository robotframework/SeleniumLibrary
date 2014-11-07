from Selenium2Library import Selenium2Library
from robot.utils import asserts
from robot.libraries.BuiltIn import BuiltIn

class CustomSeleniumKeywords(Selenium2Library):

    def custom_selenium_keyword(self):
        self.custom_selenium_keyword_inner()

    def custom_selenium_keyword_inner(self):
        asserts.assert_false(True)