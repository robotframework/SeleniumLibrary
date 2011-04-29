#  Copyright 2008-2011 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time
import socket

from robot.errors import DataError

from selenium import selenium
from runonfailure import RunOnFailure


BROWSER_ALIASES = {'ff': '*firefox',
                   'firefox': '*firefox',
                   'ie': '*iexplore',
                   'internetexplorer': '*iexplore',
                   'googlechrome': '*googlechrome',
                   'opera': '*opera',
                   'safari': '*safari'}
SELENIUM_CONNECTION_TIMEOUT = 40


class Browser(RunOnFailure):
    """Contains keywords for doing browser actions."""

    def open_browser(self, url, browser='firefox', alias=None):
        """Opens a new browser instance to given URL.

        Possible already opened connections are cached.

        Returns the index of this browser instance which can be used later to
        switch back to it. Index starts from 1 and is reset back to it when
        `Close All Browsers` keyword is used. See `Switch Browser` for
        example.

        Optional alias is a alias for the browser instance and it can be used
        for switching between browsers similarly as the index. See `Switch
        Browser` for more details about that.

        Possible values for `browser` are all the values supported by Selenium
        and some aliases that are defined for convenience. The table below
        lists the aliases for most common supported browsers.

        | firefox          | FireFox   |
        | ff               | FireFox   |
        | ie               | Internet Explorer |
        | internetexplorer | Internet Explorer |
        | safari           | Safari |
        | googlechrome     | Google Chrome |
        | opera            | Opera |

        Additionally, a string like `*custom /path/to/browser-executable` can
        be used to specify the browser directly. In this case, the path needs to
        point to an executable, not a script, otherwise the library may not be
        able to shut down the browser properly.

        Note, that you will encounter strange behavior, if you open
        multiple Internet Explorer browser instances. That is also why
        `Switch Browser` only works with one IE browser at most.
        For more information see:
        http://selenium-grid.seleniumhq.org/faq.html#i_get_some_strange_errors_when_i_run_multiple_internet_explorer_instances_on_the_same_machine
        """
        self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        browser = self._get_browser(browser)
        self._selenium = selenium(self._server_host, self._server_port, browser,
                                  url)
        self._connect_to_selenium_server()
        self._selenium.set_timeout(self._timeout * 1000)
        self._selenium.open(url, ignoreResponseCode=True)
        self._debug('Opened browser with Selenium session id %s'
                    % self._selenium.sessionId)
        return self._cache.register(self._selenium, alias)

    def _get_browser(self, browser):
        return BROWSER_ALIASES.get(browser.lower().replace(' ', ''), browser)

    def _connect_to_selenium_server(self):
        timeout = time.time() + SELENIUM_CONNECTION_TIMEOUT
        while time.time() < timeout:
            try:
                self._selenium.start()
            # AssertionError occurs on Jython: http://bugs.jython.org/issue1697
            except (socket.error, AssertionError):
                time.sleep(2)
            else:
                return
        self._selenium = NoBrowserOpen()
        raise RuntimeError("Could not connect to Selenium Server in %d seconds. "
                           "Please make sure Selenium Server is running."
                           % SELENIUM_CONNECTION_TIMEOUT)

    def close_browser(self):
        """Closes the current browser."""
        if self._selenium:
            self._debug('Closing browser with Selenium session id %s'
                        % self._selenium.sessionId)
            self._selenium.stop()
            self._cache.current = None
            self._selenium = NoBrowserOpen()

    def close_all_browsers(self):
        """Closes all open browsers and empties the connection cache.

        After this keyword new indexes get from Open Browser keyword are reset
        to 1.

        This keyword should be used in test or suite teardown to make sure
        all browsers are closed.
        """
        # ConnectionCache's connections attribute was renamed to _connections
        # in RF 2.0.2 (which was actually a stupid decision)
        try:
            connections = self._cache._connections
        except AttributeError:
            connections = self._cache.connections
        for sel in connections:
            if sel is not None and sel.sessionId is not None:
                self._debug('Closing browser with Selenium session id %s'
                            % sel.sessionId)
                sel.stop()
        self._selenium = NoBrowserOpen()
        self._cache.empty_cache()

    def switch_browser(self, index_or_alias):
        """Switches between active browsers using index or alias.

        Index is got from `Open Browser` and alias can be given to it.

        Examples:
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
            self._selenium = self._cache.switch(index_or_alias)
            self._debug('Switched to browser with Selenium session id %s'
                         % self._selenium.sessionId)
        except DataError:
            raise RuntimeError("No browser with index or alias '%s' found."
                               % index_or_alias)

    def go_to(self, url):
        """Navigates the active browser instance to the provided URL."""
        self._info("Opening url '%s'" % url)
        self._selenium.open(url, ignoreResponseCode=True)

    def wait_until_page_loaded(self, timeout=None):
        """Waits for a page load to happen.

        This keyword can be used after performing an action that causes a page
        load to ensure that following keywords see the page fully loaded.

        `timeout` is the time to wait for the page load to happen, after which
        this keyword fails. If `timeout` is not provided, the value given in
        `importing` or using keyword `Set Timeout` is used.

        Many of the keywords that cause a page load take an optional argument
        `dont_wait` that can be also used to wait/not wait page load. See
        `introduction` for more details.

        This keyword was added in SeleniumLibrary 2.5.
        """
        timeout = self._get_timeout(timeout)
        self._selenium.wait_for_page_to_load(timeout * 1000)

    def reload_page(self):
        """Simulates user reloading page.

        New in SeleniumLibrary 2.7.
        """
        self._selenium.refresh()

    def go_back(self, dont_wait=''):
        """Simulates the user clicking the "back" button on their browser.

        See `introduction` for details about locating elements and about meaning
        of `dont_wait` argument."""
        self._selenium.go_back()
        if not dont_wait:
            self.wait_until_page_loaded()

    def maximize_browser_window(self):
        """Maximizes current browser window."""
        self._selenium.window_maximize()

    def get_window_names(self):
        """Returns and logs names of all windows known to the browser."""
        return self._log_list(self._selenium.get_all_window_names(), 'name')

    def get_window_titles(self):
        """Returns and logs titles of all windows known to the browser."""
        return self._log_list(self._selenium.get_all_window_titles(), 'title')

    def get_window_identifiers(self):
        """Returns and logs id attributes of all windows known to the browser."""
        return self._log_list(self._selenium.get_all_window_ids(), 'identifier')

    def select_window(self, locator='main'):
        """Selects the window found with `locator` as the context of actions.

        If the window is found, all subsequent commands use that window, until
        this keyword is used again. If the window is not found, this keyword fails.

        `locator` may be either the title of the window or the name of the window
        in the JavaScript code that creates it. If multiple windows with
        same identifier are found, the first one is selected.

        Special locator `main` (default) can be used to select the main window.

        Example:
        | Click Link | popup_link | don't wait | # opens new window |
        | Select Window | popupName |
        | Title Should Be | Popup Title |
        | Select Window |  | | # Chooses the main window again |

        *NOTE:* Selecting windows opened by links with target `_blank` does
        not seem to work on Internet Explorer.
        """
        if locator.lower() == 'main':
            locator = 'null'
        self._selenium.select_window(locator)

    def close_window(self):
        """Closes currently opened pop-up window."""
        self._selenium.close()

    def get_location(self):
        """Returns the current location."""
        return self._selenium.get_location()

    def get_cookies(self):
        """Returns all cookies of the current page."""
        return self._selenium.get_cookie()

    def get_cookie_value(self, name):
        """Returns value of cookie found with `name`.

        If no cookie is found with `name`, this keyword fails.
        """
        return self._selenium.get_cookie_by_name(name)

    def delete_cookie(self, name, options=''):
        """Deletes cookie matching `name` and `options`.

        If the cookie is not found, nothing happens.

        `options` is the options for the cookie as a string. Currently
        supported options include `path`, `domain` and `recurse.` Format for
        `options` is `path=/path/, domain=.foo.com, recurse=true`. The order of
        options is irrelevant. Note that specifying a domain that is not a
        subset of the current domain will usually fail. Setting `recurse=true`
        will cause this keyword to search all sub-domains of current domain
        with all paths that are subset of current path. This can take a long
        time.
        """
        self._selenium.delete_cookie(name, options)

    def delete_all_cookies(self):
        """Deletes all cookies by calling `Delete Cookie` repeatedly."""
        self._selenium.delete_all_visible_cookies()


class NoBrowserOpen(object):
    set_timeout = lambda self, timeout: None

    def __getattr__(self, name):
        raise RuntimeError('No browser is open')

    def __nonzero__(self):
        return False
