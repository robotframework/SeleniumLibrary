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

    def not_keywords_but_public_methods(self):
        logger.info('Python public method not a keyword, because it is not '
                    'decorated with @keyword decorator')

    def _private_method_are_not_keywords(self):
        logger.info('Python private method is not a keyword, because it is not '
                    'decorated with @keyword decorator')
