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

import time
import types
from datetime import timedelta
from typing import Optional, Union, Any, List

from selenium import webdriver
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.support.event_firing_webdriver import EventFiringWebDriver

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.locators import WindowManager
from SeleniumLibrary.utils import secs_to_timestr, _convert_timeout

from .webdrivertools import WebDriverCreator


class BrowserManagementKeywords(LibraryComponent):
    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self._window_manager = WindowManager(ctx)
        self._webdriver_creator = WebDriverCreator(self.log_dir)

    @keyword
    def close_all_browsers(self):
        """Closes all open browsers and resets the browser cache.

        After this keyword, new indexes returned from `Open Browser` keyword
        are reset to 1.

        This keyword should be used in test or suite teardown to make sure
        all browsers are closed.
        """
        self.debug("Closing all browsers.")
        self.drivers.close_all()

    @keyword
    def close_browser(self):
        """Closes the current browser."""
        if self.drivers.current:
            self.debug(f"Closing browser with session id {self.driver.session_id}.")
            self.drivers.close()

    @keyword
    def open_browser(
        self,
        url: Optional[str] = None,
        browser: str = "firefox",
        alias: Optional[str] = None,
        remote_url: Union[bool, str] = False,
        desired_capabilities: Union[dict, None, str] = None,
        ff_profile_dir: Union[FirefoxProfile, str, None] = None,
        options: Any = None,
        service_log_path: Optional[str] = None,
        executable_path: Optional[str] = None,
    ) -> str:
        """Opens a new browser instance to the optional ``url``.

        The ``browser`` argument specifies which browser to use. The
        supported browsers are listed in the table below. The browser names
        are case-insensitive and some browsers have multiple supported names.

        |    = Browser =    |        = Name(s) =       |
        | Firefox           | firefox, ff              |
        | Google Chrome     | googlechrome, chrome, gc |
        | Headless Firefox  | headlessfirefox          |
        | Headless Chrome   | headlesschrome           |
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
        project documentation] for more details. Headless Firefox and
        Headless Chrome are new additions in SeleniumLibrary 3.1.0
        and require Selenium 3.8.0 or newer.

        After opening the browser, it is possible to use optional
        ``url`` to navigate the browser to the desired address.

        Optional ``alias`` is an alias given for this browser instance and
        it can be used for switching between browsers. When same ``alias``
        is given with two `Open Browser` keywords, the first keyword will
        open a new browser, but the second one will switch to the already
        opened browser and will not open a new browser. The ``alias``
        definition overrules ``browser`` definition. When same ``alias``
        is used but a different ``browser`` is defined, then switch to
        a browser with same alias is done and new browser is not opened.
        An alternative approach for switching is using an index returned
        by this keyword. These indices start from 1, are incremented when new
        browsers are opened, and reset back to 1 when `Close All Browsers`
        is called. See `Switch Browser` for more information and examples.

        Optional ``remote_url`` is the URL for a
        [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid].

        Optional ``desired_capabilities`` can be used to configure, for example,
        logging preferences for a browser or a browser and operating system
        when using [http://saucelabs.com|Sauce Labs]. Desired capabilities can
        be given either as a Python dictionary or as a string in the format
        ``key1:value1,key2:value2``.
        [https://github.com/SeleniumHQ/selenium/wiki/DesiredCapabilities|
        Selenium documentation] lists possible capabilities that can be
        enabled.

        Optional ``ff_profile_dir`` is the path to the Firefox profile
        directory if you wish to overwrite the default profile Selenium
        uses. Notice that prior to SeleniumLibrary 3.0, the library
        contained its own profile that was used by default. The
        ``ff_profile_dir`` can also be an instance of the
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_firefox/selenium.webdriver.firefox.firefox_profile.html|selenium.webdriver.FirefoxProfile]
        . As a third option, it is possible to use `FirefoxProfile` methods
        and attributes to define the profile using methods and attributes
        in the same way as with ``options`` argument. Example: It is possible
        to use FirefoxProfile `set_preference` to define different
        profile settings. See ``options`` argument documentation in below
        how to handle backslash escaping.

        Optional ``options`` argument allows defining browser specific
        Selenium options. Example for Chrome, the ``options`` argument
        allows defining the following
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_chrome/selenium.webdriver.chrome.options.html#selenium.webdriver.chrome.options.Options|methods and attributes]
        and for Firefox these
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_firefox/selenium.webdriver.firefox.options.html?highlight=firefox#selenium.webdriver.firefox.options.Options|methods and attributes]
        are available. Please note that not all browsers, supported by the
        SeleniumLibrary, have Selenium options available. Therefore please
        consult the Selenium documentation which browsers do support
        the Selenium options. If ``browser`` argument is `android` then
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_chrome/selenium.webdriver.chrome.options.html#selenium.webdriver.chrome.options.Options|Chrome options]
        is used. Selenium options are also supported, when ``remote_url``
        argument is used.

        The SeleniumLibrary ``options`` argument accepts Selenium
        options in two different formats: as a string and as Python object
        which is an instance of the Selenium options class.

        The string format allows defining Selenium options methods
        or attributes and their arguments in Robot Framework test data.
        The method and attributes names are case and space sensitive and
        must match to the Selenium options methods and attributes names.
        When defining a method, it must be defined in a similar way as in
        python: method name, opening parenthesis, zero to many arguments
        and closing parenthesis. If there is a need to define multiple
        arguments for a single method, arguments must be separated with
        comma, just like in Python. Example: `add_argument("--headless")`
        or `add_experimental_option("key", "value")`. Attributes are
        defined in a similar way as in Python: attribute name, equal sign,
        and attribute value. Example, `headless=True`. Multiple methods
        and attributes must be separated by a semicolon. Example:
        `add_argument("--headless");add_argument("--start-maximized")`.

        Arguments allow defining Python data types and arguments are
        evaluated by using Python
        [https://docs.python.org/3/library/ast.html#ast.literal_eval|ast.literal_eval].
        Strings must be quoted with single or double quotes, example "value"
        or 'value'. It is also possible to define other Python builtin
        data types, example `True` or `None`, by not using quotes
        around the arguments.

        The string format is space friendly. Usually, spaces do not alter
        the defining methods or attributes. There are two exceptions.
        In some Robot Framework test data formats, two or more spaces are
        considered as cell separator and instead of defining a single
        argument, two or more arguments may be defined. Spaces in string
        arguments are not removed and are left as is. Example
        `add_argument ( "--headless" )` is same as
        `add_argument("--headless")`. But `add_argument(" --headless ")` is
        not same same as `add_argument ( "--headless" )`, because
        spaces inside of quotes are not removed. Please note that if
        options string contains backslash, example a Windows OS path,
        the backslash needs escaping both in Robot Framework data and
        in Python side. This means single backslash must be writen using
        four backslash characters. Example, Windows path:
        "C:\\path\\to\\profile" must be written as
        "C:\\\\\\\\path\\\\\\to\\\\\\\\profile". Another way to write
        backslash is use Python
        [https://docs.python.org/3/reference/lexical_analysis.html#string-and-bytes-literals|raw strings]
        and example write: r"C:\\\\path\\\\to\\\\profile".

        As last format, ``options`` argument also supports receiving
        the Selenium options as Python class instance. In this case, the
        instance is used as-is and the SeleniumLibrary will not convert
        the instance to other formats.
        For example, if the following code return value is saved to
        `${options}` variable in the Robot Framework data:
        | options = webdriver.ChromeOptions()
        | options.add_argument('--disable-dev-shm-usage')
        | return options

        Then the `${options}` variable can be used as an argument to
        ``options``.

        Example the ``options`` argument can be used to launch Chomium-based
        applications which utilize the
        [https://bitbucket.org/chromiumembedded/cef/wiki/UsingChromeDriver|Chromium Embedded Framework]
        . To lauch Chomium-based application, use ``options`` to define
        `binary_location` attribute and use `add_argument` method to define
        `remote-debugging-port` port for the application. Once the browser
        is opened, the test can interact with the embedded web-content of
        the system under test.

        Optional ``service_log_path`` argument defines the name of the
        file where to write the browser driver logs. If the
        ``service_log_path``  argument contain a  marker ``{index}``, it
        will be automatically replaced with unique running
        index preventing files to be overwritten. Indices start's from 1,
        and how they are represented can be customized using Python's
        [https://docs.python.org/3/library/string.html#format-string-syntax|
        format string syntax].

        Optional ``executable_path`` argument defines the path to the driver
        executable, example to a chromedriver or a geckodriver. If not defined
        it is assumed the executable is in the
        [https://en.wikipedia.org/wiki/PATH_(variable)|$PATH].

        Examples:
        | `Open Browser` | http://example.com | Chrome  |                                         |
        | `Open Browser` | http://example.com | Firefox | alias=Firefox                           |
        | `Open Browser` | http://example.com | Edge    | remote_url=http://127.0.0.1:4444/wd/hub |
        | `Open Browser` | about:blank        |         |                                         |
        | `Open Browser` | browser=Chrome     |         |                                         |

        Alias examples:
        | ${1_index} =    | `Open Browser` | http://example.com | Chrome  | alias=Chrome     | # Opens new browser because alias is new.         |
        | ${2_index} =    | `Open Browser` | http://example.com | Firefox |                  | # Opens new browser because alias is not defined. |
        | ${3_index} =    | `Open Browser` | http://example.com | Chrome  | alias=Chrome     | # Switches to the browser with Chrome alias.      |
        | ${4_index} =    | `Open Browser` | http://example.com | Chrome  | alias=${1_index} | # Switches to the browser with Chrome alias.      |
        | Should Be Equal | ${1_index}     | ${3_index}         |         |                  |                                                   |
        | Should Be Equal | ${1_index}     | ${4_index}         |         |                  |                                                   |
        | Should Be Equal | ${2_index}     | ${2}               |         |                  |                                                   |

        Example when using
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_chrome/selenium.webdriver.chrome.options.html#selenium.webdriver.chrome.options.Options|Chrome options]
        method:
        | `Open Browser` | http://example.com | Chrome | options=add_argument("--disable-popup-blocking"); add_argument("--ignore-certificate-errors") | # Sting format.                    |
        |  ${options} =  |     Get Options    |        |                                                                                               | # Selenium options instance.       |
        | `Open Browser` | http://example.com | Chrome | options=${options}                                                                            |                                    |
        | `Open Browser` | None               | Chrome | options=binary_location="/path/to/binary";add_argument("remote-debugging-port=port")          | # Start Chomium-based application. |
        | `Open Browser` | None               | Chrome | options=binary_location=r"C:\\\\path\\\\to\\\\binary"                                         | # Windows OS path escaping.        |

        Example for FirefoxProfile
        | `Open Browser` | http://example.com | Firefox | ff_profile_dir=/path/to/profile                                                  | # Using profile from disk.                       |
        | `Open Browser` | http://example.com | Firefox | ff_profile_dir=${FirefoxProfile_instance}                                        | # Using instance of FirefoxProfile.              |
        | `Open Browser` | http://example.com | Firefox | ff_profile_dir=set_preference("key", "value");set_preference("other", "setting") | # Defining profile using FirefoxProfile mehtods. |

        If the provided configuration options are not enough, it is possible
        to use `Create Webdriver` to customize browser initialization even
        more.

        Applying ``desired_capabilities`` argument also for local browser is
        new in SeleniumLibrary 3.1.

        Using ``alias`` to decide, is the new browser opened is new
        in SeleniumLibrary 4.0. The ``options`` and ``service_log_path``
        are new in SeleniumLibrary 4.0. Support for ``ff_profile_dir``
        accepting an instance of the `selenium.webdriver.FirefoxProfile`
        and support defining FirefoxProfile with methods and
        attributes are new in SeleniumLibrary 4.0.

        Making ``url`` optional is new in SeleniumLibrary 4.1.

        The ``executable_path`` argument is new in SeleniumLibrary 4.2.
        """
        index = self.drivers.get_index(alias)
        if index:
            self.info(f"Using existing browser from index {index}.")
            self.switch_browser(alias)
            if url:
                self.go_to(url)
            return index
        return self._make_new_browser(
            url,
            browser,
            alias,
            remote_url,
            desired_capabilities,
            ff_profile_dir,
            options,
            service_log_path,
            executable_path,
        )

    def _make_new_browser(
        self,
        url=None,
        browser="firefox",
        alias=None,
        remote_url=False,
        desired_capabilities=None,
        ff_profile_dir=None,
        options=None,
        service_log_path=None,
        executable_path=None,
    ):
        if remote_url:
            self.info(
                f"Opening browser '{browser}' to base url '{url}' through "
                f"remote server at '{remote_url}'."
            )
        else:
            self.info(f"Opening browser '{browser}' to base url '{url}'.")
        driver = self._make_driver(
            browser,
            desired_capabilities,
            ff_profile_dir,
            remote_url,
            options,
            service_log_path,
            executable_path,
        )
        driver = self._wrap_event_firing_webdriver(driver)
        index = self.ctx.register_driver(driver, alias)
        if url:
            try:
                driver.get(url)
            except Exception:
                self.debug(
                    f"Opened browser with session id {driver.session_id} but failed to open url '{url}'."
                )
                raise
        self.debug(f"Opened browser with session id {driver.session_id}.")
        return index

    @keyword
    def create_webdriver(
        self, driver_name: str, alias: Optional[str] = None, kwargs={}, **init_kwargs
    ) -> str:
        """Creates an instance of Selenium WebDriver.

        Like `Open Browser`, but allows passing arguments to the created
        WebDriver instance directly. This keyword should only be used if
        the functionality provided by `Open Browser` is not adequate.

        ``driver_name`` must be a WebDriver implementation name like Firefox,
        Chrome, Ie, Opera, Safari, PhantomJS, or Remote.

        The initialized WebDriver can be configured either with a Python
        dictionary ``kwargs`` or by using keyword arguments ``**init_kwargs``.
        These arguments are passed directly to WebDriver without any
        processing. See [https://seleniumhq.github.io/selenium/docs/api/py/api.html|
        Selenium API documentation] for details about the supported arguments.

        Examples:
        | # Use proxy with Firefox   |                |                              |                                      |
        | ${proxy}=                  | `Evaluate`     | selenium.webdriver.Proxy()   | modules=selenium, selenium.webdriver |
        | ${proxy.http_proxy}=       | `Set Variable` | localhost:8888               |                                      |
        | `Create Webdriver`         | Firefox        | proxy=${proxy}               |                                      |
        | # Use proxy with PhantomJS |                |                              |                                      |
        | ${service args}=           | `Create List`  | --proxy=192.168.132.104:8888 |                                      |
        | `Create Webdriver`         | PhantomJS      | service_args=${service args} |                                      |

        Returns the index of this browser instance which can be used later to
        switch back to it. Index starts from 1 and is reset back to it when
        `Close All Browsers` keyword is used. See `Switch Browser` for an
        example.
        """
        if not isinstance(kwargs, dict):
            raise RuntimeError("kwargs must be a dictionary.")
        for arg_name in kwargs:
            if arg_name in init_kwargs:
                raise RuntimeError(f"Got multiple values for argument '{arg_name}'.")
            init_kwargs[arg_name] = kwargs[arg_name]
        driver_name = driver_name.strip()
        try:
            creation_func = getattr(webdriver, driver_name)
        except AttributeError:
            raise RuntimeError(f"'{driver_name}' is not a valid WebDriver name.")
        self.info(f"Creating an instance of the {driver_name} WebDriver.")
        driver = creation_func(**init_kwargs)
        self.debug(
            f"Created {driver_name} WebDriver instance with session id {driver.session_id}."
        )
        driver = self._wrap_event_firing_webdriver(driver)
        return self.ctx.register_driver(driver, alias)

    def _wrap_event_firing_webdriver(self, driver):
        if not self.ctx.event_firing_webdriver:
            return driver
        self.debug("Wrapping driver to event_firing_webdriver.")
        return EventFiringWebDriver(driver, self.ctx.event_firing_webdriver())

    @keyword
    def switch_browser(self, index_or_alias: str):
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
            self.drivers.switch(index_or_alias)
        except RuntimeError:
            raise RuntimeError(
                f"No browser with index or alias '{index_or_alias}' found."
            )
        self.debug(
            f"Switched to browser with Selenium session id {self.driver.session_id}."
        )

    @keyword
    def get_browser_ids(self) -> List[str]:
        """Returns index of all active browser as list.

        Example:
        | @{browser_ids}= | Get Browser Ids   |                   |                |
        | FOR             | ${id}             | IN                | @{browser_ids} |
        |                 | @{window_titles}= | Get Window Titles | browser=${id}  |
        |                 | Log               | Browser ${id} has these windows: ${window_titles} | |
        | END             |                   |                   |                |

        See `Switch Browser` for more information and examples.

        New in SeleniumLibrary 4.0
        """
        return self.drivers.active_driver_ids

    @keyword
    def get_browser_aliases(self) -> List[str]:
        """Returns aliases of all active browser that has an alias as NormalizedDict.
        The dictionary contains the aliases as keys and the index as value.
        This can be accessed as dictionary ``${aliases.key}`` or as list ``@{aliases}[0]``.

        Example:
        | `Open Browser` | https://example.com   | alias=BrowserA | |
        | `Open Browser` | https://example.com   | alias=BrowserB | |
        | &{aliases}     | `Get Browser Aliases` |                | # &{aliases} = { BrowserA=1|BrowserB=2 } |
        | `Log`          | ${aliases.BrowserA}   |                | # logs ``1`` |
        | FOR            | ${alias}              | IN             | @{aliases} |
        |                | `Log`                 | ${alias}       | # logs ``BrowserA`` and ``BrowserB`` |
        | END            |                       |                | |

        See `Switch Browser` for more information and examples.

        New in SeleniumLibrary 4.0
        """
        return self.drivers.active_aliases

    @keyword
    def get_session_id(self) -> str:
        """Returns the currently active browser session id.

        New in SeleniumLibrary 3.2
        """
        return self.driver.session_id

    @keyword
    def get_source(self) -> str:
        """Returns the entire HTML source of the current page or frame."""
        return self.driver.page_source

    @keyword
    def get_title(self) -> str:
        """Returns the title of the current page."""
        return self.driver.title

    @keyword
    def get_location(self) -> str:
        """Returns the current browser window URL."""
        return self.driver.current_url

    @keyword
    def location_should_be(self, url: str, message: Optional[str] = None):
        """Verifies that the current URL is exactly ``url``.

        The ``url`` argument contains the exact url that should exist in browser.

        The ``message`` argument can be used to override the default error
        message.

        ``message`` argument is new in SeleniumLibrary 3.2.0.
        """
        actual = self.get_location()
        if actual != url:
            if message is None:
                message = f"Location should have been '{url}' but " f"was '{actual}'."
            raise AssertionError(message)
        self.info(f"Current location is '{url}'.")

    @keyword
    def location_should_contain(self, expected: str, message: Optional[str] = None):
        """Verifies that the current URL contains ``expected``.

        The ``expected`` argument contains the expected value in url.

        The ``message`` argument can be used to override the default error
        message.

        ``message`` argument is new in SeleniumLibrary 3.2.0.
        """
        actual = self.get_location()
        if expected not in actual:
            if message is None:
                message = (
                    f"Location should have contained '{expected}' but "
                    f"it was '{actual}'."
                )
            raise AssertionError(message)
        self.info(f"Current location contains '{expected}'.")

    @keyword
    def log_location(self) -> str:
        """Logs and returns the current browser window URL."""
        url = self.get_location()
        self.info(url)
        return url

    @keyword
    def log_source(self, loglevel: str = "INFO") -> str:
        """Logs and returns the HTML source of the current page or frame.

        The ``loglevel`` argument defines the used log level. Valid log
        levels are ``WARN``, ``INFO`` (default), ``DEBUG``, ``TRACE``
        and ``NONE`` (no logging).
        """
        source = self.get_source()
        self.log(source, loglevel)
        return source

    @keyword
    def log_title(self) -> str:
        """Logs and returns the title of the current page."""
        title = self.get_title()
        self.info(title)
        return title

    @keyword
    def title_should_be(self, title: str, message: Optional[str] = None):
        """Verifies that the current page title equals ``title``.

        The ``message`` argument can be used to override the default error
        message.

        ``message`` argument is new in SeleniumLibrary 3.1.
        """
        actual = self.get_title()
        if actual != title:
            if message is None:
                message = f"Title should have been '{title}' but was '{actual}'."
            raise AssertionError(message)
        self.info(f"Page title is '{title}'.")

    @keyword
    def go_back(self):
        """Simulates the user clicking the back button on their browser."""
        self.driver.back()

    @keyword
    def go_to(self, url):
        """Navigates the current browser window to the provided ``url``."""
        self.info(f"Opening url '{url}'")
        self.driver.get(url)

    @keyword
    def reload_page(self):
        """Simulates user reloading page."""
        self.driver.refresh()

    @keyword
    def get_selenium_speed(self) -> str:
        """Gets the delay that is waited after each Selenium command.

        The value is returned as a human-readable string like ``1 second``.

        See the `Selenium Speed` section above for more information.
        """
        return secs_to_timestr(self.ctx.speed)

    @keyword
    def get_selenium_timeout(self) -> str:
        """Gets the timeout that is used by various keywords.

        The value is returned as a human-readable string like ``1 second``.

        See the `Timeout` section above for more information.
        """
        return secs_to_timestr(self.ctx.timeout)

    @keyword
    def get_selenium_implicit_wait(self) -> str:
        """Gets the implicit wait value used by Selenium.

        The value is returned as a human-readable string like ``1 second``.

        See the `Implicit wait` section above for more information.
        """
        return secs_to_timestr(self.ctx.implicit_wait)

    @keyword
    def set_selenium_speed(self, value: timedelta) -> str:
        """Sets the delay that is waited after each Selenium command.

        The value can be given as a number that is considered to be
        seconds or as a human-readable string like ``1 second``.
        The previous value is returned and can be used to restore
        the original value later if needed.

        See the `Selenium Speed` section above for more information.

        Example:
        | `Set Selenium Speed` | 0.5 seconds |
        """
        old_speed = self.get_selenium_speed()
        self.ctx.speed = _convert_timeout(value)
        for driver in self.drivers.active_drivers:
            self._monkey_patch_speed(driver)
        return old_speed

    @keyword
    def set_selenium_timeout(self, value: timedelta) -> str:
        """Sets the timeout that is used by various keywords.

        The value can be given as a number that is considered to be
        seconds or as a human-readable string like ``1 second``.
        The previous value is returned and can be used to restore
        the original value later if needed.

        See the `Timeout` section above for more information.

        Example:
        | ${orig timeout} = | `Set Selenium Timeout` | 15 seconds |
        | `Open page that loads slowly` |
        | `Set Selenium Timeout` | ${orig timeout} |
        """
        old_timeout = self.get_selenium_timeout()
        self.ctx.timeout = _convert_timeout(value)
        for driver in self.drivers.active_drivers:
            driver.set_script_timeout(self.ctx.timeout)
        return old_timeout

    @keyword
    def set_selenium_implicit_wait(self, value: timedelta) -> str:
        """Sets the implicit wait value used by Selenium.

        The value can be given as a number that is considered to be
        seconds or as a human-readable string like ``1 second``.
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
        self.ctx.implicit_wait = _convert_timeout(value)
        for driver in self.drivers.active_drivers:
            driver.implicitly_wait(self.ctx.implicit_wait)
        return old_wait

    @keyword
    def set_browser_implicit_wait(self, value: timedelta):
        """Sets the implicit wait value used by Selenium.

        Same as `Set Selenium Implicit Wait` but only affects the current
        browser.
        """
        self.driver.implicitly_wait(_convert_timeout(value))

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
        driver = self._webdriver_creator.create_driver(
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

    def _monkey_patch_speed(self, driver):
        def execute(self, driver_command, params=None):
            result = self._base_execute(driver_command, params)
            speed = self._speed if hasattr(self, "_speed") else 0.0
            if speed > 0:
                time.sleep(speed)
            return result

        if not hasattr(driver, "_base_execute"):
            driver._base_execute = driver.execute
            driver.execute = types.MethodType(execute, driver)
        driver._speed = self.ctx.speed
