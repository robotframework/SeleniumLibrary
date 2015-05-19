from Selenium2Library import Selenium2Library
from robot.utils import asserts
from robot.libraries.BuiltIn import BuiltIn

class CustomSeleniumKeywords(Selenium2Library):

    def __init__(self, *args, **kwargs):
        """Share `Selenium2Library`'s cache of browsers, so that
        we don't have to open a separate browser instance for the
        `Run On Failure Keyword Only Called Once` test."""
        ret = super(CustomSeleniumKeywords, self).__init__(*args, **kwargs)
        self._cache = BuiltIn().get_library_instance("Selenium2Library")._cache

    def custom_selenium_keyword(self):
        self.custom_selenium_keyword_inner()

    def custom_selenium_keyword_inner(self):
        asserts.assert_false(True)