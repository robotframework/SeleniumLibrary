from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.support.events import AbstractEventListener


class MyListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        logger.info("Before navigate to %s" % url)
        sl = BuiltIn().get_library_instance("SeleniumLibrary")
        if sl.driver:
            logger.info("Got driver also from SeleniumLibrary.")

    def after_navigate_to(self, url, driver):
        logger.info("After navigate to %s" % url)

    def before_click(self, element, driver):
        logger.info("Before click")

    def after_click(self, element, driver):
        logger.info("After click")

    def before_change_value_of(self, element, driver):
        logger.info("Before clear and send_keys")

    def after_change_value_of(self, element, driver):
        logger.info("After clear and send_keys")
