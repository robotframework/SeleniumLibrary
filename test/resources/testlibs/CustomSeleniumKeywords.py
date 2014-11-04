from Selenium2Library import Selenium2Library
from robot.utils import asserts
from robot.libraries.BuiltIn import BuiltIn

class CustomSeleniumKeywords(Selenium2Library):

    def __init__(self, *args, **kwargs):
        ret = super(CustomSeleniumKeywords, self).__init__(*args, **kwargs)
        self._cache = BuiltIn().get_library_instance("Selenium2Library")._cache

    def custom_selenium_keyword(self):
        self.custom_selenium_keyword_inner()

    def custom_selenium_keyword_inner(self):
        asserts.assert_false(True)