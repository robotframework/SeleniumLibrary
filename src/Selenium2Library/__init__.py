import os
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(os.path.join(_THIS_DIR, "lib", "selenium-2.4.0", "py"))

from robot.variables import GLOBAL_VARIABLES
from robot.errors import DataError
from robot import utils
from browsercache import BrowserCache
from elementfinder import ElementFinder
from windowmanager import WindowManager

from selenium import webdriver
    
FIREFOX_PROFILE_DIR = os.path.join(_THIS_DIR, 'firefoxprofile')
BROWSER_NAMES = {'ff': '*firefox',
                 'firefox': '*firefox',
                 'ie': '*iexplore',
                 'internetexplorer': '*iexplore',
                 'googlechrome': '*googlechrome',
                 'gc': '*googlechrome'
                }

class Selenium2Library(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.5

    def __init__(self):
        self._cache = BrowserCache()
        self._element_finder = ElementFinder()
        self._window_manager = WindowManager()

    def open_browser(self, url, browser='firefox', alias=None):
        self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        browser_name = browser
        browser = self._make_browser(browser_name)
        browser.get(url)
        self._debug('Opened browser with session id %s'
                    % browser.session_id)
        return self._cache.register(browser, alias)

    def close_browser(self):
        if self._cache.current:
            self._debug('Closing browser with session id %s'
                        % self._cache.current.session_id)
            self._cache.close()

    def close_all_browsers(self):
        self._debug('Closing all browsers')
        self._cache.close_all()

    def get_title(self):
        return self._current_browser().title

    def title_should_be(self, title):
        actual = self.get_title()
        if actual != title:
            raise AssertionError("Title should have been '%s' but was '%s'"
                                  % (title, actual))
        self._info("Page title is '%s'." % title)

    def get_url(self):
        return self._current_browser().get_current_url()

    def location_should_be(self, url):
        actual = self.get_url()
        if  actual != url:
            raise AssertionError("Location should have been '%s' but was '%s'"
                                 % (url, actual))
        self._info("Current location is '%s'." % url)

    def switch_browser(self, index_or_alias):
        try:
            self._cache.switch(index_or_alias)
            self._debug('Switched to browser with Selenium session id %s'
                         % self._cache.current.session_id)
        except (RuntimeError, DataError):  # RF 2.6 uses RE, earlier DE
            raise RuntimeError("No browser with index or alias '%s' found."
                               % index_or_alias)

    def go_to(self, url):
        self._info("Opening url '%s'" % url)
        self._current_browser().get(url)

    def click_link(self, locator):
        self._info("Clicking link '%s'." % locator)
        link = self._element_find(locator, True, True, tag='a')
        link.click()

    def select_window(self, locator=None):
        self._window_manager.select(self._current_browser(), locator)

    def close_window(self):
        self._current_browser().close()

    def get_window_identifiers(self):
        return self._window_manager.get_window_handles(self._current_browser())

    def _current_browser(self):
        if not self._cache.current:
            raise RuntimeError('No browser is open')
        return self._cache.current

    def _element_find(self, locator, first_only, required, tag=None):
        browser = self._current_browser()
        elements = self._element_finder.find(browser, locator, tag)
        if required and len(elements) == 0:
            raise ValueError("Element locator '" + locator + "' did not match any elements")
        if first_only:
            if len(elements) == 0: return None
            return elements[0]
        return elements

    def _make_browser(self, browser_name):
        browser_token = self._get_browser_token(browser_name)
        browser = None
        if browser_token == '*firefox':
            browser = webdriver.Firefox(webdriver.FirefoxProfile(FIREFOX_PROFILE_DIR))
        elif browser_token == '*googlechrome':
            browser = webdriver.Chrome()
        elif browser_token == '*iexplore':
            browser = webdriver.Ie()

        if browser is not None:
            # redefine properties as get methods so that they can be stubbed during tests
            browser.get_title = lambda: browser.title
            browser.get_current_url = lambda: browser.current_url
            browser.get_current_window_handle = lambda: browser.current_window_handle
            browser.get_window_handles = lambda: browser.window_handles
            return browser

        raise AssertionError(browser_name + " is not a supported browser")

    def _get_browser_token(self, browser_name):
        return BROWSER_NAMES.get(browser_name.lower().replace(' ', ''), browser_name)

    def _get_log_dir(self):
        logfile = GLOBAL_VARIABLES['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return GLOBAL_VARIABLES['${OUTPUTDIR}']

    def _log(self, message, level='INFO'):
        if level != 'NONE':
            print '*%s* %s' % (level, message)

    def _info(self, message):
        self._log(message)

    def _debug(self, message):
        self._log(message, 'DEBUG')

    def _warn(self, message):
        self._log(message,  "WARN")

    def _html(self, message):
        self._log(message, 'HTML')

    def _get_error_message(self, exception):
        # Cannot use unicode(exception) because it fails on Python 2.5 and
        # earlier if the message contains non-ASCII chars.
        # See for details: http://bugs.jython.org/issue1585
        return unicode(exception.args and exception.args[0] or '')

    def _error_contains(self, exception, message):
        return message in self._get_error_message(exception)

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s',''][len(items)==1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index+1, item))
        self._info('\n'.join(msg))
        return items
