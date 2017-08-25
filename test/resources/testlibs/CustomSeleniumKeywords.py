from robot.libraries.BuiltIn import BuiltIn

from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword


class CustomSeleniumKeywords(SeleniumLibrary):

    def __init__(self, *args, **kwargs):
        """Share `SeleniumLibrary`'s cache of browsers, so that
        we don't have to open a separate browser instance for the
        `Run On Failure Keyword Only Called Once` test."""
        super(CustomSeleniumKeywords, self).__init__(*args, **kwargs)
        sl = BuiltIn().get_library_instance("SeleniumLibrary")
        self._browsers = sl._browsers

    @keyword
    def custom_selenium_keyword(self):
        self.custom_selenium_keyword_inner()

    @keyword
    def custom_selenium_keyword_inner(self):
        raise AssertionError
