#  Copyright 2008-2009 Nokia Siemens Networks Oyj
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

import os
import time
import socket

try:
    import subprocess
except ImportError:
    # subprocess is not available in Jython 2.2 or older
    subprocess = None

from robot.errors import DataError
from robot.output import LEVELS
from robot.variables import GLOBAL_VARIABLES
from robot.running import NAMESPACES
from robot import utils

from selenium import selenium
from assertion import Assertion
from button import Button
from click import Click
from javascript import JavaScript
from select import Select
from element import Element
from xpath import LocatorParser
from screenshot import Screenshot
from table import Table

__version__ = '2.3-SNAPSHOT'
BROWSER_ALIASES = {'ff': '*firefox',
                   'firefox': '*firefox',
                   'ie': '*iexplore',
                   'internetexplorer': '*iexplore'}
SELENIUM_CONNECTION_TIMEOUT = 40


def start_selenium_server(logfile, jarpath=None, *params):
    """A hook to start the Selenium Server provided with SeleniumLibrary.

    `logfile` must be either an opened file (or file-like object) or None. If
    not None, Selenium Server log will be written to it.

    `jarpath` must be either the absolute path to the selenium-server.jar or
    None. If None, the jar file distributed with the library will be used.

    It is possible to give a list of additional command line options to
    Selenium Server in `*params`.

    Note that this function requires `subprocess` module which is available
    on Python/Jython 2.5 or newer.
    """
    if not subprocess:
        raise RuntimeError('This function requires `subprocess` module which '
                           'is available on Python/Jython 2.5 or newer')
    params = list(params)
    if not jarpath:
        jarpath = os.path.join(os.path.dirname(__file__), 'lib',
                               'selenium-server.jar')
    subprocess.Popen(['java', '-jar', jarpath] + params,
                     stdout=logfile, stderr=subprocess.STDOUT)


def shut_down_selenium_server(host='localhost', port=4444):
    """Shuts down the Selenium Server.

    `host` and `port` define where the location of Selenium Server.

    Does not fail even if the Selenium Server is not running.
    """
    try:
        selenium(host, port, '', '').do_command('shutDownSeleniumServer', [])
    except socket.error:
        pass


