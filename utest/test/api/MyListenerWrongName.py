from robot.api import logger
from selenium.webdriver.support.events import AbstractEventListener


class MyListener(AbstractEventListener):
    def before_navigate_to(self, url, driver):
        logger.info(f"Before navigate to {url}")

    def after_navigate_to(self, url, driver):
        logger.info(f"After navigate to {url}")

    def before_click(self, element, driver):
        logger.info("Before click")

    def after_click(self, element, driver):
        logger.info("After click")

    def before_change_value_of(self, element, driver):
        logger.info("Before send_keys")

    def after_change_value_of(self, element, driver):
        logger.info("After send_keys")
