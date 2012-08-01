import os
import robot
from robot.errors import DataError
from selenium import webdriver
from Selenium2Library import webdrivermonkeypatches
from Selenium2Library.utils import BrowserCache
from Selenium2Library.locators import WindowManager
from keywordgroup import KeywordGroup

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

class _BrowserManagementKeywords(KeywordGroup):

    def __init__(self):
        self._cache = BrowserCache()
        self._window_manager = WindowManager()
        self._speed_in_secs = float(0)
        self._timeout_in_secs = float(5)

    # Public, open and close

    def close_all_browsers(self):
        """Closes all open browsers and resets the browser cache.

        After this keyword new indexes returned from `Open Browser` keyword
        are reset to 1.

        This keyword should be used in test or suite teardown to make sure
        all browsers are closed.
        """
        self._debug('Closing all browsers')
        self._cache.close_all()

    def close_browser(self):
        """Closes the current browser."""
        if self._cache.current:
            self._debug('Closing browser with session id %s'
                        % self._cache.current.session_id)
            self._cache.close()

    def open_browser(self, url, browser='firefox', alias=None):
        """Opens a new browser instance to given URL.

        Returns the index of this browser instance which can be used later to
        switch back to it. Index starts from 1 and is reset back to it when
        `Close All Browsers` keyword is used. See `Switch Browser` for
        example.

        Optional alias is an alias for the browser instance and it can be used
        for switching between browsers (just as index can be used). See `Switch
        Browser` for more details.

        Possible values for `browser` are as follows:

        | firefox          | FireFox   |
        | ff               | FireFox   |
        | internetexplorer | Internet Explorer |
        | ie               | Internet Explorer |
        | googlechrome     | Google Chrome |
        | gc               | Google Chrome |
        | chrome           | Google Chrome |

        Note, that you will encounter strange behavior, if you open
        multiple Internet Explorer browser instances. That is also why
        `Switch Browser` only works with one IE browser at most.
        For more information see:
        http://selenium-grid.seleniumhq.org/faq.html#i_get_some_strange_errors_when_i_run_multiple_internet_explorer_instances_on_the_same_machine
        """
        self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        browser_name = browser
        browser = self._make_browser(browser_name)
        browser.get(url)
        self._debug('Opened browser with session id %s'
                    % browser.session_id)
        return self._cache.register(browser, alias)

    def switch_browser(self, index_or_alias):
        """Switches between active browsers using index or alias.

        Index is returned from `Open Browser` and alias can be given to it.

        Example:
        | Open Browser        | http://google.com | ff       |
        | Location Should Be  | http://google.com |          |
        | Open Browser        | http://yahoo.com  | ie       | 2nd conn |
        | Location Should Be  | http://yahoo.com  |          |
        | Switch Browser      | 1                 | # index  |
        | Page Should Contain | I'm feeling lucky |          |
        | Switch Browser      | 2nd conn          | # alias  |
        | Page Should Contain | More Yahoo!       |          |
        | Close All Browsers  |                   |          |

        Above example expects that there was no other open browsers when
        opening the first one because it used index '1' when switching to it
        later. If you aren't sure about that you can store the index into
        a variable as below.

        | ${id} =            | Open Browser  | http://google.com | *firefox |
        | # Do something ... |
        | Switch Browser     | ${id}         |                   |          |
        """
        try:
            self._cache.switch(index_or_alias)
            self._debug('Switched to browser with Selenium session id %s'
                         % self._cache.current.session_id)
        except (RuntimeError, DataError):  # RF 2.6 uses RE, earlier DE
            raise RuntimeError("No browser with index or alias '%s' found."
                               % index_or_alias)

    # Public, window management

    def close_window(self):
        """Closes currently opened pop-up window."""
        self._current_browser().close()

    def get_window_identifiers(self):
        """Returns handle identifiers for all windows known to the browser."""
        return self._window_manager.get_window_handles(self._current_browser())

    def maximize_browser_window(self):
        """Maximizes current browser window."""
        self._current_browser().execute_script(
            "if (window.screen) { window.moveTo(0, 0); window.resizeTo(window.screen.availWidth, window.screen.availHeight); }")

    def select_frame(self, locator):
        """Sets frame identified by `locator` as current frame.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        """
        self._info("Selecting frame '%s'." % locator)
        element = self._element_find(locator, True, True, tag='frame')
        self._current_browser().switch_to_frame(element)

    def select_window(self, locator=None):
        """Selects the window found with `locator` as the context of actions.

        If the window is found, all subsequent commands use that window, until
        this keyword is used again. If the window is not found, this keyword fails.
        
        By default, when a locator value is provided,
        it is matched against the title of the window and the
        handle/identifier of the window. If multiple windows with
        same identifier are found, the first one is selected.

        Special locator `main` (default) can be used to select the main window.

        It is also possible to specify the approach Selenium2Library should take
        to find a window by specifying a locator strategy:

        | *Strategy* | *Example*                               | *Description*                        |
        | title      | Select Window `|` title=My Document     | Matches by window title              |
        | name       | Select Window `|` name=${id}            | Matches by window handle/identifier, see `Get Window Identifiers` |
        | url        | Select Window `|` url=http://google.com | Matches by window's current URL      |

        Example:
        | Click Link | popup_link | # opens new window |
        | Select Window | popupName |
        | Title Should Be | Popup Title |
        | Select Window |  | | # Chooses the main window again |
        """
        self._window_manager.select(self._current_browser(), locator)

    def unselect_frame(self):
        """Sets the top frame as the current frame."""
        self._current_browser().switch_to_default_content()

    # Public, browser/current page properties

    def get_location(self):
        """Returns the current location."""
        return self._current_browser().get_current_url()

    def get_source(self):
        """Returns the entire html source of the current page or frame."""
        return self._current_browser().get_page_source()

    def get_title(self):
        """Returns title of current page."""
        return self._current_browser().get_title()

    def location_should_be(self, url):
        """Verifies that current URL is exactly `url`."""
        actual = self.get_location()
        if  actual != url:
            raise AssertionError("Location should have been '%s' but was '%s'"
                                 % (url, actual))
        self._info("Current location is '%s'." % url)

    def location_should_contain(self, expected):
        """Verifies that current URL contains `expected`."""
        actual = self.get_location()
        if not expected in actual:
            raise AssertionError("Location should have contained '%s' "
                                 "but it was '%s'." % (expected, actual))
        self._info("Current location contains '%s'." % expected)

    def log_location(self):
        """Logs and returns the current location."""
        url = self.get_location()
        self._info(url)
        return url

    def log_source(self, loglevel='INFO'):
        """Logs and returns the entire html source of the current page or frame.

        The `loglevel` argument defines the used log level. Valid log levels are
        `WARN`, `INFO` (default), `DEBUG`, `TRACE` and `NONE` (no logging).
        """
        source = self.get_source()
        self._log(source, loglevel.upper())
        return source

    def log_title(self):
        """Logs and returns the title of current page."""
        title = self.get_title()
        self._info(title)
        return title

    def title_should_be(self, title):
        """Verifies that current page title equals `title`."""
        actual = self.get_title()
        if actual != title:
            raise AssertionError("Title should have been '%s' but was '%s'"
                                  % (title, actual))
        self._info("Page title is '%s'." % title)

    # Public, navigation

    def go_back(self):
        """Simulates the user clicking the "back" button on their browser."""
        self._current_browser().back()

    def go_to(self, url):
        """Navigates the active browser instance to the provided URL."""
        self._info("Opening url '%s'" % url)
        self._current_browser().get(url)

    def reload_page(self):
        """Simulates user reloading page."""
        self._current_browser().refresh()

    # Public, execution properties

    def get_selenium_speed(self):
        """Gets the delay in seconds that is waited after each Selenium command.

        See `Set Selenium Speed` for an explanation."""
        return robot.utils.secs_to_timestr(self._speed_in_secs)

    def get_selenium_timeout(self):
        """Gets the timeout in seconds that is used by various keywords.

        See `Set Selenium Timeout` for an explanation."""
        return robot.utils.secs_to_timestr(self._timeout_in_secs)

    def set_selenium_speed(self, seconds):
        """Sets the delay in seconds that is waited after each Selenium command.

        This is useful mainly in slowing down the test execution to be able to
        view the execution. `seconds` may be given in Robot Framework time
        format. Returns the previous speed value.

        Example:
        | Set Selenium Speed | .5 seconds |
        """
        old_speed = self.get_selenium_speed()
        self._speed_in_secs = robot.utils.timestr_to_secs(seconds)
        for browser in self._cache.browsers:
            browser.set_speed(self._speed_in_secs)
        return old_speed

    def set_selenium_timeout(self, seconds):
        """Sets the timeout in seconds used by various keywords.

        There are several `Wait ...` keywords that take timeout as an
        argument. All of these timeout arguments are optional. The timeout
        used by all of them can be set globally using this keyword.
        See `introduction` for more information about timeouts.

        The previous timeout value is returned by this keyword and can
        be used to set the old value back later. The default timeout
        is 5 seconds, but it can be altered in `importing`.

        Example:
        | ${orig timeout} = | Set Selenium Timeout | 15 seconds |
        | Open page that loads slowly |
        | Set Selenium Timeout | ${orig timeout} |
        """
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