class SeleniumLibrary(Assertion, Button, Click, JavaScript, Select, Element,
                      Screenshot, Table):
    """SeleniumLibrary is a web testing library for Robot Test Automation Framework.

    It uses the Selenium Remote Control tool internally to control a web browser.
    See http://selenium-rc.openqa.org/ for more information on Selenium tool.

    SeleniumLibrary runs tests in a real browser instance. It should work in
    most modern browsers and can be used with both Python and Jython interpreters.

    *Before running the tests*

    Prior to running test cases using SeleniumLibrary, the Selenium Server must
    be started. This can be done using keyword `Start Selenium Server` or from
    the command line by using command: `java -jar
    /path/to/selenium-server.jar`. The Selenium Server is included in the
    SeleniumLibrary distribution and can be found under
    `[PythonLibs]/site-packages/SeleniumLibrary/lib`. Additionally, `Open
    Browser` keyword must be used in order to open browser in the desired
    location before any other keyword from the library may be used.

    *Locating elements*

    To do operations on elements, elements have to be identified. The most
    common way of doing this is by searching the values of key attributes of
    an element type. All keywords that operate on elements document the key
    attributes for that element type. If the given `locator` argument matches
    the value of any key attribute, the element is found.

    Asterisk character may be used as a wildcard in locators, but it only works
    as the last character of the expression. In the middle of the locator it
    is interpreted as literal '*'.

    It is also possible to give an arbitrary XPath or DOM expression as
    `locator`. In this case, the expression must be prefixed with either
    'xpath=' or 'dom='.

    Examples:
    | Click Link      | my link | # Matches if either link text or value of attribute 'id', 'name' or 'href' equals 'my link' |
    | Page Should Contain Link | Link id * | # Passes if the page contain any link starting with 'Link id' |
    | Select Checkbox | xpath=//table[0]/input[@name='my_checkbox'] | # Using XPath |
    | Click Image     | dom=document.images[56] | # Using a DOM expression |

    *Handling page load events*

    Some keywords that may cause a page to load take an additional argument
    `dont_wait` that is used to determine whether a new page is expected to
    load or not. By default, a page load is expected to happen whenever a link
    or image is clicked, or a form submitted. If a page load does not happen
    (if the link only executes some JavaScript, for example), a non-empty value
    must be given to `dont_wait` argument.

    There are also some keywords that may cause a page to load but by default
    we expect them not to. In these case, the keywords have an optional `wait`
    argument, and providing a non-empty value for it will cause the keyword to
    Examples:

    | Click Link | link text    |            |          | # A page is expected to load. |
    | Click Link | another link | don't wait |          | # A page is not expected to load. |
    | Select Radio Button | group1 | value1  |          | # A page is not expected to load. |
    | Select Radio Button | group2 | value2  | and wait | # A page is expected to load. |

    *Testing sites using https*

    Usually, https works out of the box. However, there may be trouble with
    self-signed certificates. We have a Wiki page describing how to test
    against these, using Firefox:
    http://code.google.com/p/robotframework-seleniumlibrary/wiki/HandlingSelfSignedCertificates
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, timeout=5.0, server_host='localhost', server_port=4444,
                 jar_path=None):
        """SeleniumLibrary can be imported with optional arguments.

        `timeout` is the default timeout used to wait for page load actions.
        It can be later set with `Set Selenium Timeout`

        `host` and `port` are used to connect to Selenium Server. Browsers
        opened with this SeleniumLibrary instance will be attached to that
        server. Note that the Selenium Server must be running before `Open
        Browser` keyword can be used. Selenium Server can be started with
        keyword `Start Selenium Server`.

        `jar_path` is the absolute path to the selenium-server.jar file to be
        used by the library. If set, a custom, modified version can be started
        instead of the default one distributed with the library.

        Examples:
        | Library | SeleniumLibrary | 15 | | | # Sets default timeout |
        | Library | SeleniumLibrary | | | 4455 | # Use default timeout and host but specify different port. |
        """
        self._cache = utils.ConnectionCache()
        self._selenium = _NoBrowser()
        self.set_selenium_timeout(timeout or 5.0)
        self._server_host = server_host or 'localhost'
        self._server_port = server_port and int(server_port) or 4444
        self._jar_path = jar_path
        self._selenium_log = None
        self._locator_parser = LocatorParser(self)
        self._namegen = _NameGenerator()

    def start_selenium_server(self, *params):
        """Starts the Selenium Server provided with SeleniumLibrary.

        `params` can contain additional command line parameters given
        to the started Selenium Server. Starting from 2.3 version the
        server will use the port given in `importing`
        automatically. In older versions the port must be given in
        `params`.

        Examples:
        | Start Selenium Server |
        | Start Selenium Server | -firefoxProfileTemplate | C:\\\\the\\\\path |
        | Start Selenium Server | -avoidProxy | -ensureCleanSession |

        All Selenium Server output is written into `selenium_server_log.txt`
        file in the same directory as the Robot Framework log file.

        If the test execution round starts and stops Selenium Server multiple
        times, it is best to open the server to different port each time.
        From 2.3 onwards, this is easiest done by importing the library with
        different parameters each time.

        *NOTE:* This keyword requires `subprocess` module which is available
        on Python/Jython 2.5 or newer.
        """
        params = ('-port', str(self._server_port)) + params
        logpath = os.path.join(self._get_log_dir(), 'selenium_server_log.txt')
        self._selenium_log = open(logpath, 'w')
        start_selenium_server(self._selenium_log, self._jar_path, *params)
        self._html('Selenium Server started to port %s. '
                   'Log is written to <a href="file://%s">%s</a>.'
                   % (self._server_port, logpath.replace('\\', '/'), logpath))

    def _get_log_dir(self):
        logfile = GLOBAL_VARIABLES['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return GLOBAL_VARIABLES['${OUTPUTDIR}']

    def stop_selenium_server(self):
        """Stops the selenium server (and closes all browsers)."""
        shut_down_selenium_server(self._server_host, self._server_port)
        self._selenium = _NoBrowser()
        if self._selenium_log:
            self._selenium_log.close()

    def open_browser(self, url, browser='firefox', alias=None):
        """Opens a new browser instance to given url.

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
        lists all the supported browsers.

        | *firefox         | FireFox   |
        | firefox          | FireFox   |
        | ff               | FireFox   |
        | *iexplore        | Internet Explorer |
        | ie               | Internet Explorer |
        | internetexplorer | Internet Explorer |
        | *safari          | Safari |
        | *googlechrome    | Google Chrome |
        | *opera           | Opera |

        Additionally, a string like `*custom /path/to/browser-executable` can
        be used to specify the browser directly. In this case, the path needs to
        point to an executable, not a script, otherwise the library may not be
        able to shut down the browser properly.
        
        Note, that you will encounter strange behaviour, if you open multiple 
        Internet Explorer browser instances. That's also why `Switch Browser` only
        works with one IE browser at most. 
        http://selenium-grid.seleniumhq.org/faq.html#i_get_some_strange_errors_when_i_run_multiple_internet_explorer_instances_on_the_same_machine
        """
        self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        browser = self._get_browser(browser)
        self._selenium = selenium(self._server_host, self._server_port, browser,
                                  url)
        self._connect_to_selenium_server()
        self._selenium.set_timeout(self._timeout)
        self._selenium.open(url)
        self._debug('Opened browser with Selenium session id %s' %
                        self._selenium.sessionId)
        return self._cache.register(self._selenium, alias)

    def _get_browser(self, browser):
        return BROWSER_ALIASES.get(browser.lower().replace(' ', ''), browser)

    def _connect_to_selenium_server(self):
        timeout = time.time() + SELENIUM_CONNECTION_TIMEOUT
        while time.time() < timeout:
            try:
                self._selenium.start()
            except socket.error:
                time.sleep(2)
            else:
                return
        self._selenium = _NoBrowser()
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
            self._selenium = _NoBrowser()

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
        self._selenium = _NoBrowser()
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
            raise DataError("No browser with index or alias '%s' found." % index_or_alias)

    def set_selenium_timeout(self, seconds):
        """Sets the timeout used by various keywords.

        The keywords that expect a page load to happen will fail if the page
        does not load within the time specified with `seconds`.  `seconds` may
        be given in Robot Framework time format and the default value is 5
        seconds. Returns the previous timeout value.
        """
        timeout = utils.timestr_to_secs(seconds) * 1000
        old = getattr(self, '_timeout', timeout)
        self._timeout = timeout
        self._selenium.set_timeout(self._timeout)
        return utils.secs_to_timestr(old/1000)

    def set_selenium_speed(self, seconds):
        """Sets the delay that is waited after each Selenium command.

        This is useful mainly in slowing down the test execution to be able to
        view the execution.  `seconds` may be given in Robot Framework time
        format.  Returns the previous speed value.

        Example:
        | Set Selenium Speed | 2 seconds |
        """
        old = self._selenium.get_speed()
        seconds = str(int(utils.timestr_to_secs(seconds)*1000))
        self._selenium.set_speed(seconds)
        return utils.secs_to_timestr(float(old)/1000)

    def call_selenium_api(self, method_name, *args):
        """Calls a method in the Selenium remote control API directly.

        This keyword can be used if some functionality provided by
        Selenium is not yet exposed as a keyword.

        `method_name` is the name of the method to call in the Selenium API and
        `args` specify the arguments it expects.

        The keyword first tries to find a method in Selenium's Python API
        provided by the `selenium.py` file. If no matching method is found, the
        keyword calls the Selenium Server's Remote Controller API directly via
        the `do_command` method in the Python API. In both cases the keyword
        returns the return value of the call directly without any modifications
        or verifications.

        Examples:
        | ${ret} = | Call Selenium API | is_element_present | # Python API |
        | Call Selenium API | double_click | element_id | # Python API |
        | Call Selenium API | doubleClick  | element_id | # RC API |
        """
        try:
            method = getattr(self._selenium, method_name)
        except AttributeError:
            method = lambda *args: self._selenium.do_command(method_name, args)
        return method(*args)

    def go_to(self, url):
        """Navigates the active browser instance to the provided URL."""
        self._info("Opening url '%s'" % url)
        self._selenium.open(url)

    def go_back(self, dont_wait=''):
        """Simulates the user clicking the "back" button on their browser.
        
        See `introduction` for details about locating elements and about meaning
        of `dont_wait` argument."""
        self._selenium.go_back()
        if not dont_wait:
            self._wait_for_page_to_load()

    def maximize_browser_window(self):
        """Maximizes current browser window."""
        self._selenium.window_maximize()

    def select_frame(self, locator):
        """Sets frame identified by `locator` as current frame.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        """
        self._info("Selecting frame '%s'." % locator)
        self._selenium.select_frame(self._parse_locator(locator))

    def unselect_frame(self):
        """Sets the top frame as the current frame."""
        self._selenium.select_frame('relative=top')

    def get_window_names(self):
        """Returns names of all windows known to the browser."""
        return self._selenium.get_all_window_names()

    def get_window_titles(self):
        """Returns titles of all windows known to the browser."""
        return self._selenium.get_all_window_titles()

    def get_window_identifiers(self):
        """Returns values of id attributes of all windows known to the browser."""
        return self._selenium.get_all_window_ids()

    def get_all_links(self):
        """Returns a list containing ids of all links found in current page.

        If a link has no id, an empty string will be in the list instead.
        """
        return self._selenium.get_all_links()

    def select_window(self, windowID=None):
        """Selects the window found with `windowID` as the context of actions.

        If the window is found, all subsequent commands use that window, until
        this keyword is used again. If the window is not found, this keyword fails.

        `windowID` may be either the title of the window or the name of the window
        in the JavaScript code that creates it. Name is second argument passed
        to JavaScript function window.open(). In case of multiple windows with
        same identifier are found, the first one is selected.

        To select main window, the argument can be left empty, or name 'main'
        can be used.

        Example:
        | Click Link | popup_link | don't wait | # opens new window |
        | Select Window | popupName |
        | Title Should Be | Popup Title |
        | Select Window |  | | # Chooses the main window again |
        """
        if not windowID or windowID.lower() == 'main':
            windowID = 'null'
        self._selenium.select_window(windowID)

    def close_window(self):
        """Closes currently opened pop-up window."""
        self._selenium.close()

    def get_location(self):
        """Returns the current location."""
        return self._selenium.get_location()

    def get_title(self):
        """Returns title of current page."""
        return self._selenium.get_title()

    def input_text(self, locator, text):
        """Types the given `text` into text field identified by `locator`.

        See `introduction` for details about locating elements.
        """
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        self._selenium.type(self._parse_locator(locator), text)

    def input_password(self, locator, text):
        """Types the given password into text field identified by `locator`.

        Difference between this keyword and `Input Text` is that this keyword
        does not log the given password. See `introduction` for details about
        locating elements.
        """
        self._info("Typing password into text field '%s'" % locator)
        self._selenium.type(self._parse_locator(locator), text)

    def get_value(self, locator):
        """Returns the value attribute of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._selenium.get_value(self._parse_locator(locator))

    def get_text(self, locator):
        """Returns the text of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._selenium.get_text(self._parse_locator(locator))

    def get_source(self):
        """Returns the entire html source of the current page or frame."""
        return self._selenium.get_html_source()

    def log_source(self, level='INFO'):
        """Logs and returns the entire html source of the current page or frame.

        `level` defines the log level. Valid log levels are 'WARN', 'INFO' (the default), 'DEBUG'
        and 'TRACE'. In case `level` is invalid, 'INFO' will be used."""
        level = level.upper()
        if not level in LEVELS:
            level = 'INFO'
        source = self.get_source()
        self._log(source, level)
        return source

    def focus(self, locator):
        """Sets focus to element identified by `locator`.

        This is useful for instance to direct native keystrokes to particular
        element using `Press Key Native`.
        """
        self._selenium.focus(locator)

    def drag_and_drop(self, locator, movement):
        """Drags element identified with `locator` by `movement`

        `movement is a string in format "+70 -300" interpreted as pixels in
        relation to elements current position.
        """
        self._selenium.dragdrop(self._parse_locator(locator), movement)

    def press_key(self, locator, key, wait=''):
        """Simulates user pressing key on element identified by `locator`.

        `key` is either a single character, or a numerical ASCII code of the key
        lead by '\\'.

        See `introduction` for details about `wait` argument.

        Examples:
        | Press Key | text_field   | q |
        | Press Key | login_button | \\13 | # ASCII code for enter key |

        Sometimes this keyword doesn't trigger the correct JavaScript event
        on the clicked element. In those cases `Press Key Native` can be
        used as a workaround. 
        
        The selenium command key_press [1] that is used internally exposes some
        erratic behaviour [2], especially when used with the Internet Explorer. If
        don't get the expected results, try `Press Key Native` instead.
        
        [1] http://release.seleniumhq.org/selenium-remote-control/1.0-beta-2/doc/python/selenium.selenium-class.html#key_press
        [2] http://jira.openqa.org/browse/SRC-385
        """
        self._selenium.key_press(locator, key)
        if wait:
            self._wait_for_page_to_load()

    def press_key_native(self, keycode, wait=''):
        """Simulates user pressing key by sending an operating system keystroke.

        `keycode` corresponds to `java.awt.event.KeyEvent` constants, which can
        be found from
        http://java.sun.com/javase/6/docs/api/constant-values.html#java.awt.event.KeyEvent.CHAR_UNDEFINED

        The key press does not target a particular element. An element can be
        chosen by first using `Focus` keyword.

        See `introduction` for details about `wait` argument.

        Examples:
        | Press Key Native | 517          | # Exclamation mark |
        | Focus            | login_button |
        | Press Key Native | 10           | # Enter key  |

        Notice that this keyword is very fragile and, for example, using the
        keyboard or mouse while tests are running often causes problems. It can
        be beneficial to bring the window to the front again with executing JavaScript:
        
        | Execute Javascript | window.focus() |          |
        | Focus              | login_button   |          |
        | Press Key Native   | 10             | and wait |
        """
        self._selenium.key_press_native(keycode)
        if wait:
            self._wait_for_page_to_load()

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
        supported options include 'path', 'domain' and 'recurse.' Format for
        `options` is "path=/path/, domain=.foo.com, recurse=true". The order of
        options is irrelevant. Note that specifying a domain that isn't a
        subset of the current domain will usually fail. Setting `recurse=true`
        will cause this keyword to search all sub-domains of current domain
        with all paths that are subset of current path. This can take a long
        time.
        """
        self._selenium.delete_cookie(name, options)

    def delete_all_cookies(self):
        """Deletes all cookies by calling `Delete Cookie` repeatedly."""
        self._selenium.delete_all_visible_cookies()

    def choose_file(self, identifier, file_path):
        """Inputs the `file_path` into file input field found by `identifier`

        From version 2.2.2 onwards, existence of `file_path` is not checked.
        `OperatingSystem.File Should Exist` can be used for that if needed.
        """
        if not os.path.isfile(file_path):
            self._info("The path '%s' does not exists in local file system." % file_path)
        self._selenium.type(identifier, file_path)

    def attach_file(self, locator, file_locator):
        """Sets a file input (upload) field identified by `locator` to the file
        given as `file_locator`.

        This method works when attaching files on browsers running on remote
        machines. The file to be attached must be placed on a web server
        accessible by the machine running the browser at the root of the server
        - any subdirectories will not work. `file_locator` is the URL to the
        file. Selenium RC will take care of downloading the file to the test
        machine and then attaching the file.

        Supported browsers: Firefox

        For files on the same machine use `Choose File` keyword.
        """
        self._selenium.attach_file(locator, file_locator)

    def add_location_strategy(self, strategy_name, function_definition):
        """Adds a custom location strategy.

        `strategy_name` is the name of the strategy; a prefix used when
        addressing an element.

        `function_definition` is the JavaScript that will be called. It must
        return a DOM reference, an array with DOM references, or null.

        Together with the modified selenium-server.jar it can provide a new
        method of locating elements on the page. For example, a jQuery
        strategy can be added to locate elements given jQuery selector syntax.

        For jQuery selector setup see:
        http://code.google.com/p/robotframework-seleniumlibrary/wiki/jQueryElementSelectors

        Examples:
        | ${func} = | return Selenium.prototype.locateElementByJQuerySelector(locator, inDocument, inWindow); |
        | Add Location Strategy | jquery | ${func} |
        | Page Should Contain Element | jquery=div.#data-table |
        """
        self._locator_parser.add_strategy(strategy_name)
        self._selenium.add_location_strategy(strategy_name, function_definition)

    def _log(self, message, level='INFO'):
        print '*%s* %s' % (level, message)

    def _info(self, message):
        self._log(message)

    def _debug(self, message):
        self._log(message, 'DEBUG')

    def _warn(self, message):
        self._log(message,  "WARN")

    def _html(self, message):
        self._log(message, 'HTML')

    def _wait_for_page_to_load(self, timeout=None):
        timeout = timeout is None and self._timeout or timeout
        self._selenium.wait_for_page_to_load(timeout)

    def _parse_locator(self, locator, tag=None):
        parsed_locator = self._locator_parser.locator_for(locator, tag)
        self._debug("Parsed locator '%s' to search expression '%s'"
                    % (locator, parsed_locator))
        return parsed_locator

    def _get_error_message(self, exception):
        # Cannot use unicode(exception) because it fails on Python 2.5 and earlier if the message contains Unicode chars
        # See for details: http://bugs.jython.org/issue1585
        return unicode(exception.args and exception.args[0] or '')

class _NoBrowser(object):
    set_timeout = lambda self, timeout: None
    def __getattr__(self, name):
        raise RuntimeError('No browser is open')
    def __nonzero__(self):
        return False


class _NameGenerator(object):
    def __init__(self):
        self._index = 0
    def next(self):
        self._index += 1
        return 'selenium-screenshot-%d.png' % self._index
