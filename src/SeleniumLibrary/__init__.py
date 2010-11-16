#  Copyright 2008-2010 Nokia Siemens Networks Oyj
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
    subprocess = None  # subprocess not available on Python/Jython < 2.5

from robot.errors import DataError
from robot.variables import GLOBAL_VARIABLES
from robot import utils
from selenium import selenium

from browser import Browser
from button import Button
from page import Page
from click import Click
from javascript import JavaScript
from mouse import Mouse
from select import Select
from element import Element
from screenshot import Screenshot
from textfield import TextField
from table import Table

from xpath import LocatorParser
from version import VERSION

__version__ = VERSION
BROWSER_ALIASES = {'ff': '*firefox',
                   'firefox': '*firefox',
                   'ie': '*iexplore',
                   'internetexplorer': '*iexplore',
                   'googlechrome': '*googlechrome',
                   'opera': '*opera',
                   'safari': '*safari'}
SELENIUM_CONNECTION_TIMEOUT = 40
_SELLIB_DIR = os.path.dirname(os.path.abspath(__file__))
SELENIUM_SERVER_PATH = os.path.join(_SELLIB_DIR, 'lib', 'selenium-server.jar')
FIREFOX_PROFILE_DIR = os.path.join(_SELLIB_DIR, 'firefoxprofile')
FIREFOX_DEFAULT_PROFILE = 'DEFAULT'
FIREFOX_TEMPLATE_ARG = '-firefoxProfileTemplate'


def start_selenium_server(logfile, jarpath=None, *params):
    """A hook to start the Selenium Server provided with SeleniumLibrary.

    `logfile` must be either an opened file (or file-like object) or None. If
    not None, Selenium Server log will be written to it.

    `jarpath` must be either the absolute path to the selenium-server.jar or
    None. If None, the jar file distributed with the library will be used.

    It is possible to give a list of additional command line options to
    Selenium Server in `*params`. A custom automation friendly Firefox
    profile is enabled by default using the `-firefoxProfileTemplate` option.
    For more information see the documentation of the start_selenium_server
    method of the Selenium class.

    Note that this function requires `subprocess` module which is available
    on Python/Jython 2.5 or newer.
    """
    if not subprocess:
        raise RuntimeError('This function requires `subprocess` module which '
                           'is available on Python/Jython 2.5 or newer')
    cmd = _server_startup_command(jarpath, *params)
    subprocess.Popen(cmd, stdout=logfile, stderr=subprocess.STDOUT)
    print 'Selenium Server started with command "%s" ' % ' '.join(cmd)

def _server_startup_command(jarpath, *params):
    if not jarpath:
        jarpath = SELENIUM_SERVER_PATH
    return ['java', '-jar', jarpath] + _command_line_args_for_server(*params)

def _command_line_args_for_server(*params):
    params = list(params)
    if not FIREFOX_TEMPLATE_ARG in params:
        params.extend([FIREFOX_TEMPLATE_ARG, FIREFOX_PROFILE_DIR])
    else:
        index = params.index(FIREFOX_TEMPLATE_ARG)
        value = params[index+1]
        if value.upper() == FIREFOX_DEFAULT_PROFILE:
            params = params[:index] + params[index+2:]
    return params


def shut_down_selenium_server(host='localhost', port=4444):
    """Shuts down the Selenium Server.

    `host` and `port` define where the location of Selenium Server.

    Does not fail even if the Selenium Server is not running.
    """
    try:
        selenium(host, port, '', '').shut_down_selenium_server()
    except socket.error:
        pass


