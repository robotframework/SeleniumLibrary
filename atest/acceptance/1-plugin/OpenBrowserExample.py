from robot.api import logger
from selenium import webdriver

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.keywords import BrowserManagementKeywords
from SeleniumLibrary.keywords.webdrivertools import WebDriverCreator


class OpenBrowserExample(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self._new_creator = NewWebDriverCreator(self.log_dir)

    @keyword
    def open_browser(
        self,
        url,
        browser="firefox",
        alias=None,
        remote_url=False,
        desired_capabilities=None,
        ff_profile_dir=None,
        options=None,
        service_log_path=None,
        extra_dictionary=None,
        executable_path=None,
    ):
        self._new_creator.extra_dictionary = extra_dictionary
        browser_manager = BrowserManagementKeywords(self.ctx)
        browser_manager._make_driver = self._make_driver
        browser_manager.open_browser(
            url,
            browser=browser,
            alias=alias,
            remote_url=remote_url,
            desired_capabilities=desired_capabilities,
            ff_profile_dir=ff_profile_dir,
            options=options,
            service_log_path=service_log_path,
            executable_path=None,
        )

    def _make_driver(
        self,
        browser,
        desired_capabilities=None,
        profile_dir=None,
        remote=None,
        options=None,
        service_log_path=None,
        executable_path=None,
    ):
        driver = self._new_creator.create_driver(
            browser=browser,
            desired_capabilities=desired_capabilities,
            remote_url=remote,
            profile_dir=profile_dir,
            options=options,
            service_log_path=service_log_path,
            executable_path=executable_path,
        )
        driver.set_script_timeout(self.ctx.timeout)
        driver.implicitly_wait(self.ctx.implicit_wait)
        if self.ctx.speed:
            self._monkey_patch_speed(driver)
        return driver


class NewWebDriverCreator(WebDriverCreator):
    def create_driver(
        self,
        browser,
        desired_capabilities,
        remote_url,
        profile_dir=None,
        options=None,
        service_log_path=None,
        executable_path=None,
    ):
        self.browser_names["seleniumwire"] = "seleniumwire"
        browser = self._normalise_browser_name(browser)
        creation_method = self._get_creator_method(browser)
        desired_capabilities = self._parse_capabilities(desired_capabilities, browser)
        service_log_path = self._get_log_path(service_log_path)
        options = self.selenium_options.create(self.browser_names.get(browser), options)
        if service_log_path:
            logger.info("Browser driver log file created to: %s" % service_log_path)
            self._create_directory(service_log_path)
        if (
            creation_method == self.create_firefox
            or creation_method == self.create_headless_firefox
        ):
            return creation_method(
                desired_capabilities,
                remote_url,
                profile_dir,
                options=options,
                service_log_path=service_log_path,
            )
        if creation_method == self.create_seleniumwire:
            return creation_method(
                desired_capabilities,
                remote_url,
                options=options,
                service_log_path=service_log_path,
            )
        return creation_method(
            desired_capabilities,
            remote_url,
            options=options,
            service_log_path=service_log_path,
        )

    def create_seleniumwire(
        self, desired_capabilities, remote_url, options=None, service_log_path=None
    ):
        logger.info(self.extra_dictionary)
        return webdriver.Chrome()
