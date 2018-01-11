from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from SeleniumLibrary.base import keyword
from SeleniumLibrary.base import LibraryComponent
from SeleniumLibrary.keywords import BrowserManagementKeywords


class KeywordClass(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)

    @keyword
    def open_browser(self, host):
        logger.info('This is keyword from KeywordClass')
        url = 'http://{}.com/'.format(host)
        browser_management = BrowserManagementKeywords(self.ctx)
        browser_management.open_browser(url, 'chrome')

    @keyword
    def get_browser_desired_capabilities(self):
        logger.info('Getting currently open browser desired capabilities')
        return self.driver.desired_capabilities


class NewKeywords(object):

    ROBOT_LISTENER_API_VERSION = 2

    def __init__(self):
        self.ROBOT_LIBRARY_LISTENER = self

    def start_suite(self, name, attributes):
        sl = BuiltIn().get_library_instance('SeleniumLibrary')
        sl.add_library_components([KeywordClass(sl)])
        BuiltIn().reload_library('SeleniumLibrary')
        self.added = True
