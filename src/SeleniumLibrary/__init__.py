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

from collections import namedtuple
from inspect import isclass

from robot.api import logger
from robot.errors import DataError
from robot.libraries.BuiltIn import BuiltIn
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
from SeleniumLibrary.locators import ElementFinder
from SeleniumLibrary.utils import LibraryListener, timestr_to_secs, is_truthy


__version__ = '4.0.0.dev1'


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

    == Table of contents ==

    - `Locating elements`
    - `Timeouts, waits and delays`
    - `Run-on-failure functionality`
    - `Boolean arguments`
    - `Plugins`
    - `EventFiringWebDriver`
    - `Thread support`
    - `Importing`
    - `Shortcuts`
    - `Keywords`

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

    By default locators are considered to use the keyword specific default
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
    is preferred, because the latter is identical to Robot Framework's
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
    the syntax is simple and locating elements by an id is fast for browsers.
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
    instance and ``${locator}`` is name of the locator strategy. To use
    this locator it must first be registered by using the
    `Add Location Strategy` keyword:

    | `Add Location Strategy` | custom | Custom Locator Strategy |

    The first argument of `Add Location Strategy` specifies the name of
    the strategy and it must be unique. After registering the strategy,
    the usage is the same as with other locators:

    | `Click Element` | custom:example |

    See the `Add Location Strategy` keyword for more details.

    = Timeouts, waits and delays =

    This section discusses different ways how to wait for elements to
    appear on web pages and to slow down execution speed otherwise.
    It also explains the `time format` that can be used when setting various
    timeouts, waits and delays.

    == Timeout ==

    SeleniumLibrary contains various keywords that have an optional
    ``timeout`` argument that specifies how long these keywords should
    wait for certain events or actions. These keywords include, for example,
    ``Wait ...`` keywords and keywords related to alerts. Additionally
    `Execute Async Javascript`. although it does not have ``timeout``,
    argument, uses timeout to define how long asynchronous JavaScript
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
    appear on a page is not a good idea, and the above explained timeouts
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
    a keyword if any of its own keywords fails. By default it uses the
    `Capture Page Screenshot` keyword, but this can be changed either by
    using the `Register Keyword To Run On Failure` keyword or with the
    ``run_on_failure`` argument when `importing` the library. It is
    possible to use any keyword from any imported library or resource file.

    The run-on-failure functionality can be disabled by using a special
    value ``NOTHING`` or anything considered false (see `Boolean arguments`)
    such as ``NONE``.

    = Boolean arguments =

    Some keywords accept arguments that are handled as Boolean values true or
    false. If such an argument is given as a string, it is considered false if
    it is either empty or case-insensitively equal to ``false``, ``no``, ``off``,
     ``0`` or ``none``. Other strings are considered true regardless their value, and
    other argument types are tested using same
    [https://docs.python.org/2/library/stdtypes.html#truth-value-testing|rules as in Python].

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

    = Plugins =

    SeleniumLibrary offers plugins as a way to modify, add library keywords and modify some of the internal
    functionality without creating new library or hacking the source code. Plugins can be only loaded in the
    library import, with the `plugins` argument and SeleniumLibrary does not offer way to unload the
    plugins from the SeleniumLibrary.

    Plugins is new SeleniumLibrary 4.0

    == Importing plugins ==

    Importing plugins is similar when importing Robot Framework
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#importing-libraries|libraries]. It
    is possible import plugin with using
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#using-physical-path-to-library|physical path]
    or with
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#using-library-name|plugin name],
    exactly in same way as importing libraries in Robot Framework. SeleniumLibrary plugins are searched from the
    same
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#module-search-path|module search path]
    as Robot Framework searches libraries. It is only possible to import plugins written in Python, other programming
    languages or Robot Framework test data is not supported. Like with Robot Framework library imports, plugin
    names are case sensitive and spaces are not supported in the plugin name. It is possible to import multiple plugins
    at the same time by separating plugins with comma. It is possible to have space before and after the comma. Plugins
    are imported in the order they defined in the `plugins` argument. If two or more plugins declare the same keyword
    or modify the same method/attribute in the SeleniumLibrary, the last plugin to perform the changes will overwrite
    the changes made by other plugins.

    | Library | SeleniumLibrary | plugins=${CURDIR}/MyPlugin.py                   | # Imports plugin with physical path |
    | Library | SeleniumLibrary | plugins=plugins.MyPlugin, plugins.MyOtherPlugin | # Import two plugins with name      |

    Generally speaking, plugin are not any different from the classes that are used to implement keyword in the
    SeleniumLibrary. Example like with
    [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/keywords/browsermanagement.py|BrowserManagementKeywords]
    class inherits the
    [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/base/librarycomponent.py|LibraryComponent]
    and uses ``@keyword`` decorator to mark which methods are exposed as keywords.

    == Plugin arguments ==
    When SeleniumLibrary creates instances from the plugin classes, it will by default initiate the class with a single
    argument, called ``ctx`` (context). ``ctx`` is the instance of the SeleniummLibrary and it provides access to the
    common methods and attributes used across in the SeleniumLibrary classes. But is recommended to use
    wrappers provided by the `LibraryComponent`.

    It is also possible to provide optional arguments to the plugins. Arguments must be separated with a semicolon
    from the plugin. SeleniumLibrary will not convert arguments and plugin is responsible for converting the argument
    to proper types.

    | Library | SeleniumLibrary | plugins=plugins.Plugin;ArgOne;ArgTwo | # Import two plugins with two arguments: ArgOne and ArgTwo |

    It is possible to provide variable number of arguments and keywords arguments. Named arguments must be defined
    first, variable number of arguments as second and keywords arguments as last. All arguments must be separated
    with semicolon. Example if plugin __init__ is defined like this:
    | class Plugin(LibraryComponent):
    |
    |     def __init__(self, ctx, arg, *varargs, **kwargs):
    Then, for example, it is possible to plugin with these arguments:
    | Library | SeleniumLibrary | plugins=plugins.Plugin;argument1;varg1;varg2;kw1=kwarg1;kw2=kwarg2 |
    Then the ``argument1`` is given the ``arg`` in the ``__init__``. The ``varg1`` and ``varg2`` variable number
    arguments are given to the ``*varargs`` argument in the  ``__init__``. Finally, the ``kw1=kwarg1`` and
    ``kw2=kwarg2`` keyword arguments are given to the ``**kwargs`` in the  ``__init__``. As in Python, there can be
    zero or more variable number and keyword arguments.

    == Plugin API ==

    Plugins must be implemented as Python classes and plugins must inherit the SeleniumLibrary
    [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/base/librarycomponent.py|LibraryComponent]
    class. Plugin __init__ must support at least one argument: ``ctx``. Also optional arguments are supported, see
    `Plugin arguments` for more details how to provide optional arguments to plugins.

    SeleniumLibrary uses Robot Framework
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#dynamic-library-api|dynamic library API].
    The main difference, when compared to libraries using dynamic library API, is that plugins are not responsible
    for implementing the dynamic library API. SeleniumLibrary is handling the dynamic library API requirements
    towards Robot Framework. For plugins this means that methods that implements keywords, must be decorated
    with ``@keyword`` decorator. The ``@keyword`` decorator can be imported from Robot Framework and used in the
    following way:
    | from robot.api.deco import keyword
    |
    | class Plugin(LibraryComponent):
    |
    |     @keyword
    |     def keyword(self):
    |         # Code here to implement a keyword.

    == Handling failures ==
    SeleniumLibrary does not suppress exception raised during plugin import or during keywords discovery from the
    plugins. In this case the whole SeleniumLibrary import will fail and SeleniumLibrary keywords can not be used
    from that import.

    ==  LibraryComponent ==
    Although ``ctx`` provides access to the common methods and attributes used in the SeleniumLibrary, the
    [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/base/librarycomponent.py|LibraryComponent]
    provides more, an easier and IDE friendly access to the common methods and attributes, Example currently
    active browser can be found from ``self.ctx.driver``, the ``LibraryComponent`` exposes the browser as:
    ``self.driver``. Plugin classes must inherit the ``LibraryComponent``.

    The following methods are available from the ``LibraryComponent`` class:

    |        = Method =        |                                                                  = Description =                                                                  |
    | find_element             | Finds first element matching ``locator``.                                                                                                         |
    | find_elements            | Find all elements matching ``locator``.                                                                                                           |
    | is_text_present          | Returns True if text is present in the page.                                                                                                      |
    | is_element_enabled       | Returns True if element is enabled.                                                                                                               |
    | is_visible               | Returns True if element is visible.                                                                                                               |
    | log_source               | Calls method defining the `Log Source` keyword.                                                                                                   |
    | assert_page_contains     | Raises AssertionError if element is not found from the page.                                                                                      |
    | assert_page_not_contains | Raises AssertionError if element is found from the page.                                                                                          |
    | get_timeout              | By default returns SeleniumLibrary ``timeout`` argument value. With argument converts string with Robot Framework ``timestr_to_secs`` to seconds. |
    | info                     | Wrapper to ``robot.api.logger.info`` method.                                                                                                      |
    | debug                    | Wrapper to ``robot.api.logger.debug`` method.                                                                                                     |
    | warn                     | Wrapper to ``robot.api.logger.warn`` method.                                                                                                      |
    | log                      | Wrapper to ``robot.api.logger.write`` method.                                                                                                     |

    The following attributes are available from the ``LibraryComponent`` class:

    | = Attribute =  |                                                                          = Description =                                                                           |
    | driver         | Currently active browser/WebDriver instance in the SeleniumLibrary.                                                                                                |
    | drivers        | [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/keywords/webdrivertools.py|Cache] for the opened browsers/WebDriver instances.  |
    | element_finder | Read/write attribute for the [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/locators/elementfinder.py|ElementFinder] instance. |
    | ctx            | Instance of the SeleniumLibrary.                                                                                                                                   |
    | log_dir        | Folder where output files are written.                                                                                                                             |

    See the
    [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/__init__.py|SeleniumLibrary init],
    the
    [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/base/librarycomponent.py|LibraryComponent]
    and the
    [https://github.com/robotframework/SeleniumLibrary/blob/master/src/SeleniumLibrary/base/context.py|ContextAware]
    classes for further implementation details.

    == Generating keyword documentation ==
    To separate keywords which are added or modified by plugins, SeleniumLibrary will add ``plugin``
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#keyword-tags|keyword tag]
    to all keywords added or modified from plugins. When SeleniumLibrary keyword documentation, with plugins,
    is generated by
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#library-documentation-tool-libdoc|libdoc]
    it is easy to separate keywords which are added or modified by plugins. Keyword documentation can be example
    generated by following command:

    | python -m robot.libdoc SeleniumLibrary::plugins=/path/to/Plugin.py ./SeleniumLibraryWithPlugin.html

    = EventFiringWebDriver =

    The Selenium
    [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html#module-selenium.webdriver.support.event_firing_webdriver|EventFiringWebDriver]
    offers listener API for firing events before and after certain Selenium API calls.
    SeleniumLibrary offers support for Selenium ``EventFiringWebDriver`` listener class, by providing possibility
    to import the listener class with ``event_firing_webdriver`` argument. Refer to the Selenium
    ``EventFiringWebDriver`` documentation which Selenium API methods which can fire events and how the Selenium
    listener class should be implemented.

    EventFiringWebDriver is new in SeleniumLibrary 4.0

    == Importing listener class ==

    Importing Selenium listener class is similar when importing Robot Framework
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#importing-libraries|libraries]. It
    is possible import Selenium listener class with using
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#using-physical-path-to-library|physical path]
    or with
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#using-library-name|listener name],
    exactly in same way as importing libraries in Robot Framework. Selenium listener class is searched from the same
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#module-search-path|module search path]
    as Robot Framework searches libraries. It is only possible to import listener class written in Python, other
    programming languages or Robot Framework test data is not supported. Like with Robot Framework library imports,
    Selenium listener class name is case sensitive and spaces are not supported in the class name. It is only
    possible to import one Selenium listener class and it is not possible to provide arguments for the Selenium
    listener class.

    | Library | SeleniumLibrary | event_firing_webdriver=listner.SeleniumListener | # Improts listener with name.         |
    | Library | SeleniumLibrary | event_firing_webdriver=${CURDIR}/MyListener.py  | # Imports listner with physical path. |

    = Thread support =

    SeleniumLibrary is not thread safe. This is mainly due because the underlying
    [https://github.com/SeleniumHQ/selenium/wiki/Frequently-Asked-Questions#q-is-webdriver-thread-safe|
    Selenium tool is not thread safe] within one browser/driver instance.
    Because of the limitation in the Selenium side, the keywords or the
    API provided by the SeleniumLibrary is not thread safe.
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
          Location where possible screenshots are created. If not given,
          the directory where the log file is written is used.
        - ``plugins``:
          Allows extending the SeleniumLibrary with external Python classes.
        - ``event_firing_webdriver``:
          Class for wrapping Selenium with
          [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.event_firing_webdriver.html#module-selenium.webdriver.support.event_firing_webdriver|EventFiringWebDriver]
        """
        self.timeout = timestr_to_secs(timeout)
        self.implicit_wait = timestr_to_secs(implicit_wait)
        self.speed = 0.0
        self.run_on_failure_keyword \
            = RunOnFailureKeywords.resolve_keyword(run_on_failure)
        self._running_on_failure_keyword = False
        self.screenshot_root_directory = screenshot_root_directory
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
        if is_truthy(plugins):
            plugin_libs = self._parse_plugins(plugins)
            libraries = libraries + plugin_libs
        self._drivers = WebDriverCache()
        DynamicCore.__init__(self, libraries)
        self.ROBOT_LIBRARY_LISTENER = LibraryListener()
        if is_truthy(event_firing_webdriver):
            self.event_firing_webdriver = self._parse_listener(event_firing_webdriver)
        else:
            self.event_firing_webdriver = None

    def run_keyword(self, name, args, kwargs):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except Exception:
            self.failure_occurred()
            raise

    def get_keyword_tags(self, name):
        tags = list(DynamicCore.get_keyword_tags(self, name))
        if name in self._plugin_keywords:
            tags.append('plugin')
        return tags

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

        By default executes the registered run-on-failure keyword.
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
            from. By default search starts from the root using `WebDriver`.
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
            from. By default search starts from the root using `WebDriver`.
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
