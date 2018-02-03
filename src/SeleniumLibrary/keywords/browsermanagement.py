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

from selenium import webdriver

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.locators import WindowManager
from SeleniumLibrary.utils import (is_truthy, is_noney, secs_to_timestr,
                                   timestr_to_secs)

from .webdrivertools import WebDriverCreator


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
        self.drivers.close_all()

    @keyword
    def close_browser(self):
        """Closes the current browser."""
        if self.drivers.current:
            self.debug('Closing browser with session id {}.'
                       .format(self.driver.session_id))
            self.drivers.close()

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

        Optional ``alias`` is an alias given for this browser instance and
        it can be used for switching between browsers. An alternative
        approach for switching is using an index returned by this keyword.
        These indices start from 1, are incremented when new browsers are
        opened, and reset back to 1 when `Close All Browsers` is called.
        See `Switch Browser` for more information and examples.

        Optional ``remote_url`` is the URL for a
        [https://github.com/SeleniumHQ/selenium/wiki/Grid2|Selenium Grid].

        Optional ``desired_capabilities`` can be used to configure, for example,
        logging preferences for a browser or a browser and operating system
        when using [http://saucelabs.com|Sauce Labs]. Desired capabilities can
        be given either as a Python dictionary or as a string in format
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

        Applying ``desired_capabilities`` argument also for local browser is
        new in SeleniumLibrary 3.1.
        """
        if is_truthy(remote_url):
            self.info("Opening browser '%s' to base url '%s' through "
                      "remote server at '%s'." % (browser, url, remote_url))
        else:
            self.info("Opening browser '%s' to base url '%s'." % (browser, url))
        driver = self._make_driver(browser, desired_capabilities,
                                   ff_profile_dir, remote_url)
        try:
            driver.get(url)
        except Exception:
            self.ctx.register_driver(driver, alias)
            self.debug("Opened browser with session id %s but failed "
                       "to open url '%s'." % (driver.session_id, url))
            raise
        self.debug('Opened browser with session id %s.' % driver.session_id)
        return self.ctx.register_driver(driver, alias)

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
        return self.ctx.register_driver(driver, alias)

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
            self.drivers.switch(index_or_alias)
        except RuntimeError:
            raise RuntimeError("No browser with index or alias '%s' found."
                               % index_or_alias)
        self.debug('Switched to browser with Selenium session id %s.'
                   % self.driver.session_id)

    @keyword
    def get_source(self):
        """Returns the entire HTML source of the current page or frame."""
        return self.driver.page_source

    @keyword
    def get_title(self):
        """Returns the title of current page."""
        return self.driver.title

    @keyword
    def get_location(self):
        """Returns the current browser URL."""
        return self.driver.current_url

    @keyword
    def location_should_be(self, url):
        """Verifies that current URL is exactly ``url``."""
        actual = self.get_location()
        if actual != url:
            raise AssertionError("Location should have been '%s' but was "
                                 "'%s'." % (url, actual))
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
        self.log(source, loglevel)
        return source

    @keyword
    def log_title(self):
        """Logs and returns the title of current page."""
        title = self.get_title()
        self.info(title)
        return title

    @keyword
    def title_should_be(self, title, message=None):
        """Verifies that current page title equals ``title``.

        The ``message`` argument can be used to override the default error
        message.

        ``message`` argument is new in SeleniumLibrary 3.1.
        """
        actual = self.get_title()
        if actual != title:
            if is_noney(message):
                message = "Title should have been '%s' but was '%s'." % (title, actual)
            raise AssertionError(message)
        self.info("Page title is '%s'." % title)

    @keyword
    def go_back(self):
        """Simulates the user clicking the back button on their browser."""
        self.driver.back()

    @keyword
    def go_to(self, url):
        """Navigates the active browser instance to the provided ``url``."""
        self.info("Opening url '%s'" % url)
        self.driver.get(url)

    @keyword
    def reload_page(self):
        """Simulates user reloading page."""
        self.driver.refresh()

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
        for driver in self.drivers.active_drivers:
            self._monkey_patch_speed(driver)
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
        for driver in self.drivers.active_drivers:
            driver.set_script_timeout(self.ctx.timeout)
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
        for driver in self.drivers.active_drivers:
            driver.implicitly_wait(self.ctx.implicit_wait)
        return old_wait

    @keyword
    def set_browser_implicit_wait(self, value):
        """Sets the implicit wait value used by Selenium.

        Same as `Set Selenium Implicit Wait` but only affects the current
        browser.
        """
        self.driver.implicitly_wait(timestr_to_secs(value))

    def _make_driver(self, browser, desired_capabilities=None,
                     profile_dir=None, remote=None):
        driver = WebDriverCreator(self.log_dir).create_driver(
            browser=browser, desired_capabilities=desired_capabilities,
            remote_url=remote, profile_dir=profile_dir)
        driver.set_script_timeout(self.ctx.timeout)
        driver.implicitly_wait(self.ctx.implicit_wait)
        if self.ctx.speed:
            self._monkey_patch_speed(driver)
        return driver

    def _monkey_patch_speed(self, driver):
        def execute(self, driver_command, params=None):
            result = self._base_execute(driver_command, params)
            speed = self._speed if hasattr(self, '_speed') else 0.0
            if speed > 0:
                time.sleep(speed)
            return result
        if not hasattr(driver, '_base_execute'):
            driver._base_execute = driver.execute
            driver.execute = types.MethodType(execute, driver)
        driver._speed = self.ctx.speed
