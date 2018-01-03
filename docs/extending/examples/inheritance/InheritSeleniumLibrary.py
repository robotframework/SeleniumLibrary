from robot.api import logger
from SeleniumLibrary import SeleniumLibrary
from SeleniumLibrary.base import keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords


class InheritSeleniumLibrary(SeleniumLibrary):

    @keyword
    def open_browser(self, host):
        url = 'http://{}.com/'.format(host)
        browser_management = BrowserManagementKeywords(self)
        browser_management.open_browser(url, 'chrome')

    @keyword
    def get_browser_desired_capabilities(self):
        logger.info('Getting currently open browser desired capabilities')
        return self.driver.desired_capabilities
