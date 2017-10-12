# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import os.path
import time
import types

from robot.errors import DataError
from robot.utils import NormalizedDict
from selenium import webdriver
from selenium.common.exceptions import NoSuchWindowException

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.locators import WindowManager
from SeleniumLibrary.utils import (is_falsy, is_truthy, secs_to_timestr,
                                   timestr_to_secs, SELENIUM_VERSION)


ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FIREFOX_PROFILE_DIR = os.path.join(ROOT_DIR, 'resources', 'firefoxprofile')
BROWSER_NAMES = NormalizedDict({
    'ff': "_make_ff",
    'firefox': "_make_ff",
    'ie': "_make_ie",
    'internetexplorer': "_make_ie",
    'googlechrome': "_make_chrome",
    'gc': "_make_chrome",
    'chrome': "_make_chrome",
    'opera': "_make_opera",
    'phantomjs': "_make_phantomjs",
    'htmlunit': "_make_htmlunit",
    'htmlunitwithjs': "_make_htmlunitwithjs",
    'android': "_make_android",
    'iphone': "_make_iphone",
    'safari': "_make_safari",
    'edge': "_make_edge"
})


class BrowserManagementKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self._window_manager = WindowManager(ctx)

    @keyword
    def close_all_browsers(self):
        """Closes all open browsers and resets the browser cache.

        After this keyword new indexes returned from `Open Browser` keyword
        are reset to 1.

        This keyword should be used in test or suite teardown to make sure
        all browsers are closed.
        """
        self.debug('Closing all browsers.')
        self.browsers.close_all()

    @keyword
    def close_browser(self):
        """Closes the current browser."""
        if self.browsers.current:
            self.debug('Closing browser with session id {}.'
                       .format(self.browser.session_id))
            self.browsers.close()

    @keyword
    def open_browser(self, url, browser='firefox', alias=None,
                     remote_url=False, desired_capabilities=None,
                     ff_profile_dir=None):
        """Opens a new browser instance to the given ``url``.

        The ``browser`` argument specifies which browser to use, and the
        supported browser are listed in the table below. The browser names
        are case-insensitive and some browsers have multiple supported names.

        |    = Browser =    |        = Name(s) =       |
        | Firefox           | firefox, ff              |
        | Google Chrome     | googlechrome, chrome, gc |
        | Internet Explorer | internetexplorer, ie     |
        | Edge              | edge                     |
        | Safari            | safari                   |
        | Opera             | opera                    |
        | Android           | android                  |
        | Iphone            | iphone                   |
        | PhantomJS         | phantomjs                |
        | HTMLUnit          | htmlunit                 |
        | HTMLUnit with Javascript | htmlunitwithjs    |

        To be able to actually use one of these browsers, you need to have
        a matching Selenium browser driver available. See the
        [https://github.com/robotframework/SeleniumLibrary#browser-drivers|
        project documentation] for more details.

        Optional ``alias`` is an alias given for this browser instance and
        it can be used for switching between browsers. An alternative
        approach for switching is using an index returned by this keyword.
        These indices start from 1, are incremented when new browsers are
        opened, and reset back to 1 when `Close All Browsers` is called.
        See `Switch Browser` for more information and examples.

        Optional ``remote_url`` is the URL for a remote Selenium server. If
        you specify a value for a remote, you can also specify
        ``desired_capabilities`` to configure, for example, a proxy server
        for Internet Explorer or a browser and operating system when using
        [http://saucelabs.com|Sauce Labs]. Desired capabilities can be given
        either as a Python dictionary or as a string in format
        ``key1:value1,key2:value2``.
        [https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities|
        Selenium documentation] lists possible capabilities that can be
        enabled.

        Optional ``ff_profile_dir`` is the path to the Firefox profile
        directory if you wish to overwrite the default profile Selenium
        uses. Notice that prior to SeleniumLibrary 3.0, the library
        contained its own profile that was used by default.

        Examples:
        | `Open Browser` | http://example.com | Chrome  |
        | `Open Browser` | http://example.com | Firefox | alias=Firefox |
        | `Open Browser` | http://example.com | Edge    | remote_url=http://127.0.0.1:4444/wd/hub |

        If the provided configuration options are not enough, it is possible
        to use `Create Webdriver` to customize browser initialization even
        more.
        """
        if is_truthy(remote_url):
            self.info("Opening browser '%s' to base url '%s' through "
                      "remote server at '%s'." % (browser, url, remote_url))
        else:
            self.info("Opening browser '%s' to base url '%s'." % (browser, url))
        browser_name = browser
        browser = self._make_browser(browser_name, desired_capabilities,
                                     ff_profile_dir, remote_url)
        try:
            browser.get(url)
        except Exception:
            self.ctx.register_browser(browser, alias)
            self.debug("Opened browser with session id %s but failed "
                       "to open url '%s'." % (browser.session_id, url))
            raise
        self.debug('Opened browser with session id %s.' % browser.session_id)
        return self.ctx.register_browser(browser, alias)

    @keyword
    def create_webdriver(self, driver_name, alias=None, kwargs={},
                         **init_kwargs):
        """Creates an instance of Selenium WebDriver.

        Like `Open Browser`, but allows passing arguments to the created
        WebDriver instance directly. This keyword should only be used if
        functionality provided by `Open Browser` is not adequate.

        ``driver_name`` must be an WebDriver implementation name like Firefox,
        Chrome, Ie, Opera, Safari, PhantomJS, or Remote.

        The initialized WebDriver can be configured either with a Python
        dictionary ``kwargs`` or by using keyword arguments ``**init_kwargs``.
        These arguments are passed directly to WebDriver without any
        processing. See [https://seleniumhq.github.io/selenium/docs/api/py/api.html|
        Selenium API documentation] for details about the supported arguments.

        Examples:
        | # Use proxy with Firefox   |                |                                           |                         |
        | ${proxy}=                  | `Evaluate`     | sys.modules['selenium.webdriver'].Proxy() | sys, selenium.webdriver |
        | ${proxy.http_proxy}=       | `Set Variable` | localhost:8888                            |                         |
        | `Create Webdriver`         | Firefox        | proxy=${proxy}                            |                         |
        | # Use proxy with PhantomJS |                |                                           |                         |
        | ${service args}=           | `Create List`  | --proxy=192.168.132.104:8888              |                         |
        | `Create Webdriver`         | PhantomJS      | service_args=${service args}              |                         |

        Returns the index of this browser instance which can be used later to
        switch back to it. Index starts from 1 and is reset back to it when
        `Close All Browsers` keyword is used. See `Switch Browser` for an
        example.
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
            raise RuntimeError("'%s' is not a valid WebDriver name." % driver_name)
        self.info("Creating an instance of the %s WebDriver." % driver_name)
        driver = creation_func(**init_kwargs)
        self.debug("Created %s WebDriver instance with session id %s."
                   % (driver_name, driver.session_id))
        return self.ctx.register_browser(driver, alias)

    @keyword
    def switch_browser(self, index_or_alias):
        """Switches between active browsers using ``index_or_alias``.

        Indices are returned by the `Open Browser` keyword and aliases can
        be given to it explicitly. Indices start from 1.

        Example:
        | `Open Browser`        | http://google.com | ff       |
        | `Location Should Be`  | http://google.com |          |
        | `Open Browser`        | http://yahoo.com  | ie       | alias=second |
        | `Location Should Be`  | http://yahoo.com  |          |
        | `Switch Browser`      | 1                 | # index  |
        | `Page Should Contain` | I'm feeling lucky |          |
        | `Switch Browser`      | second            | # alias  |
        | `Page Should Contain` | More Yahoo!       |          |
        | `Close All Browsers`  |                   |          |

        Above example expects that there was no other open browsers when
        opening the first one because it used index ``1`` when switching to
        it later. If you are not sure about that, you can store the index
        into a variable as below.

        | ${index} =         | `Open Browser` | http://google.com |
        | # Do something ... |                |                   |
        | `Switch Browser`   | ${index}       |                   |
        """
        try:
            self.browsers.switch(index_or_alias)
        except RuntimeError:
            raise RuntimeError("No browser with index or alias '%s' found."
                               % index_or_alias)
        self.debug('Switched to browser with Selenium session id %s.'
                   % self.browser.session_id)

    @keyword
    def close_window(self):
        """Closes currently opened pop-up window."""
        self.browser.close()

    @keyword
    def get_window_identifiers(self):
        """Returns and logs id attributes of all known browser windows."""
        ids = [info.id for info in self._window_manager.get_window_infos()]
        return self._log_list(ids)

    @keyword
    def get_window_names(self):
        """Returns and logs names of all known browser windows."""
        names = [info.name for info in self._window_manager.get_window_infos()]
        return self._log_list(names)

    @keyword
    def get_window_titles(self):
        """Returns and logs titles of all known browser windows."""
        titles = [info.title for info in self._window_manager.get_window_infos()]
        return self._log_list(titles)

    @keyword
    def maximize_browser_window(self):
        """Maximizes current browser window."""
        self.browser.maximize_window()

    @keyword
    def get_window_size(self):
        """Returns current window width and height as integers.

        See also `Set Window Size`.

        Example:
        | ${width} | ${height}= | `Get Window Size` |
        """
        size = self.browser.get_window_size()
        return size['width'], size['height']

    @keyword
    def set_window_size(self, width, height):
        """Sets current windows size to given ``width`` and ``height``.

        Values can be given using strings containing numbers or by using
        actual numbers. See also `Get Window Size`.

        Browsers have a limit how small they can be set. Trying to set them
        smaller will cause the actual size to be bigger than the requested
        size.

        Example:
        | `Set Window Size` | 800 | 600 |
        """
        return self.browser.set_window_size(int(width), int(height))

    @keyword
    def get_window_position(self):
        """Returns current window position.

        Position is relative to the top left corner of the screen. Returned
        values are integers. See also `Set Window Position`.

        Example:
        | ${x} | ${y}= | `Get Window Position` |
        """
        position = self.browser.get_window_position()
        return position['x'], position['y']

    @keyword
    def set_window_position(self, x, y):
        """Sets window position using ``x`` and ``y`` coordinates.

        The position is relative to the top left corner of the screen,
        but some browsers exclude possible task bar set by the operating
        system from the calculation. The actual position may thus be
        different with different browsers.

        Values can be given using strings containing numbers or by using
        actual numbers. See also `Get Window Position`.

        Example:
        | `Set Window Position` | 100 | 200 |
        """
        self.browser.set_window_position(int(x), int(y))

    @keyword
    def select_frame(self, locator):
        """Sets frame identified by ``locator`` as the current frame.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        
        See `Unselect Frame` to cancel the frame selection and return to the Main frame.
        
        Please note that the frame search always start from the document root or main frame.
        
        Example:
        | Select Frame   | xpath: //frame[@name='top]/iframe[@name='left'] | # Selects the 'left' iframe |
        | Click Link     | foo                                             | # Clicks link 'foo' in 'left' iframe |
        | Unselect Frame |                                                 | # Returns to main frame |
        | Select Frame   | left                                            | # Selects the 'top' frame |        
        """
        self.info("Selecting frame '%s'." % locator)
        element = self.find_element(locator)
        self.browser.switch_to.frame(element)

    @keyword
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

        It is also possible to specify the approach SeleniumLibrary should take
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
            return self.browser.current_window_handle
        except NoSuchWindowException:
            pass
        finally:
            self._window_manager.select(locator)

    @keyword
    def get_log(self, log_type):
        """Get the specified Selenium log.

        The ``log_type` argument defines which log to get. Possible values
        are ``browser``, ``driver``, ``client``, and ``server``.

        New in SeleniumLibrary 3.0.
        """
        return self.browser.get_log(log_type)

    @keyword
    def list_windows(self):
        """Return all current window handles as a list."""
        return self.browser.window_handles

    @keyword
    def unselect_frame(self):
        """Sets the top frame as the current frame.
        
        In practice cancels a previous `Select Frame` call.
        """
        self.browser.switch_to.default_content()

    @keyword
    def get_location(self):
        """Returns the current browser URL."""
        return self.browser.current_url

    @keyword
    def get_locations(self):
        """Returns and logs URLs of all known browser windows."""
        urls = [info.url for info in self._window_manager.get_window_infos()]
        return self._log_list(urls)

    @keyword
    def get_source(self):
        """Returns the entire HTML source of the current page or frame."""
        return self.browser.page_source

    @keyword
    def get_title(self):
        """Returns the title of current page."""
        return self.browser.title

    @keyword
    def location_should_be(self, url):
        """Verifies that current URL is exactly ``url``."""
        actual = self.get_location()
        if actual != url:
            raise AssertionError("Location should have been '%s' but was '%s'"
                                 % (url, actual))
        self.info("Current location is '%s'." % url)

    @keyword
    def location_should_contain(self, expected):
        """Verifies that current URL contains ``expected``."""
        actual = self.get_location()
        if expected not in actual:
            raise AssertionError("Location should have contained '%s' "
                                 "but it was '%s'." % (expected, actual))
        self.info("Current location contains '%s'." % expected)

    @keyword
    def log_location(self):
        """Logs and returns the current URL."""
        url = self.get_location()
        self.info(url)
        return url

    @keyword
    def log_source(self, loglevel='INFO'):
        """Logs and returns the HTML source of the current page or frame.

        The ``loglevel`` argument defines the used log level. Valid log
        levels are ``WARN``, ``INFO`` (default), ``DEBUG``, and ``NONE``
        (no logging).
        """
        source = self.get_source()
        self.log(source, loglevel.upper())
        return source

    @keyword
    def log_title(self):
        """Logs and returns the title of current page."""
        title = self.get_title()
        self.info(title)
        return title

    @keyword
    def title_should_be(self, title):
        """Verifies that current page title equals ``title``."""
        actual = self.get_title()
        if actual != title:
            raise AssertionError("Title should have been '%s' but was '%s'."
                                 % (title, actual))
        self.info("Page title is '%s'." % title)

    @keyword
    def go_back(self):
        """Simulates the user clicking the back button on their browser."""
        self.browser.back()

    @keyword
    def go_to(self, url):
        """Navigates the active browser instance to the provided ``url``."""
        self.info("Opening url '%s'" % url)
        self.browser.get(url)

    @keyword
    def reload_page(self):
        """Simulates user reloading page."""
        self.browser.refresh()

    @keyword
    def get_selenium_speed(self):
        """Gets the delay that is waited after each Selenium command.

        The value is returned as a human readable string like ``1 second``.

        See the `Selenium Speed` section above for more information.
        """
        return secs_to_timestr(self.ctx.speed)

    @keyword
    def get_selenium_timeout(self):
        """Gets the timeout that is used by various keywords.

        The value is returned as a human readable string like ``1 second``.

        See the `Timeout` section above for more information.
        """
        return secs_to_timestr(self.ctx.timeout)

    @keyword
    def get_selenium_implicit_wait(self):
        """Gets the implicit wait value used by Selenium.

        The value is returned as a human readable string like ``1 second``.

        See the `Implicit wait` section above for more information.
        """
        return secs_to_timestr(self.ctx.implicit_wait)

    @keyword
    def set_selenium_speed(self, value):
        """Sets the delay that is waited after each Selenium command.

        The value can be given as a number that is considered to be
        seconds or as a human readable string like ``1 second``.
        The previous value is returned and can be used to restore
        the original value later if needed.

        See the `Selenium Speed` section above for more information.

        Example:
        | `Set Selenium Speed` | 0.5 seconds |
        """
        old_speed = self.get_selenium_speed()
        self.ctx.speed = timestr_to_secs(value)
        for browser in self.browsers.browsers:
            self._monkey_patch_speed(browser)
        return old_speed

    @keyword
    def set_selenium_timeout(self, value):
        """Sets the timeout that is used by various keywords.

        The value can be given as a number that is considered to be
        seconds or as a human readable string like ``1 second``.
        The previous value is returned and can be used to restore
        the original value later if needed.

        See the `Timeout` section above for more information.

        Example:
        | ${orig timeout} = | `Set Selenium Timeout` | 15 seconds |
        | `Open page that loads slowly` |
        | `Set Selenium Timeout` | ${orig timeout} |
        """
        old_timeout = self.get_selenium_timeout()
        self.ctx.timeout = timestr_to_secs(value)
        for browser in self.browsers.get_open_browsers():
            browser.set_script_timeout(self.ctx.timeout)
        return old_timeout

    @keyword
    def set_selenium_implicit_wait(self, value):
        """Sets the implicit wait value used by Selenium.

        The value can be given as a number that is considered to be
        seconds or as a human readable string like ``1 second``.
        The previous value is returned and can be used to restore
        the original value later if needed.

        This keyword sets the implicit wait for all opened browsers.
        Use `Set Browser Implicit Wait` to set it only to the current
        browser.

        See the `Implicit wait` section above for more information.

        Example:
        | ${orig wait} = | `Set Selenium Implicit Wait` | 10 seconds |
        | `Perform AJAX call that is slow` |
        | `Set Selenium Implicit Wait` | ${orig wait} |
        """
        old_wait = self.get_selenium_implicit_wait()
        self.ctx.implicit_wait = timestr_to_secs(value)
        for browser in self.browsers.get_open_browsers():
            browser.implicitly_wait(self.ctx.implicit_wait)
        return old_wait

    @keyword
    def set_browser_implicit_wait(self, value):
        """Sets the implicit wait value used by Selenium.

        Same as `Set Selenium Implicit Wait` but only affects the current
        browser.
        """
        self.browser.implicitly_wait(timestr_to_secs(value))

    def _get_browser_creation_function(self, browser_name):
        try:
            func_name = BROWSER_NAMES[browser_name]
        except KeyError:
            raise ValueError(browser_name + " is not a supported browser.")
        return getattr(self, func_name)

    def _make_browser(self, browser_name, desired_capabilities=None,
                      profile_dir=None, remote=None):
        creation_func = self._get_browser_creation_function(browser_name)
        browser = creation_func(remote, desired_capabilities, profile_dir)
        browser.set_script_timeout(self.ctx.timeout)
        browser.implicitly_wait(self.ctx.implicit_wait)
        if self.ctx.speed:
            self._monkey_patch_speed(browser)
        return browser

    def _make_ff(self, remote, desired_capabilities, profile_dir):
        if is_falsy(profile_dir):
            profile = webdriver.FirefoxProfile()
        else:
            profile = webdriver.FirefoxProfile(profile_dir)
        if is_truthy(remote):
            browser = self._create_remote_web_driver(
                webdriver.DesiredCapabilities.FIREFOX, remote,
                desired_capabilities, profile)
        else:
            browser = webdriver.Firefox(firefox_profile=profile,
                                        **self._geckodriver_log_config)
        return browser

    def _make_ie(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.Ie,
                webdriver.DesiredCapabilities.INTERNETEXPLORER, remote, desired_capabilities)

    def _make_chrome(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.Chrome,
                webdriver.DesiredCapabilities.CHROME, remote, desired_capabilities)

    def _make_opera(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.Opera,
                webdriver.DesiredCapabilities.OPERA, remote, desired_capabilities)

    def _make_phantomjs(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.PhantomJS,
                webdriver.DesiredCapabilities.PHANTOMJS, remote, desired_capabilities)

    def _make_htmlunit(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.Remote,
                webdriver.DesiredCapabilities.HTMLUNIT, remote, desired_capabilities)

    def _make_htmlunitwithjs(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.Remote,
                webdriver.DesiredCapabilities.HTMLUNITWITHJS, remote, desired_capabilities)

    def _make_android(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.Remote,
                webdriver.DesiredCapabilities.ANDROID, remote, desired_capabilities)

    def _make_iphone(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.Remote,
                webdriver.DesiredCapabilities.IPHONE, remote, desired_capabilities)

    def _make_safari(self, remote, desired_capabilities, profile_dir):
        return self._generic_make_browser(webdriver.Safari,
                webdriver.DesiredCapabilities.SAFARI, remote, desired_capabilities)

    def _make_edge(self, remote, desired_capabilities, profile_dir):
        if hasattr(webdriver, 'Edge'):
            return self._generic_make_browser(webdriver.Edge,
                webdriver.DesiredCapabilities.EDGE, remote, desired_capabilities)
        else:
            raise ValueError("Edge is not a supported browser with your version of Selenium python library. Please, upgrade to minimum required version 2.47.0.")

    def _generic_make_browser(self, webdriver_type , desired_cap_type, remote_url, desired_caps):
        '''most of the make browser functions just call this function which creates the
        appropriate web-driver'''
        if is_falsy(remote_url):
            browser = webdriver_type()
        else:
            browser = self._create_remote_web_driver(desired_cap_type,
                                                     remote_url, desired_caps)
        return browser

    def _create_remote_web_driver(self, capabilities_type, remote_url, desired_capabilities=None, profile=None):
        '''parses the string based desired_capabilities if neccessary and
        creates the associated remote web driver'''

        desired_capabilities_object = capabilities_type.copy()

        if not isinstance(desired_capabilities, dict):
            desired_capabilities = self._parse_capabilities_string(desired_capabilities)

        desired_capabilities_object.update(desired_capabilities or {})

        return webdriver.Remote(desired_capabilities=desired_capabilities_object,
                command_executor=str(remote_url), browser_profile=profile)

    def _parse_capabilities_string(self, capabilities_string):
        '''parses the string based desired_capabilities which should be in the form
        key1:val1,key2:val2
        '''
        desired_capabilities = {}

        if is_falsy(capabilities_string):
            return desired_capabilities

        for cap in capabilities_string.split(","):
            (key, value) = cap.split(":", 1)
            desired_capabilities[key.strip()] = value.strip()

        return desired_capabilities

    def _get_speed(self, browser):
        return browser._speed if hasattr(browser, '_speed') else 0.0

    def _monkey_patch_speed(self, browser):
        def execute(self, driver_command, params=None):
            result = self._base_execute(driver_command, params)
            speed = self._speed if hasattr(self, '_speed') else 0.0
            if speed > 0:
                time.sleep(speed)
            return result
        if not hasattr(browser, '_base_execute'):
            browser._base_execute = browser.execute
            browser.execute = types.MethodType(execute, browser)
        browser._speed = self.ctx.speed

    def _log_list(self, items, what='item'):
        msg = [
            'Altogether {} {}.'.format(
                len(items), what if len(items) == 1 else '{}s'.format(what))
        ]
        for index, item in enumerate(items):
            msg.append('{}: {}'.format(index + 1, item))
        self.info('\n'.join(msg))
        return items

    @property
    def _geckodriver_log_config(self):
        if SELENIUM_VERSION.major == '3':
            return {'log_path': os.path.join(self.log_dir, 'geckodriver.log')}
        return {}
