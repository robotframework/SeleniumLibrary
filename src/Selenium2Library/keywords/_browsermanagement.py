import os
import robot
from robot.errors import DataError
from selenium import webdriver
from Selenium2Library import webdrivermonkeypatches
from Selenium2Library.utils import BrowserCache
from Selenium2Library.locators import WindowManager
from keywordgroup import KeywordGroup
from selenium.common.exceptions import NoSuchWindowException

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIREFOX_PROFILE_DIR = os.path.join(ROOT_DIR, 'resources', 'firefoxprofile')
BROWSER_NAMES = {'ff': "_make_ff",
                 'firefox': "_make_ff",
                 'ie': "_make_ie",
                 'internetexplorer': "_make_ie",
                 'googlechrome': "_make_chrome",
                 'gc': "_make_chrome",
                 'chrome': "_make_chrome",
                 'opera' : "_make_opera",
                 'phantomjs' : "_make_phantomjs",
                 'htmlunit' : "_make_htmlunit",
                 'htmlunitwithjs' : "_make_htmlunitwithjs",
                 'android': "_make_android",
                 'iphone': "_make_iphone",
                 'safari': "_make_safari",
                 'edge': "_make_edge"
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
        | phantomjs        | PhantomJS     |
        | htmlunit         | HTMLUnit      |
        | htmlunitwithjs   | HTMLUnit with Javascipt support |
        | android          | Android       |
        | iphone           | Iphone        |
        | safari           | Safari        |
        | edge             | Edge          |


        Note, that you will encounter strange behavior, if you open
        multiple Internet Explorer browser instances. That is also why
        `Switch Browser` only works with one IE browser at most.
        For more information see:
        http://selenium-grid.seleniumhq.org/faq.html#i_get_some_strange_errors_when_i_run_multiple_internet_explorer_instances_on_the_same_machine

        Optional 'remote_url' is the url for a remote selenium server for example
        http://127.0.0.1:4444/wd/hub. If you specify a value for remote you can
        also specify 'desired_capabilities' which is a string in the form
        key1:val1,key2:val2 that will be used to specify desired_capabilities
        to the remote server. This is useful for doing things like specify a
        proxy server for internet explorer or for specify browser and os if your
        using saucelabs.com. 'desired_capabilities' can also be a dictonary
        (created with 'Create Dictionary') to allow for more complex configurations.

        Optional 'ff_profile_dir' is the path to the firefox profile dir if you
        wish to overwrite the default.
        """
        if remote_url:
            self._info("Opening browser '%s' to base url '%s' through remote server at '%s'"
                    % (browser, url, remote_url))
        else:
            self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        browser_name = browser
        browser = self._make_browser(browser_name,desired_capabilities,ff_profile_dir,remote_url)
        try:
            browser.get(url)
        except:
            self._cache.register(browser, alias)
            self._debug("Opened browser with session id %s but failed to open url '%s'"
                        % (browser.session_id, url))
            raise
        self._debug('Opened browser with session id %s'
                    % browser.session_id)
        return self._cache.register(browser, alias)

    def create_webdriver(self, driver_name, alias=None, kwargs={}, **init_kwargs):
        """Creates an instance of a WebDriver.

        Like `Open Browser`, but allows passing arguments to a WebDriver's
        __init__. _Open Browser_ is preferred over _Create Webdriver_ when
        feasible.

        Returns the index of this browser instance which can be used later to
        switch back to it. Index starts from 1 and is reset back to it when
        `Close All Browsers` keyword is used. See `Switch Browser` for
        example.

        `driver_name` must be the exact name of a WebDriver in
        _selenium.webdriver_ to use. WebDriver names include: Firefox, Chrome,
        Ie, Opera, Safari, PhantomJS, and Remote.

        Use keyword arguments to specify the arguments you want to pass to
        the WebDriver's __init__. The values of the arguments are not
        processed in any way before being passed on. For Robot Framework
        < 2.8, which does not support keyword arguments, create a keyword
        dictionary and pass it in as argument `kwargs`. See the
        [http://selenium.googlecode.com/git/docs/api/py/api.html|Selenium API Documentation]
        for information about argument names and appropriate argument values.

        Examples:
        | # use proxy for Firefox     |              |                                           |                         |
        | ${proxy}=                   | Evaluate     | sys.modules['selenium.webdriver'].Proxy() | sys, selenium.webdriver |
        | ${proxy.http_proxy}=        | Set Variable | localhost:8888                            |                         |
        | Create Webdriver            | Firefox      | proxy=${proxy}                            |                         |
        | # use a proxy for PhantomJS |              |                                           |                         |
        | ${service args}=            | Create List  | --proxy=192.168.132.104:8888              |                         |
        | Create Webdriver            | PhantomJS    | service_args=${service args}              |                         |

        Example for Robot Framework < 2.8:
        | # debug IE driver |                   |                  |                                |
        | ${kwargs}=        | Create Dictionary | log_level=DEBUG  | log_file=%{HOMEPATH}${/}ie.log |
        | Create Webdriver  | Ie                | kwargs=${kwargs} |                                |
        """
        if not isinstance(kwargs, dict):
            raise RuntimeError("kwargs must be a dictionary.")
        for arg_name in kwargs:
            if arg_name in init_kwargs:
                raise RuntimeError("Got multiple values for argument '%s'." % arg_name)
            init_kwargs[arg_name] = kwargs[arg_name]
        driver_name = driver_name.strip()
        try:
            creation_func = getattr(webdriver, driver_name)
        except AttributeError:
            raise RuntimeError("'%s' is not a valid WebDriver name" % driver_name)
        self._info("Creating an instance of the %s WebDriver" % driver_name)
        driver = creation_func(**init_kwargs)
        self._debug("Created %s WebDriver instance with session id %s" % (driver_name, driver.session_id))
        return self._cache.register(driver, alias)

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
        self._current_browser().maximize_window()

    def get_window_size(self):
        """Returns current window size as `width` then `height`.

        Example:
        | ${width} | ${height}= | Get Window Size |
        """
        size = self._current_browser().get_window_size()
        return size['width'], size['height']

    def set_window_size(self, width, height):
        """Sets the `width` and `height` of the current window to the specified values.

        Example:
        | Set Window Size | ${800} | ${600}       |
        | ${width} | ${height}= | Get Window Size |
        | Should Be Equal | ${width}  | ${800}    |
        | Should Be Equal | ${height} | ${600}    |
        """
        return self._current_browser().set_window_size(width, height)

    def get_window_position(self):
        """Returns current window position as `x` then `y`.

        Example:
        | ${x} | ${y}= | Get Window Position |
        """
        position = self._current_browser().get_window_position()
        return position['x'], position['y']

    def set_window_position(self, x, y):
        """Sets the position `x` and `y` of the current window to the specified values.

        Example:
        | Set Window Size | ${1000} | ${0}       |
        | ${x} | ${y}= | Get Window Position |
        | Should Be Equal | ${x}      | ${1000}   |
        | Should Be Equal | ${y}      | ${0}      |
        """
        return self._current_browser().set_window_position(x, y)

    def select_frame(self, locator):
        """Sets frame identified by `locator` as current frame.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        """
        self._info("Selecting frame '%s'." % locator)
        element = self._element_find(locator, True, True)
        self._current_browser().switch_to_frame(element)

    def select_window(self, locator=None):
        """Selects the window matching locator and return previous window handle.

        locator: any of name, title, url, window handle, excluded handle's list, or special words.
        return: either current window handle before selecting, or None if no current window.

        If the window is found, all subsequent commands use that window, until
        this keyword is used again. If the window is not found, this keyword fails.

        By default, when a locator value is provided,
        it is matched against the title of the window and the
        javascript name of the window. If multiple windows with
        same identifier are found, the first one is selected.

        There are some special locators for searching target window:
        string 'main' (default): select the main window;
        string 'self': only return current window handle;
        string 'new': select the last-indexed window assuming it is the newest opened window
        window list: select the first window not in given list (See 'List Windows' to get the list)

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
        try:
            return self._current_browser().get_current_window_handle()
        except NoSuchWindowException:
            pass
        finally:
            self._window_manager.select(self._current_browser(), locator)

    def list_windows(self):
        """Return all current window handles as a list"""
        return self._current_browser().get_window_handles()

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
        WARN, INFO (default), DEBUG, and NONE (no logging).
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
        See `Timeouts` for more information about timeouts.

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
        for browser in self._cache.get_open_browsers():
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

    def _get_browser_creation_function(self, browser_name):
        func_name = BROWSER_NAMES.get(browser_name.lower().replace(' ', ''))
        return getattr(self, func_name) if func_name else None

    def _make_browser(self, browser_name, desired_capabilities=None,
                      profile_dir=None, remote=None):
        creation_func = self._get_browser_creation_function(browser_name)

        if not creation_func:
            raise ValueError(browser_name + " is not a supported browser.")

        browser = creation_func(remote, desired_capabilities, profile_dir)
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

    def _make_phantomjs(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.PhantomJS,
                webdriver.DesiredCapabilities.PHANTOMJS, remote, desired_capabilities)

    def _make_htmlunit(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.Remote,
                webdriver.DesiredCapabilities.HTMLUNIT, remote, desired_capabilities)

    def _make_htmlunitwithjs(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.Remote,
                webdriver.DesiredCapabilities.HTMLUNITWITHJS, remote, desired_capabilities)

    def _make_android(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.Remote,
                webdriver.DesiredCapabilities.ANDROID, remote, desired_capabilities)

    def _make_iphone(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.Remote,
                webdriver.DesiredCapabilities.IPHONE, remote, desired_capabilities)

    def _make_safari(self , remote , desired_capabilities , profile_dir):
        return self._generic_make_browser(webdriver.Safari,
                webdriver.DesiredCapabilities.SAFARI, remote, desired_capabilities)

    def _make_edge(self , remote , desired_capabilities , profile_dir):
        if hasattr(webdriver, 'Edge'):
            return self._generic_make_browser(webdriver.Edge,
                webdriver.DesiredCapabilities.EDGE, remote, desired_capabilities)
        else:
            raise ValueError("Edge is not a supported browser with your version of Selenium python library. Please, upgrade to minimum required version 2.47.0.")

    def _generic_make_browser(self, webdriver_type , desired_cap_type, remote_url, desired_caps):
        '''most of the make browser functions just call this function which creates the
        appropriate web-driver'''
        if not remote_url:
            browser = webdriver_type()
        else:
            browser = self._create_remote_web_driver(desired_cap_type,remote_url , desired_caps)
        return browser

    def _create_remote_web_driver(self , capabilities_type , remote_url , desired_capabilities=None , profile=None):
        '''parses the string based desired_capabilities if neccessary and
        creates the associated remote web driver'''

        desired_capabilities_object = capabilities_type.copy()

        if type(desired_capabilities) in (str, unicode):
            desired_capabilities = self._parse_capabilities_string(desired_capabilities)

        desired_capabilities_object.update(desired_capabilities or {})

        return webdriver.Remote(desired_capabilities=desired_capabilities_object,
                command_executor=str(remote_url), browser_profile=profile)

    def _parse_capabilities_string(self, capabilities_string):
        '''parses the string based desired_capabilities which should be in the form
        key1:val1,key2:val2
        '''
        desired_capabilities = {}

        if not capabilities_string:
            return desired_capabilities

        for cap in capabilities_string.split(","):
            (key, value) = cap.split(":", 1)
            desired_capabilities[key.strip()] = value.strip()

        return desired_capabilities
