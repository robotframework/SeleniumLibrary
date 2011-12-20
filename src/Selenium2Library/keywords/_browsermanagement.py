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
BROWSER_NAMES = {'ff': "_make_ff",
                 'firefox': "_make_ff",
                 'ie': "_make_ie",
                 'internetexplorer': "_make_ie",
                 'googlechrome': "_make_chrome",
                 'gc': "_make_chrome",
                 'chrome': "_make_chrome",
                 'opera' : "_make_opera"
                }

class _BrowserManagementKeywords(KeywordGroup):

    def __init__(self):
        self._cache = BrowserCache()
        self._window_manager = WindowManager()
        self._speed_in_secs = float(0)
        self._timeout_in_secs = float(5)
        self._implicit_wait_in_secs = float(0)

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

    def open_browser(self, url, browser='firefox', alias=None,remote_url=False,
                desired_capabilities=None,ff_profile_dir=None):
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
        | opera            | Opera         |
        

        Note, that you will encounter strange behavior, if you open
        multiple Internet Explorer browser instances. That is also why
        `Switch Browser` only works with one IE browser at most.
        For more information see:
        http://selenium-grid.seleniumhq.org/faq.html#i_get_some_strange_errors_when_i_run_multiple_internet_explorer_instances_on_the_same_machine

        Optional 'remote_url' is the url for a remote selenium server for example
        http://127.0.0.1/wd/hub.  If you specify a value for remote you can
        also specify 'desired_capabilities' which is a string in the form
        key1:val1,key2:val2 that will be used to specify desired_capabilities
        to the remote server.  This is useful for doing things like specify a
        proxy server for internet explorer or for specify browser and os if your
        using saucelabs.com.

        Optional 'ff_profile_dir' is the path to the firefox profile dir if you
        wish to overwrite the default.
        """
        if remote_url:
            self._info("Opening broser '%s' to base url '%s' through remote server at '%s'"
                    % (browser, url, remote_url))
        else:
            self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        browser_name = browser
        browser = self._make_browser(browser_name,desired_capabilities,ff_profile_dir,remote_url)
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
        """Returns and logs id attributes of all windows known to the browser."""
        return self._log_list(self._window_manager.get_window_ids(self._current_browser()))

    def get_window_names(self):
        """Returns and logs names of all windows known to the browser."""
        values = self._window_manager.get_window_names(self._current_browser())

        # for backward compatibility, since Selenium 1 would always
        # return this constant value for the main window
        if len(values) and values[0] == 'undefined':
            values[0] = 'selenium_main_app_window'

        return self._log_list(values)

    def get_window_titles(self):
        """Returns and logs titles of all windows known to the browser."""
        return self._log_list(self._window_manager.get_window_titles(self._current_browser()))

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
        javascript name of the window. If multiple windows with
        same identifier are found, the first one is selected.

        Special locator `main` (default) can be used to select the main window.

        It is also possible to specify the approach Selenium2Library should take
        to find a window by specifying a locator strategy:

        | *Strategy* | *Example*                               | *Description*                        |
        | title      | Select Window `|` title=My Document     | Matches by window title              |
        | name       | Select Window `|` name=${name}          | Matches by window javascript name    |
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

    def get_selenium_implicit_wait(self):
        """Gets the wait in seconds that is waited by Selenium.

        See `Set Selenium Implicit Wait` for an explanation."""
        return robot.utils.secs_to_timestr(self._implicit_wait_in_secs)

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
        for browser in self._cache.browsers:
            browser.set_script_timeout(self._timeout_in_secs)
        return old_timeout

    def set_selenium_implicit_wait(self, seconds):
        """Sets Selenium 2's default implicit wait in seconds and
        sets the implicit wait for all open browsers.

        From selenium 2 function 'Sets a sticky timeout to implicitly 
            wait for an element to be found, or a command to complete.
            This method only needs to be called one time per session.'

        Example:
        | ${orig wait} = | Set Selenium Implicit Wait | 10 seconds |
        | Perform AJAX call that is slow |
        | Set Selenium Implicit Wait | ${orig wait} | 
        """
        old_wait = self.get_selenium_implicit_wait()
        self._implicit_wait_in_secs = robot.utils.timestr_to_secs(seconds)
        for browser in self._cache.get_open_browsers():
            browser.implicitly_wait(self._implicit_wait_in_secs)
        return old_wait
    

    def set_browser_implicit_wait(self, seconds):
        """Sets current browser's implicit wait in seconds.

        From selenium 2 function 'Sets a sticky timeout to implicitly 
            wait for an element to be found, or a command to complete.
            This method only needs to be called one time per session.'

        Example:
        | Set Browser Implicit Wait | 10 seconds |

        See also `Set Selenium Implicit Wait`.
        """
        implicit_wait_in_secs = robot.utils.timestr_to_secs(seconds)
        self._current_browser().implicitly_wait(implicit_wait_in_secs)

    # Private

    def _current_browser(self):
        if not self._cache.current:
            raise RuntimeError('No browser is open')
        return self._cache.current

    def _get_browser_token(self, browser_name):
        return BROWSER_NAMES.get(browser_name.lower().replace(' ', ''), browser_name)


    def _get_browser_creation_function(self,browser_name):
        return BROWSER_NAMES.get(browser_name.lower().replace(' ', ''), browser_name)

    def _make_browser(self , browser_name , desired_capabilities=None , profile_dir=None,
                    remote=None):

        creation_func = self._get_browser_creation_function(browser_name)
        browser = getattr(self,creation_func)(remote , desired_capabilities , profile_dir)

        if browser is None:
            raise ValueError(browser_name + " is not a supported browser.")

        browser.set_speed(self._speed_in_secs)
        browser.set_script_timeout(self._timeout_in_secs)
        browser.implicitly_wait(self._implicit_wait_in_secs)

        return browser


    def _make_ff(self , remote , desired_capabilites , profile_dir):
        
        if not profile_dir: profile_dir = FIREFOX_PROFILE_DIR
        profile = webdriver.FirefoxProfile(profile_dir)
        if remote:
            browser = self._create_remote_web_driver(webdriver.DesiredCapabilities.FIREFOX  , 
                        remote , desired_capabilites , profile)
        else:
            browser = webdriver.Firefox(firefox_profile=profile)
        return browser
    
    def _make_ie(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.Ie, 
                webdriver.DesiredCapabilities.INTERNETEXPLORER, remote, desired_capabilities)

    def _make_chrome(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.Chrome, 
                webdriver.DesiredCapabilities.CHROME, remote, desired_capabilities)

    def _make_opera(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.Opera, 
                webdriver.DesiredCapabilities.OPERA, remote, desired_capabilities)

    
    def _generic_make_browser(self, webdriver_type , desired_cap_type, remote_url, desired_caps):
        '''most of the make browser functions just call this function which creates the 
        appropriate web-driver'''
        if not remote_url: 
            browser = webdriver_type()
        else:
            browser = self._create_remote_web_driver(desired_cap_type,remote_url , desired_caps)
        return browser
    

    def _create_remote_web_driver(self , capabilities_type , remote_url , desired_capabilities=None , profile=None):
        '''parses the string based desired_capabilities which should be in the form
        key1:val1,key2:val2 and creates the associated remote web driver'''
        desired_cap = self._create_desired_capabilities(capabilities_type , desired_capabilities)
        return webdriver.Remote(desired_capabilities=desired_cap , command_executor=str(remote_url) ,                                       browser_profile=profile)


    def _create_desired_capabilities(self, capabilities_type, capabilities_string):
        desired_capabilities = capabilities_type
        if capabilities_string:
            for cap in capabilities_string.split(","):
                (key, value) = cap.split(":")
                desired_capabilities[key.strip()] = value.strip()
        return desired_capabilities
    