class SeleniumLibrary(Browser, Page, Button, Click, JavaScript, Mouse, Select,
                      Element, Screenshot, Table, TextField):
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

    All table related keywords (`Table Should Contain`, etc.) allow to identity a table either by
    the id of the table element, or by a css locator. Both of the following examples work. It's not
    possible to use an xpath or dom expression, since the table keywords use a css locator internally.

    Table Examples:
    | Table Should Contain | tableID | $ 43,00 |
    | Table Should Contain | css=h2.someClass ~ table:last-child() | text |


    *Handling page load events*

    Some keywords that may cause a page to load take an additional argument
    `dont_wait` that is used to determine whether a new page is expected to
    load or not. By default, a page load is expected to happen whenever a link
    or image is clicked, or a form submitted. If a page load does not happen
    (if the link only executes some JavaScript, for example), a non-empty value
    must be given for the `dont_wait` argument.

    There are also some keywords that may cause a page to load but by default
    we expect them not to. For these cases, the keywords have an optional `wait`
    argument, and providing a non-empty value for it will cause the keyword to
    wait.

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
                 jar_path=None, run_on_failure='Capture Screenshot'):
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

        `run_on_failure` specifies the name of a SeleniumLibrary keyword to
        execute when another SeleniumLibrary keyword fails. By default
        `Capture Screenshot` will be used to take a screenshot of the situation.
        Using any value that is not a keyword name will disable this feature
        altogether. See `Register Keyword To Run On Failure` keyword for more
        information about this functionality that was added in SeleniumLibrary
        2.5.

        Because there are many optional arguments, it is often a good idea to
        use the handy named-arguments syntax supported by Robot Framework 2.5
        and later. This is demonstrated by the last example below.

        Examples:
        | Library | SeleniumLibrary | 15 | | | # Sets default timeout |
        | Library | SeleniumLibrary | | | 4455 | # Use default timeout and host but specify different port. |
        | Library | SeleniumLibrary | run_on_failure=Nothing | # Do nothing on failure. |
        """
        self._cache = utils.ConnectionCache()
        self._selenium = _NoBrowser()
        self.set_selenium_timeout(timeout or 5.0)
        self._server_host = server_host or 'localhost'
        self._server_port = int(server_port or 4444)
        self._jar_path = jar_path
        self._set_run_on_failure(run_on_failure)
        self._selenium_log = None
        self._locator_parser = LocatorParser(self)
        self._namegen = _NameGenerator()

    def start_selenium_server(self, *params):
        """Starts the Selenium Server provided with SeleniumLibrary.

        `params` can contain additional command line options given to the
        Selenium Server. This keyword uses some command line options
        automatically:

        1) The port given in `importing` is added to `params` automatically
        using the `-port` option.

        2) A custom Firefox profile that is included with the library
        and contains automation friendly settings is enabled via the
        `-firefoxProfileTemplate` option. You can override this
        profile with your own custom profile by using the same argument
        in `params` yourself. To use the default profile on your machine,
        use this argument with `DEFAULT` value. Using a custom Firefox
        profile automatically is a new feature in SeleniumLibrary 2.5.
        For more information see
        http://code.google.com/p/robotframework-seleniumlibrary/wiki/CustomFirefoxProfile

        Examples:
        | Start Selenium Server | | | # Default settings. Uses the Firefox profile supplied with the library. |
        | Start Selenium Server | -firefoxProfileTemplate | C:\\\\the\\\\path | # Uses custom Firefox profile. |
        | Start Selenium Server | -firefoxProfileTemplate | DEFAULT | # Uses default Firefox profile on your machine. |
        | Start Selenium Server | -avoidProxy | -ensureCleanSession | # Uses various Selenium Server settings. |

        All Selenium Server output is written into `selenium_server_log.txt`
        file in the same directory as the Robot Framework log file.

        If the test execution round starts and stops Selenium Server multiple
        times, it is best to open the server to different port each time.

        *NOTE:* This keyword requires `subprocess` module which is available
        on Python/Jython 2.5 or newer.
        """
        params = ('-port', str(self._server_port)) + params
        logpath = os.path.join(self._get_log_dir(), 'selenium_server_log.txt')
        self._selenium_log = open(logpath, 'w')
        start_selenium_server(self._selenium_log, self._jar_path, *params)
        self._html('Selenium server log is written to <a href="file://%s">%s</a>.'
                   % (logpath.replace('\\', '/'), logpath))

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
            raise RuntimeError("No browser with index or alias '%s' found."
                               % index_or_alias)

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
        the `do_command` method in the Python API [1]. In both cases the keyword
        returns the return value of the call directly without any modifications
        or verifications.

        Examples:
        | ${ret} = | Call Selenium API | is_element_present | # Python API |
        | Call Selenium API | double_click | element_id | # Python API |
        | Call Selenium API | doubleClick  | element_id | # RC API |

        [1] http://release.seleniumhq.org/selenium-remote-control/1.0-beta-2/doc/python/
        """
        try:
            method = getattr(self._selenium, method_name)
        except AttributeError:
            method = lambda *args: self._selenium.do_command(method_name, args)
        return method(*args)

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

    def _parse_locator(self, locator, tag=None):
        parsed_locator = self._locator_parser.locator_for(locator, tag)
        self._debug("Parsed locator '%s' to search expression '%s'"
                    % (locator, parsed_locator))
        return parsed_locator

    def _get_error_message(self, exception):
        # Cannot use unicode(exception) because it fails on Python 2.5 and
        # earlier if the message contains non-ASCII chars.
        # See for details: http://bugs.jython.org/issue1585
        return unicode(exception.args and exception.args[0] or '')

    def _error_contains(self, exception, message):
        return message in self._get_error_message(exception)

    def _wait_until(self, callable, timeout, error):
        maxtime = time.time() + timeout
        while not callable():
            if time.time() > maxtime:
                raise AssertionError(error)
            time.sleep(0.2)


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
