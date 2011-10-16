import os
import robot
from robot.errors import DataError
from selenium import webdriver
from Selenium2Library import webdrivermonkeypatches
from Selenium2Library.utils import BrowserCache
from Selenium2Library.locators import WindowManager

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIREFOX_PROFILE_DIR = os.path.join(ROOT_DIR, 'resources', 'firefoxprofile')
BROWSER_NAMES = {'ff': '*firefox',
                 'firefox': '*firefox',
                 'ie': '*iexplore',
                 'internetexplorer': '*iexplore',
                 'googlechrome': '*googlechrome',
                 'gc': '*googlechrome',
                 'chrome': '*googlechrome'
                }

class _BrowserManagementKeywords(object):

    def __init__(self):
        self._cache = BrowserCache()
        self._window_manager = WindowManager()
        self._speed_in_secs = float(0)
        self._timeout_in_secs = float(5)

    # Public, open and close

    def close_all_browsers(self):
        self._debug('Closing all browsers')
        self._cache.close_all()

    def close_browser(self):
        if self._cache.current:
            self._debug('Closing browser with session id %s'
                        % self._cache.current.session_id)
            self._cache.close()

    def open_browser(self, url, browser='firefox', alias=None):
        self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        browser_name = browser
        browser = self._make_browser(browser_name)
        browser.get(url)
        self._debug('Opened browser with session id %s'
                    % browser.session_id)
        return self._cache.register(browser, alias)

    def switch_browser(self, index_or_alias):
        try:
            self._cache.switch(index_or_alias)
            self._debug('Switched to browser with Selenium session id %s'
                         % self._cache.current.session_id)
        except (RuntimeError, DataError):  # RF 2.6 uses RE, earlier DE
            raise RuntimeError("No browser with index or alias '%s' found."
                               % index_or_alias)

    # Public, window management

    def close_window(self):
        self._current_browser().close()

    def get_window_identifiers(self):
        return self._window_manager.get_window_handles(self._current_browser())

    def select_frame(self, locator):
        self._info("Selecting frame '%s'." % locator)
        element = self._element_find(locator, True, True, tag='frame')
        self._current_browser().switch_to_frame(element)

    def select_window(self, locator=None):
        self._window_manager.select(self._current_browser(), locator)

    def unselect_frame(self):
        self._current_browser().switch_to_default_content()

    # Public, browser/current page properties

    def get_source(self):
        return self._current_browser().get_page_source()

    def get_title(self):
        return self._current_browser().get_title()

    def get_url(self):
        return self._current_browser().get_current_url()

    def location_should_be(self, url):
        actual = self.get_url()
        if  actual != url:
            raise AssertionError("Location should have been '%s' but was '%s'"
                                 % (url, actual))
        self._info("Current location is '%s'." % url)

    def location_should_contain(self, expected):
        actual = self.get_url()
        if not expected in actual:
            raise AssertionError("Location should have contained '%s' "
                                 "but it was '%s'." % (expected, actual))
        self._info("Current location contains '%s'." % expected)

    def log_source(self, loglevel='INFO'):
        source = self.get_source()
        self._log(source, loglevel.upper())
        return source

    def log_title(self):
        self._info(self.get_title())

    def log_url(self):
        self._info(self.get_url())

    def title_should_be(self, title):
        actual = self.get_title()
        if actual != title:
            raise AssertionError("Title should have been '%s' but was '%s'"
                                  % (title, actual))
        self._info("Page title is '%s'." % title)

    # Public, navigation

    def go_back(self):
        self._current_browser().back()

    def go_to(self, url):
        self._info("Opening url '%s'" % url)
        self._current_browser().get(url)

    def reload_page(self):
        self._current_browser().refresh()

    # Public, execution properties

    def get_selenium_speed(self):
        return robot.utils.secs_to_timestr(self._speed_in_secs)

    def get_selenium_timeout(self):
        return robot.utils.secs_to_timestr(self._timeout_in_secs)

    def set_selenium_speed(self, seconds):
        old_speed = self.get_selenium_speed()
        self._speed_in_secs = robot.utils.timestr_to_secs(seconds)
        for browser in self._cache.browsers:
            browser.set_speed(self._speed_in_secs)
        return old_speed

    def set_selenium_timeout(self, seconds):
        old_timeout = self.get_selenium_timeout()
        self._timeout_in_secs = robot.utils.timestr_to_secs(seconds)
        return old_timeout

    # Private

    def _current_browser(self):
        if not self._cache.current:
            raise RuntimeError('No browser is open')
        return self._cache.current

    def _get_browser_token(self, browser_name):
        return BROWSER_NAMES.get(browser_name.lower().replace(' ', ''), browser_name)

    def _make_browser(self, browser_name):
        browser_token = self._get_browser_token(browser_name)
        browser = None
        if browser_token == '*firefox':
            browser = webdriver.Firefox(webdriver.FirefoxProfile(FIREFOX_PROFILE_DIR))
        elif browser_token == '*googlechrome':
            browser = webdriver.Chrome()
        elif browser_token == '*iexplore':
            browser = webdriver.Ie()

        if browser is None:
            raise ValueError(browser_name + " is not a supported browser.")

        browser.set_speed(self._speed_in_secs)
        browser.set_script_timeout(self._timeout_in_secs)

        return browser

