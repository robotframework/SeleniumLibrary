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

import os
import time
import socket
import urlparse
try:
    import subprocess
except ImportError:
    subprocess = None  # subprocess not available on Python/Jython < 2.5

from robot.variables import GLOBAL_VARIABLES
from robot import utils
from selenium import selenium

from browser import Browser, NoBrowserOpen
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
from flex import Flex

from xpath import LocatorParser
from version import VERSION

__version__ = VERSION
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
    Selenium Server in `*params`.

    A custom automation friendly Firefox profile is enabled by default using
    the `-firefoxProfileTemplate` option.  If there is `user-extensions.js`
    file in the same directory as the jar, it is loaded automatically using the
    option `-userExtensions`.  For more information  about these options, see
    the documentation of the start_selenium_server method of the Selenium
    class.

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
    params = _add_default_user_extension(jarpath, list(params))
    return ['java', '-jar', jarpath] + _server_startup_params(params)

def _add_default_user_extension(jarpath, params):
    extpath = os.path.join(os.path.dirname(jarpath), 'user-extensions.js')
    if os.path.isfile(extpath) and '-userExtensions' not in params:
        params.extend(['-userExtensions', extpath])
    return params

def _server_startup_params(params):
    if FIREFOX_TEMPLATE_ARG not in params:
        return params + [FIREFOX_TEMPLATE_ARG, FIREFOX_PROFILE_DIR]
    index = params.index(FIREFOX_TEMPLATE_ARG)
    try:
        if params[index+1] == FIREFOX_DEFAULT_PROFILE:
            params[index:index+2] = []
    except IndexError:
        pass
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
                      Element, Screenshot, Table, TextField, Flex):
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

    All keywords in SeleniumLibrary that need to find an element on the page
    take an argument, `locator`. In the most common case, `locator` is
    matched against the values of key attributes of the particular element type.
    For example, `id` and `name` are key attributes to all elements, and
    locating elements is easy using just the `id` as a `locator`.

    Asterisk character may be used as a wildcard in locators, but it only works
    as the last character of the expression. In the middle of the locator it
    is interpreted as literal '*'.

    It is also possible to give an arbitrary XPath or DOM expression as
    `locator`. In this case, the expression must be prefixed with either
    'xpath=' or 'dom='.

    Examples:
    | Click Link      | my link | # Matches if either link text or 'id', 'name' or 'href' of a link equals 'my link' |
    | Page Should Contain Link | Link id * | # Passes if the page contain any link starting with 'Link id' |
    | Select Checkbox | xpath=//table[0]/input[@name='my_checkbox'] | # Using XPath |
    | Click Image     | dom=document.images[56] | # Using a DOM expression |

    Table related keywords, such as `Table Should Contain`, allow identifying
    tables either by an id, by a CSS locator, or by an XPath expression.
    The XPath support was added in SeleniumLibrary 2.6.

    Examples:
    | Table Should Contain | tableID | text |
    | Table Should Contain | css=h2.someClass ~ table:last-child() | text |
    | Table Should Contain | xpath=//table/[@name="myTable"] | text |

    *Locating Flex elements*

    SeleniumLibary 2.6 and newer support testing Adobe Flex and Flash
    applications using Flex Pilot tool. For more information, including the
    required bootstrapping, see
    http://code.google.com/p/robotframework-seleniumlibrary/wiki/FlexTesting

    By default Flex elements are located based on `id` they have in Flex source
    code. Other supported locators are `name`, `automationName`, `text`,
    `htmlText`, `label` and xpath-like `chain`. To use them, you need to prefix
    the value with the locator type like `name=example`. Locators also support
    `*` as a wildcard.

    Examples:
    | Click Flex Element | foo          | # Search element by id |
    | Click Flex Element | name=myName  | # Search element by name |
    | Click Flex Element | label=Hello! | # Search element by label text |
    | Click Flex Element | chain=id:someId/name:someName | # Search element first by id and then its child by name |
    | Click Flex Element | name=wild*   | # Name with wildcard |
    | Click Flex Element | chain=name:*llo/name:world | # Chain with wildcard |

    *Handling page load events*

    Some keywords that may cause a page to load take an additional argument
    `dont_wait` that is used to determine whether a new page is expected to
    load or not. By default, a page load is expected to happen whenever a link
    or image is clicked, or a form submitted. If a page load does not happen
    (if the link only executes some JavaScript, for example), a non-empty value
    must be given for the `dont_wait` argument. How much to wait is determined
    by a timeout discussed in the next section.

    There are also some keywords that may cause a page to load but by default
    we expect them not to. For these cases, the keywords have an optional `wait`
    argument, and providing a non-empty value for it will cause the keyword to
    wait. An other possibility is using `Wait Until Page Loaded` keyword
    which also accepts a custom timeout.

    Examples:
    | Click Link | link text    |            |          | # A page is expected to load. |
    | Click Link | another link | don't wait |          | # A page is not expected to load. |
    | Select Radio Button | group1 | value1  |          | # A page is not expected to load. |
    | Select Radio Button | group2 | value2  | and wait | # A page is expected to load. |

    *Timeouts*

    How much to wait when a new page is loaded is specified by a timeout
    that can be given in `importing` (default is 5 seconds) or dynamically
    with `Set Selenium Timeout` keyword.

    There are also several `Wait ...` keywords that take timeout as an
    argument. Starting from SeleniumLibrary 2.6 all these timeouts are
    optional and the same timeout used with page loads is used as a default.

    All timeouts can be given as numbers considered seconds (e.g. 0.5 or 42)
    or in Robot Framework's time syntax (e.g. '1.5 seconds' or '1 min 30 s').
    For more information about the time syntax see:
    http://robotframework.googlecode.com/svn/trunk/doc/userguide/RobotFrameworkUserGuide.html#time-format.

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

        `server_host` and `server_port` are used to connect to Selenium Server.
        Browsers opened with this SeleniumLibrary instance will be attached to
        that server. Note that the Selenium Server must be running before `Open
        Browser` keyword can be used. Selenium Server can be started with
        keyword `Start Selenium Server`. Starting from SeleniumLibrary 2.6.1,
        it is possible to give `server_host` as a URL with a possible embedded
        port, for example `http://192.168.52.1:4444`. If `server_host` contains
        port, the value of `server_port` is ignored.

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
        and later. This is demonstrated by the last two examples below.

        Examples:
        | Library | SeleniumLibrary | 15 | | | # Sets default timeout |
        | Library | SeleniumLibrary | | | 4455 | # Use default timeout and host but specify different port. |
        | Library | SeleniumLibrary | server_host=http://192.168.52.1:4444 | | | # Host as URL. |
        | Library | SeleniumLibrary | run_on_failure=Nothing | | | # Do nothing on failure. |
        """
        self._cache = utils.ConnectionCache()
        self._selenium = NoBrowserOpen()
        self.set_selenium_timeout(timeout or 5.0)
        self._server_host, self._server_port \
                = self._parse_host_and_port(server_host or 'localhost',
                                            server_port or 4444)
        self._jar_path = jar_path
        self._set_run_on_failure(run_on_failure)
        self._selenium_log = None
        self._locator_parser = LocatorParser(self)
        self._namegen = _NameGenerator()

    def _parse_host_and_port(self, host, port):
        if '://' in host:
            host = urlparse.urlparse(host).netloc
        if ':' in host:
            host, port = host.split(':', 1)
        return host, int(port)

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
        use this argument with `DEFAULT` value (case-sensitive). Using a
        custom Firefox profile automatically is a new feature in
        SeleniumLibrary 2.5. For more information see
        http://code.google.com/p/robotframework-seleniumlibrary/wiki/CustomFirefoxProfile

        3) Starting from SeleniumLibrary 2.6, if there is `user-extensions.js`
        file in the same directory as Selenium Server jar, it is loaded using
        the `-userExtensions` option.  This is not done if the option is
        defined in `params`.  By default, such extension file providing Flex
        testing support is loaded automatically.

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
        self._selenium = NoBrowserOpen()
        if self._selenium_log:
            self._selenium_log.close()

    def set_selenium_timeout(self, seconds):
        """Sets the timeout used by various keywords.

        Keywords that expect a page load to happen will fail if the page
        is not loaded within the timeout specified with `seconds`.
        Starting from SeleniumLibrary 2.6, this timeout is also the default
        timeout with various `Wait ...` keywords. See `introduction` for
        more information about timeouts and handling page loads.

        The previous timeout value is returned by this keyword and can
        be used to set the old value back later. The default timeout
        is 5 seconds, but it can be altered in `importing`.

        Example:
        | ${orig timeout} = | Set Selenium Timeout | 15 seconds |
        | Open page that loads slowly |
        | Set Selenium Timeout | ${orig timeout} |
        """
        timeout = utils.timestr_to_secs(seconds)
        old = getattr(self, '_timeout', timeout)
        self._timeout = timeout
        self._selenium.set_timeout(timeout * 1000)
        return utils.secs_to_timestr(old)

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

        Example:
        | Add Location Strategy | jquery | return Selenium.prototype.locateElementByJQuerySelector(locator, inDocument, inWindow); |
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

    def _wait_until(self, timeout, error, function, *args):
        timeout = self._get_timeout(timeout)
        error = error.replace('<TIMEOUT>', utils.secs_to_timestr(timeout))
        maxtime = time.time() + timeout
        while not function(*args):
            if time.time() > maxtime:
                raise AssertionError(error)
            time.sleep(0.2)

    def _get_timeout(self, timeout=None):
        if timeout:
            return utils.timestr_to_secs(timeout)
        return self._timeout

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s',''][len(items)==1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index+1, item))
        self._info('\n'.join(msg))
        return items


class _NameGenerator(object):
    def __init__(self):
        self._index = 0
    def next(self):
        self._index += 1
        return 'selenium-screenshot-%d.png' % self._index
