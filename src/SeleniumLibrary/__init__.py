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
import re
from collections import namedtuple
from inspect import getdoc, isclass

from robot.api import logger
from robot.errors import DataError
from robot.libraries.BuiltIn import BuiltIn
from robot.utils import is_string
from robot.utils.importer import Importer

from SeleniumLibrary.base import DynamicCore, LibraryComponent
from SeleniumLibrary.errors import NoOpenBrowser, PluginError
from SeleniumLibrary.keywords import (AlertKeywords,
                                      BrowserManagementKeywords,
                                      CookieKeywords,
                                      ElementKeywords,
                                      FormElementKeywords,
                                      FrameKeywords,
                                      JavaScriptKeywords,
                                      RunOnFailureKeywords,
                                      ScreenshotKeywords,
                                      SelectElementKeywords,
                                      TableElementKeywords,
                                      WaitingKeywords,
                                      WebDriverCache,
                                      WindowKeywords)
from SeleniumLibrary.keywords.screenshot import EMBED
from SeleniumLibrary.locators import ElementFinder
from SeleniumLibrary.utils import LibraryListener, timestr_to_secs, is_truthy


__version__ = '4.4.0'


class SeleniumLibrary(DynamicCore):
    """SeleniumLibrary is a web testing library for Robot Framework.

    This document explains how to use keywords provided by SeleniumLibrary.
    For information about installation, support, and more, please visit the
    [https://github.com/robotframework/SeleniumLibrary|project pages].
    For more information about Robot Framework, see http://robotframework.org.

    SeleniumLibrary uses the Selenium WebDriver modules internally to
    control a web browser. See http://seleniumhq.org for more information
    about Selenium in general and SeleniumLibrary README.rst
    [https://github.com/robotframework/SeleniumLibrary#browser-drivers|Browser drivers chapter]
    for more details about WebDriver binary installation.

    %TOC%

    = Locating elements =

    All keywords in SeleniumLibrary that need to interact with an element
    on a web page take an argument typically named ``locator`` that specifies
    how to find the element. Most often the locator is given as a string
    using the locator syntax described below, but `using WebElements` is
    possible too.

    == Locator syntax ==

    SeleniumLibrary supports finding elements based on different strategies
    such as the element id, XPath expressions, or CSS selectors. The strategy
    can either be explicitly specified with a prefix or the strategy can be
    implicit.

    === Default locator strategy ===

    By default, locators are considered to use the keyword specific default
    locator strategy. All keywords support finding elements based on ``id``
    and ``name`` attributes, but some keywords support additional attributes
    or other values that make sense in their context. For example, `Click
    Link` supports the ``href`` attribute and the link text and addition
    to the normal ``id`` and ``name``.

    Examples:

    | `Click Element` | example | # Match based on ``id`` or ``name``.            |
    | `Click Link`    | example | # Match also based on link text and ``href``.   |
    | `Click Button`  | example | # Match based on ``id``, ``name`` or ``value``. |

    If a locator accidentally starts with a prefix recognized as `explicit
    locator strategy` or `implicit XPath strategy`, it is possible to use
    the explicit ``default`` prefix to enable the default strategy.

    Examples:

    | `Click Element` | name:foo         | # Find element with name ``foo``.               |
    | `Click Element` | default:name:foo | # Use default strategy with value ``name:foo``. |
    | `Click Element` | //foo            | # Find element using XPath ``//foo``.           |
    | `Click Element` | default: //foo   | # Use default strategy with value ``//foo``.    |

    === Explicit locator strategy ===

    The explicit locator strategy is specified with a prefix using either
    syntax ``strategy:value`` or ``strategy=value``. The former syntax
    is preferred because the latter is identical to Robot Framework's
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#named-argument-syntax|
    named argument syntax] and that can cause problems. Spaces around
    the separator are ignored, so ``id:foo``, ``id: foo`` and ``id : foo``
    are all equivalent.

    Locator strategies that are supported by default are listed in the table
    below. In addition to them, it is possible to register `custom locators`.

    | = Strategy = |          = Match based on =         |         = Example =            |
    | id           | Element ``id``.                     | ``id:example``                 |
    | name         | ``name`` attribute.                 | ``name:example``               |
    | identifier   | Either ``id`` or ``name``.          | ``identifier:example``         |
    | class        | Element ``class``.                  | ``class:example``              |
    | tag          | Tag name.                           | ``tag:div``                    |
    | xpath        | XPath expression.                   | ``xpath://div[@id="example"]`` |
    | css          | CSS selector.                       | ``css:div#example``            |
    | dom          | DOM expression.                     | ``dom:document.images[5]``     |
    | link         | Exact text a link has.              | ``link:The example``           |
    | partial link | Partial link text.                  | ``partial link:he ex``         |
    | sizzle       | Sizzle selector deprecated.         | ``sizzle:div.example``         |
    | jquery       | jQuery expression.                  | ``jquery:div.example``         |
    | default      | Keyword specific default behavior.  | ``default:example``            |

    See the `Default locator strategy` section below for more information
    about how the default strategy works. Using the explicit ``default``
    prefix is only necessary if the locator value itself accidentally
    matches some of the explicit strategies.

    Different locator strategies have different pros and cons. Using ids,
    either explicitly like ``id:foo`` or by using the `default locator
    strategy` simply like ``foo``, is recommended when possible, because
    the syntax is simple and locating elements by id is fast for browsers.
    If an element does not have an id or the id is not stable, other
    solutions need to be used. If an element has a unique tag name or class,
    using ``tag``, ``class`` or ``css`` strategy like ``tag:h1``,
    ``class:example`` or ``css:h1.example`` is often an easy solution. In
    more complex cases using XPath expressions is typically the best
    approach. They are very powerful but a downside is that they can also
    get complex.

    Examples:

    | `Click Element` | id:foo                      | # Element with id 'foo'. |
    | `Click Element` | css:div#foo h1              | # h1 element under div with id 'foo'. |
    | `Click Element` | xpath: //div[@id="foo"]//h1 | # Same as the above using XPath, not CSS. |
    | `Click Element` | xpath: //*[contains(text(), "example")] | # Element containing text 'example'. |

    *NOTE:*

    - The ``strategy:value`` syntax is only supported by SeleniumLibrary 3.0
      and newer.
    - Using the ``sizzle`` strategy or its alias ``jquery`` requires that
      the system under test contains the jQuery library.
    - Prior to SeleniumLibrary 3.0, table related keywords only supported
      ``xpath``, ``css`` and ``sizzle/jquery`` strategies.

    === Implicit XPath strategy ===

    If the locator starts with ``//`` or ``(//``, the locator is considered
    to be an XPath expression. In other words, using ``//div`` is equivalent
    to using explicit ``xpath://div``.

    Examples:

    | `Click Element` | //div[@id="foo"]//h1 |
    | `Click Element` | (//div)[2]           |

    The support for the ``(//`` prefix is new in SeleniumLibrary 3.0.

    == Using WebElements ==

    In addition to specifying a locator as a string, it is possible to use
    Selenium's WebElement objects. This requires first getting a WebElement,
    for example, by using the `Get WebElement` keyword.

    | ${elem} =       | `Get WebElement` | id:example |
    | `Click Element` | ${elem}          |            |

    == Custom locators ==

    If more complex lookups are required than what is provided through the
    default locators, custom lookup strategies can be created. Using custom
    locators is a two part process. First, create a keyword that returns
    a WebElement that should be acted on:

    | Custom Locator Strategy | [Arguments] | ${browser} | ${locator} | ${tag} | ${constraints} |
    |   | ${element}= | Execute Javascript | return window.document.getElementById('${locator}'); |
    |   | [Return] | ${element} |

    This keyword is a reimplementation of the basic functionality of the
    ``id`` locator where ``${browser}`` is a reference to a WebDriver
    instance and ``${locator}`` is the name of the locator strategy. To use
    this locator, it must first be registered by using the
    `Add Location Strategy` keyword:

    | `Add Location Strategy` | custom | Custom Locator Strategy |

    The first argument of `Add Location Strategy` specifies the name of
    the strategy and it must be unique. After registering the strategy,
    the usage is the same as with other locators:

    | `Click Element` | custom:example |

    See the `Add Location Strategy` keyword for more details.

    = Browser and Window =

    There is different conceptual meaning when SeleniumLibrary talks
    about windows or browsers. This chapter explains those differences.

    == Browser ==

    When `Open Browser` or `Create WebDriver` keyword is called, it
    will create a new Selenium WebDriver instance by using the
    [https://www.seleniumhq.org/docs/03_webdriver.jsp|Selenium WebDriver]
    API. In SeleniumLibrary terms, a new browser is created. It is
    possible to start multiple independent browsers (Selenium Webdriver
    instances) at the same time, by calling `Open Browser` or
    `Create WebDriver` multiple times. These browsers are usually
    independent of each other and do not share data like cookies,
    sessions or profiles. Typically when the browser starts, it
    creates a single window which is shown to the user.

    == Window ==

    Windows are the part of a browser that loads the web site and presents
    it to the user. All content of the site is the content of the window.
    Windows are children of a browser. In SeleniumLibrary browser is a
    synonym for WebDriver instance. One browser may have multiple
    windows. Windows can appear as tabs, as separate windows or pop-ups with
    different position and size. Windows belonging to the same browser
    typically share the sessions detail, like cookies. If there is a
    need to separate sessions detail, example login with two different
    users, two browsers (Selenium WebDriver instances) must be created.
    New windows can be opened example by the application under test or
    by example `Execute Javascript` keyword:

    | `Execute Javascript`    window.open()    # Opens a new window with location about:blank

    The example below opens multiple browsers and windows,
    to demonstrate how the different keywords can be used to interact
    with browsers, and windows attached to these browsers.

    Structure:
    | BrowserA
    |            Window 1  (location=https://robotframework.org/)
    |            Window 2  (location=https://robocon.io/)
    |            Window 3  (location=https://github.com/robotframework/)
    |
    | BrowserB
    |            Window 1  (location=https://github.com/)

    Example:
    | `Open Browser`       | https://robotframework.org         | ${BROWSER}       | alias=BrowserA   | # BrowserA with first window is opened.                                       |
    | `Execute Javascript` | window.open()                      |                  |                  | # In BrowserA second window is opened.                                        |
    | `Switch Window`      | locator=NEW                        |                  |                  | # Switched to second window in BrowserA                                       |
    | `Go To`              | https://robocon.io                 |                  |                  | # Second window navigates to robocon site.                                    |
    | `Execute Javascript` | window.open()                      |                  |                  | # In BrowserA third window is opened.                                         |
    | ${handle}            | `Switch Window`                    | locator=NEW      |                  | # Switched to third window in BrowserA                                        |
    | `Go To`              | https://github.com/robotframework/ |                  |                  | # Third windows goes to robot framework github site.                          |
    | `Open Browser`       | https://github.com                 | ${BROWSER}       | alias=BrowserB   | # BrowserB with first windows is opened.                                      |
    | ${location}          | `Get Location`                     |                  |                  | # ${location} is: https://www.github.com                                      |
    | `Switch Window`      | ${handle}                          | browser=BrowserA |                  | # BrowserA second windows is selected.                                        |
    | ${location}          | `Get Location`                     |                  |                  | # ${location} = https://robocon.io/                                           |
    | @{locations 1}       | `Get Locations`                    |                  |                  | # By default, lists locations under the currectly active browser (BrowserA).   |
    | @{locations 2}       | `Get Locations`                    |  browser=ALL     |                  | # By using browser=ALL argument keyword list all locations from all browsers. |

    The above example, @{locations 1} contains the following items:
    https://robotframework.org/, https://robocon.io/ and
    https://github.com/robotframework/'. The @{locations 2}
    contains the following items: https://robotframework.org/,
    https://robocon.io/, https://github.com/robotframework/'
    and 'https://github.com/.

    = Timeouts, waits, and delays =

    This section discusses different ways how to wait for elements to
    appear on web pages and to slow down execution speed otherwise.
    It also explains the `time format` that can be used when setting various
    timeouts, waits, and delays.

    == Timeout ==

    SeleniumLibrary contains various keywords that have an optional
    ``timeout`` argument that specifies how long these keywords should
    wait for certain events or actions. These keywords include, for example,
    ``Wait ...`` keywords and keywords related to alerts. Additionally
    `Execute Async Javascript`. Although it does not have ``timeout``,
    argument, uses a timeout to define how long asynchronous JavaScript
    can run.

    The default timeout these keywords use can be set globally either by
    using the `Set Selenium Timeout` keyword or with the ``timeout`` argument
    when `importing` the library. See `time format` below for supported
    timeout syntax.

    == Implicit wait ==

    Implicit wait specifies the maximum time how long Selenium waits when
    searching for elements. It can be set by using the `Set Selenium Implicit
    Wait` keyword or with the ``implicit_wait`` argument when `importing`
    the library. See [https://www.seleniumhq.org/docs/04_webdriver_advanced.jsp|
    Selenium documentation] for more information about this functionality.

    See `time format` below for supported syntax.

    == Selenium speed ==

    Selenium execution speed can be slowed down globally by using `Set
    Selenium speed` keyword. This functionality is designed to be used for
    demonstrating or debugging purposes. Using it to make sure that elements
    appear on a page is not a good idea. The above-explained timeouts
    and waits should be used instead.

    See `time format` below for supported syntax.

    == Time format ==

    All timeouts and waits can be given as numbers considered seconds
    (e.g. ``0.5`` or ``42``) or in Robot Framework's time syntax
    (e.g. ``1.5 seconds`` or ``1 min 30 s``). For more information about
    the time syntax see the
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#time-format|Robot Framework User Guide].

    = Run-on-failure functionality =

    SeleniumLibrary has a handy feature that it can automatically execute
    a keyword if any of its own keywords fails. By default, it uses the
    `Capture Page Screenshot` keyword, but this can be changed either by
    using the `Register Keyword To Run On Failure` keyword or with the
    ``run_on_failure`` argument when `importing` the library. It is
    possible to use any keyword from any imported library or resource file.

    The run-on-failure functionality can be disabled by using a special value
    ``NOTHING`` or anything considered false (see `Boolean arguments`)
    such as ``NONE``.

    = Boolean arguments =

    Some keywords accept arguments that are handled as Boolean values true or
    false. If such an argument is given as a string, it is considered false if
    it is either empty or case-insensitively equal to ``false``, ``no``, ``off``,
     ``0`` or ``none``. Other strings are considered true regardless of their value and
    other argument types are tested using the same
    [https://docs.python.org/3/library/stdtypes.html#truth-value-testing|rules as in Python].

    True examples:

    | `Set Screenshot Directory` | ${RESULTS} | persist=True    | # Strings are generally true.    |
    | `Set Screenshot Directory` | ${RESULTS} | persist=yes     | # Same as the above.             |
    | `Set Screenshot Directory` | ${RESULTS} | persist=${TRUE} | # Python True is true.           |
    | `Set Screenshot Directory` | ${RESULTS} | persist=${42}   | # Numbers other than 0 are true. |

    False examples:

    | `Set Screenshot Directory` | ${RESULTS} | persist=False    | # String false is false.        |
    | `Set Screenshot Directory` | ${RESULTS} | persist=no       | # Also string no is false.      |
    | `Set Screenshot Directory` | ${RESULTS} | persist=NONE     | # String NONE is false.         |
    | `Set Screenshot Directory` | ${RESULTS} | persist=${EMPTY} | # Empty string is false.        |
    | `Set Screenshot Directory` | ${RESULTS} | persist=${FALSE} | # Python False is false.        |
    | `Set Screenshot Directory` | ${RESULTS} | persist=${NONE}  | # Python None is false.         |

    Note that prior to SeleniumLibrary 3.0, all non-empty strings, including
    ``false``, ``no`` and ``none``, were considered true. Starting from
    SeleniumLibrary 4.0, strings ``0`` and ``off`` are considered as false.

    = EventFiringWebDriver =

    The SeleniumLibrary offers support for
    [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html#module-selenium.webdriver.support.event_firing_webdriver|EventFiringWebDriver].
    See the Selenium and SeleniumLibrary
    [https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending.rst#EventFiringWebDriver|EventFiringWebDriver support]
    documentation for further details.

    EventFiringWebDriver is new in SeleniumLibrary 4.0

    = Thread support =

    SeleniumLibrary is not thread-safe. This is mainly due because the underlying
    [https://github.com/SeleniumHQ/selenium/wiki/Frequently-Asked-Questions#q-is-webdriver-thread-safe|
    Selenium tool is not thread-safe] within one browser/driver instance.
    Because of the limitation in the Selenium side, the keywords or the
    API provided by the SeleniumLibrary is not thread-safe.

    = Plugins =

    SeleniumLibrary offers plugins as a way to modify and add library keywords and modify some of the internal
    functionality without creating a new library or hacking the source code. See
    [https://github.com/robotframework/SeleniumLibrary/blob/master/docs/extending/extending.rst#Plugins|plugin API]
    documentation for further details.

    Plugin API is new SeleniumLibrary 4.0
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None, plugins=None,
                 event_firing_webdriver=None):
        """SeleniumLibrary can be imported with several optional arguments.

        - ``timeout``:
          Default value for `timeouts` used with ``Wait ...`` keywords.
        - ``implicit_wait``:
          Default value for `implicit wait` used when locating elements.
        - ``run_on_failure``:
          Default action for the `run-on-failure functionality`.
        - ``screenshot_root_directory``:
          Path to folder where possible screenshots are created or EMBED.
          See `Set Screenshot Directory` keyword for further details about EMBED.
          If not given, the directory where the log file is written is used.
        - ``plugins``:
          Allows extending the SeleniumLibrary with external Python classes.
        - ``event_firing_webdriver``:
          Class for wrapping Selenium with
          [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html#module-selenium.webdriver.support.event_firing_webdriver|EventFiringWebDriver]
        """
        self.timeout = timestr_to_secs(timeout)
        self.implicit_wait = timestr_to_secs(implicit_wait)
        self.speed = 0.0
        self.run_on_failure_keyword = RunOnFailureKeywords.resolve_keyword(run_on_failure)
        self._running_on_failure_keyword = False
        self.screenshot_root_directory = screenshot_root_directory
        self._resolve_screenshot_root_directory()
        self._element_finder = ElementFinder(self)
        self._plugin_keywords = []
        libraries = [
            AlertKeywords(self),
            BrowserManagementKeywords(self),
            CookieKeywords(self),
            ElementKeywords(self),
            FormElementKeywords(self),
            FrameKeywords(self),
            JavaScriptKeywords(self),
            RunOnFailureKeywords(self),
            ScreenshotKeywords(self),
            SelectElementKeywords(self),
            TableElementKeywords(self),
            WaitingKeywords(self),
            WindowKeywords(self)
        ]
        self.ROBOT_LIBRARY_LISTENER = LibraryListener()
        self._running_keyword = None
        self.event_firing_webdriver = None
        if is_truthy(event_firing_webdriver):
            self.event_firing_webdriver = self._parse_listener(event_firing_webdriver)
        self._plugins = []
        if is_truthy(plugins):
            plugin_libs = self._parse_plugins(plugins)
            self._plugins = plugin_libs
            libraries = libraries + plugin_libs
        self._drivers = WebDriverCache()
        DynamicCore.__init__(self, libraries)

    def run_keyword(self, name, args, kwargs):
        self._running_keyword = name
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except Exception:
            self.failure_occurred()
            raise
        finally:
            self._running_keyword = None

    def get_keyword_tags(self, name):
        tags = list(DynamicCore.get_keyword_tags(self, name))
        if name in self._plugin_keywords:
            tags.append('plugin')
        return tags

    def get_keyword_documentation(self, name):
        if name == '__intro__':
            return self._get_intro_documentation()
        return DynamicCore.get_keyword_documentation(self, name)

    def _parse_plugin_doc(self):
        Doc = namedtuple('Doc', 'doc, name')
        for plugin in self._plugins:
            yield Doc(doc=getdoc(plugin) or 'No plugin documentation found.',
                      name=plugin.__class__.__name__)

    def _get_intro_documentation(self):
        intro = DynamicCore.get_keyword_documentation(self, '__intro__')
        for plugin_doc in self._parse_plugin_doc():
            intro += '\n\n'
            intro = intro + '= Plugin: %s =' % plugin_doc.name + '\n\n'
            intro = intro + plugin_doc.doc
        return self._create_toc(intro)

    def _create_toc(self, intro):
        toc = ['== Table of contents ==', '']
        all_match = re.findall(r'(^\=\s)(.+)(\s\=$)', intro, re.MULTILINE)
        for match in all_match:
            toc.append('- `%s`' % match[1])
        toc.extend(['- `Importing`', '- `Shortcuts`', '- `Keywords`'])
        return intro.replace('%TOC%', '\n'.join(toc))

    def register_driver(self, driver, alias):
        """Add's a `driver` to the library WebDriverCache.

        :param driver: Instance of the Selenium `WebDriver`.
        :type driver: selenium.webdriver.remote.webdriver.WebDriver
        :param alias: Alias given for this `WebDriver` instance.
        :type alias: str
        :return: The index of the `WebDriver` instance.
        :rtype: int
        """
        return self._drivers.register(driver, alias)

    def failure_occurred(self):
        """Method that is executed when a SeleniumLibrary keyword fails.

        By default, executes the registered run-on-failure keyword.
        Libraries extending SeleniumLibrary can overwrite this hook
        method if they want to provide custom functionality instead.
        """
        if self._running_on_failure_keyword or not self.run_on_failure_keyword:
            return
        try:
            self._running_on_failure_keyword = True
            BuiltIn().run_keyword(self.run_on_failure_keyword)
        except Exception as err:
            logger.warn("Keyword '%s' could not be run on failure: %s"
                        % (self.run_on_failure_keyword, err))
        finally:
            self._running_on_failure_keyword = False

    @property
    def driver(self):
        """Current active driver.

        :rtype: selenium.webdriver.remote.webdriver.WebDriver
        :raises SeleniumLibrary.errors.NoOpenBrowser: If browser is not open.
        """
        if not self._drivers.current:
            raise NoOpenBrowser('No browser is open.')
        return self._drivers.current

    def find_element(self, locator, parent=None):
        """Find element matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :type locator: str or selenium.webdriver.remote.webelement.WebElement
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default, search starts from the root using `WebDriver`.
        :type parent: selenium.webdriver.remote.webelement.WebElement
        :return: Found `WebElement`.
        :rtype: selenium.webdriver.remote.webelement.WebElement
        :raises SeleniumLibrary.errors.ElementNotFound: If element not found.
        """
        return self._element_finder.find(locator, parent=parent)

    def find_elements(self, locator, parent=None):
        """Find all elements matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :type locator: str or selenium.webdriver.remote.webelement.WebElement
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default, search starts from the root using `WebDriver`.
        :type parent: selenium.webdriver.remote.webelement.WebElement
        :return: list of found `WebElement` or e,mpty if elements are not found.
        :rtype: list[selenium.webdriver.remote.webelement.WebElement]
        """
        return self._element_finder.find(locator, first_only=False,
                                         required=False, parent=parent)

    def _parse_plugins(self, plugins):
        libraries = []
        importer = Importer('test library')
        for parsed_plugin in self._string_to_modules(plugins):
            plugin = importer.import_class_or_module(parsed_plugin.module)
            if not isclass(plugin):
                message = "Importing test library: '%s' failed." % parsed_plugin.module
                raise DataError(message)
            plugin = plugin(self, *parsed_plugin.args,
                            **parsed_plugin.kw_args)
            if not isinstance(plugin, LibraryComponent):
                message = 'Plugin does not inherit SeleniumLibrary.base.LibraryComponent'
                raise PluginError(message)
            self._store_plugin_keywords(plugin)
            libraries.append(plugin)
        return libraries

    def _parse_listener(self, event_firing_webdriver):
        listener_module = self._string_to_modules(event_firing_webdriver)
        listener_count = len(listener_module )
        if listener_count > 1:
            message = 'Is is possible import only one listener but there was %s listeners.' % listener_count
            raise ValueError(message)
        listener_module = listener_module[0]
        importer = Importer('test library')
        listener = importer.import_class_or_module(listener_module.module)
        if not isclass(listener):
            message = "Importing test Selenium lister class '%s' failed." % listener_module.module
            raise DataError(message)
        return listener

    def _string_to_modules(self, modules):
        Module = namedtuple('Module', 'module, args, kw_args')
        parsed_modules = []
        for module in modules.split(','):
            module = module.strip()
            module_and_args = module.split(';')
            module_name = module_and_args.pop(0)
            kw_args = {}
            args = []
            for argument in module_and_args:
                if '=' in argument:
                    key, value = argument.split('=')
                    kw_args[key] = value
                else:
                    args.append(argument)
            module = Module(module=module_name, args=args, kw_args=kw_args)
            parsed_modules.append(module)
        return parsed_modules

    def _store_plugin_keywords(self, plugin):
        dynamic_core = DynamicCore([plugin])
        self._plugin_keywords.extend(dynamic_core.get_keyword_names())

    def _resolve_screenshot_root_directory(self):
        screenshot_root_directory = self.screenshot_root_directory
        if is_string(screenshot_root_directory):
            if screenshot_root_directory.upper() == EMBED:
                self.screenshot_root_directory = EMBED
