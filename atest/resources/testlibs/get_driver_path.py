"""
>>> from selenium.webdriver.common import driver_finder
>>> drfind = driver_finder.DriverFinder()
>>> from selenium.webdriver.chrome.service import Service
>>> from selenium.webdriver.chrome.options import Options
>>> drfind.get_path(Service(),Options())


    def _import_service(self, browser):
        browser = browser.replace("headless_", "", 1)
        # Throw error is used with remote .. "They cannot be used with a Remote WebDriver session." [ref doc]
        service = importlib.import_module(f"selenium.webdriver.{browser}.service")
        return service.Service

    def _import_options(self, browser):
        browser = browser.replace("headless_", "", 1)
        options = importlib.import_module(f"selenium.webdriver.{browser}.options")
        return options.Options

"""
from selenium import webdriver
from selenium.webdriver.common import driver_finder
import importlib
import inspect


def get_driver_path(browser):
    browser = browser.lower().replace("headless_", "", 1)
    service = importlib.import_module(f"selenium.webdriver.{browser}.service")
    options = importlib.import_module(f"selenium.webdriver.{browser}.options")

    args = inspect.signature(driver_finder.DriverFinder.__init__).parameters.keys()
    if ('service' in args) and ('options' in args):
        # Selenium V4.20.0 or greater
        finder = driver_finder.DriverFinder(service.Service(), options.Options())
        return finder.get_driver_path()
    else:
        # Selenium v4.19.0 and prior
        finder = driver_finder.DriverFinder()
        func = getattr(finder, 'get_path')
        return finder.get_path(service.Service(), options.Options())
