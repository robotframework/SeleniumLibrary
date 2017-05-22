from robot.api import logger
from selenium.webdriver.remote.webelement import WebElement

from Selenium2Library.context import ContextAware
from Selenium2Library.locators import ElementFinder


LOG_LEVELS = ['TRACE', 'DEBUG', 'INFO', 'WARN', 'ERROR']


class LibraryComponent(ContextAware):

    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)
        self.element_finder = ElementFinder()

    def info(self, msg, html=False):
        logger.info(msg, html)

    def debug(self, msg, html=False):
        logger.debug(msg, html)

    def log(self, msg, level='INFO', html=False):
        if level.upper() in LOG_LEVELS:
            logger.write(msg, level, html)

    def warn(self, msg, html=False):
        logger.warn(msg, html)

    # TODO: Move logic in elementfinder.ElementFinder but keep method as proxy
    # in LibraryComponent class
    def element_find(self, locator, first_only=True, required=True, tag=None):
        if isinstance(locator, WebElement):
            return locator
        elements = self.element_finder.find(self.browser, locator, tag)
        if required and not elements:
            raise ValueError("Element locator '{}' did not match any "
                             "elements.".format(locator))
        if first_only:
            if not elements:
                return None
            return elements[0]
        return elements

    # TODO: Move logic in elementfinder.ElementFinder but keep method as proxy
    # in LibraryComponent class
    def get_value(self, locator, tag=None):
        element = self.element_find(
            locator, required=False, tag=tag
        )
        return element.get_attribute('value') if element is not None else None

    # TODO: Move logic in elementfinder.ElementFinder but keep method as proxy
    # in LibraryComponent class
    def page_contains_element(self, locator, tag=None,
                              message=None, loglevel='INFO'):
        element_name = tag if tag else 'element'
        if not self.element_find(locator, required=False, tag=tag):
            if not message:
                message = (
                    "Page should have contained %s "
                    "'%s' but did not" % (element_name, locator)
                )
            self.ctx.log_source(loglevel)
            raise AssertionError(message)
        self.info(
            "Current page contains %s '%s'." % (element_name, locator)
        )

    # TODO: Move logic in elementfinder.ElementFinder but keep method as proxy
    # in LibraryComponent class
    def page_not_contains_element(self, locator, tag=None,
                                  message=None, loglevel='INFO'):
        element_name = tag if tag else 'element'
        if self.element_find(locator, required=False, tag=tag):
            if not message:
                message = (
                    "Page should not have contained %s '%s'"
                    % (element_name, locator)
                )
            self.ctx.log_source(loglevel)
            raise AssertionError(message)
        self.info(
            "Current page does not contain %s '%s'."
            % (element_name, locator)
        )
