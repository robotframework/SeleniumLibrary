from robot.libraries.BuiltIn import BuiltIn

from Selenium2Library import Selenium2Library
from Selenium2Library.base import keyword


class CustomSeleniumKeywords(Selenium2Library):

    def __init__(self, *args, **kwargs):
        """Share `Selenium2Library`'s cache of browsers, so that
        we don't have to open a separate browser instance for the
        `Run On Failure Keyword Only Called Once` test."""
        super(CustomSeleniumKeywords, self).__init__(*args, **kwargs)
        s2l = BuiltIn().get_library_instance("Selenium2Library")
        self._browsers = s2l._browsers

    @keyword
    def custom_selenium_keyword(self):
        self.custom_selenium_keyword_inner()

    @keyword
    def custom_selenium_keyword_inner(self):
        raise AssertionError
