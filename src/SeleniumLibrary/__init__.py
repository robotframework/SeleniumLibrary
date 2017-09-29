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

import warnings

from robot.api import logger
from robot.libraries.BuiltIn import BuiltIn

from SeleniumLibrary.base import DynamicCore
from SeleniumLibrary.keywords import (AlertKeywords,
                                      BrowserManagementKeywords,
                                      CookieKeywords,
                                      ElementKeywords,
                                      FormElementKeywords,
                                      JavaScriptKeywords,
                                      RunOnFailureKeywords,
                                      ScreenshotKeywords,
                                      SelectElementKeywords,
                                      TableElementKeywords,
                                      WaitingKeywords)
from SeleniumLibrary.locators import ElementFinder, TableElementFinder
from SeleniumLibrary.utils import (BrowserCache, Deprecated, LibraryListener,
                                   timestr_to_secs)


__version__ = '3.0.0b4.dev1'


class SeleniumLibrary(DynamicCore):
    """SeleniumLibrary is a web testing library for Robot Framework.

    This document explains how to use keywords provided by SeleniumLibrary.
    For information about installation, support, and more, please visit the
    [https://github.com/robotframework/SeleniumLibrary|project pages].
    For more information about Robot Framework, see http://robotframework.org.

    SeleniumLibrary uses the Selenium WebDriver modules internally to
    control a web browser. See http://seleniumhq.org for more information
    about Selenium in general.

    == Table of contents ==

    - `Locating elements`
    - `Timeouts, waits and delays`
    - `Run-on-failure functionality`
    - `Boolean arguments`
    - `Importing`
    - `Shortcuts`
    - `Keywords`

    = Locating elements =

    All keywords in SeleniumLibrary that need to interact with an element
    on a web page take an argument named ``locator`` that specifies how
    to find the element. Most often the locator is given as a string using
    the locator syntax described below, but `using WebElements` is possible
    too.

    == Locator syntax ==

    SeleniumLibrary supports finding elements based on different strategies
    such as the element id, XPath expressions, or CSS selectors. The strategy
    can either be explicitly specified with a prefix or the strategy can be
    implicit.

    === Explicit locator strategy ===

    The explicit locator strategy is specified with a prefix using either
    syntax ``strategy:value`` or ``strategy=value``. The former syntax
    is preferred, because the latter is identical to Robot Framework's
    [http://robotframework.org/robotframework/latest/RobotFrameworkUserGuide.html#named-argument-syntax|
    named argument syntax] and that can cause problems. Notice that the
    ``strategy:value`` syntax is olny supported by SeleniumLibrary 3.0 and
    newer, though.

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
    | sizzle       | Sizzle selector provided by jQuery. | ``sizzle:div.example``         |
    | jquery       | Same as the above.                  | ``jquery:div.example``         |
    | default      | Keyword specific default behavior.  | ``default:example``            |

    See the `Default locator strategy` section below for more information
    about how the default strategy works. Using the explicit ``default``
    prefix is only necessary if the locator value itself accidentally
    matches some of the explicit strategies.

    Spaces around the separator are ignored, so ``id : foo``, ``id: foo``
    and ``id:foo`` are all equivalent.

    Examples:

    | `Click Element` | id:container                      |
    | `Click Element` | css:div#container h1              |
    | `Click Element` | xpath: //div[@id="container"]//h1 |

    Notice that using the ``sizzle`` strategy or its alias ``jquery``
    requires that the system under test contains the jQuery library.

    === Implicit XPath strategy ===

    If the locator starts with ``//`` or ``(//``, the locator is considered
    to be an XPath expression. In other words, using ``//div`` is equivalent
    to using explicit ``xpath://div``.

    Examples:

    | `Click Element` | //div[@id="container"] |
    | `Click Element` | (//div)[2]             |

    The support for the ``(//`` prefix is new in SeleniumLibrary 3.0.

    === Default locator strategy ===

    By default locators are considered to use the keyword specific default
    locator strategy. All keywords support finding elements based on ``id``
    and ``name`` attributes, but some keywords support additional _key
    attributes_ that make sense in their context. For example, `Click Link`
    supports the link text and the ``href`` attribute in addition to the
    normal ``id`` and ``name``.

    Examples:

    | `Click Element` | example | # Match based on ``id`` or ``name``.            |
    | `Click Link`    | example | # Match also based on link text and ``href``.   |
    | `Click Button`  | example | # Match based on ``id``, ``name`` or ``value``. |

    If the locator accidentally starts with some of the explicit locator
    prefixes or with the implicit XPath prefixes, it is possible to use
    the explicit ``default`` prefix to enable the default strategy.

    Examples:

    | `Click Element` | name:foo         | # Find element with name ``foo``.               |
    | `Click Element` | default:name:foo | # Use default strategy with value ``name:foo``. |
    | `Click Element` | //foo            | # Find element using XPath ``//foo``.           |
    | `Click Element` | default://foo    | # Use default strategy with value ``//foo``.    |

    == Using WebElements ==

    In addition to specifying a locator as a string, it is possible to use
    Selenium's WebElement objects. This requires first getting a WebElement,
    for example, by using the `Get WebElement` keyword.

    | ${elem} =       | `Get WebElement` | id=example |
    | `Click Element` | ${elem}          |            |

    == Custom locators ==

    If more complex lookups are required than what is provided through the
    default locators, custom lookup strategies can be created. Using custom
    locators is a two part process. First, create a keyword that returns
    a WebElement that should be acted on:

    | Custom Locator Strategy | [Arguments] | ${browser} | ${strategy} | ${tag} | ${constraints} |
    |   | ${element}= | Execute Javascript | return window.document.getElementById('${criteria}'); |
    |   | [Return] | ${element} |

    This keyword is a reimplementation of the basic functionality of the
    ``id`` locator where ``${browser}`` is a reference to a WebDriver
    instance and ``${strategy}`` is name of the locator strategy. To use
    this locator it must first be registered by using the
    `Add Location Strategy` keyword:

    | `Add Location Strategy` | custom | Custom Locator Strategy |

    The first argument of `Add Location Strategy` specifies the name of
    the strategy and it must be unique. After registering the strategy,
    the usage is the same as with other locators:

    | `Click Element` | custom:example |

    See the `Add Location Strategy` keyword for more details.

    == Locating tables ==

    Starting from release 3.0.0, it is possible to locate table using all
    strategies supported by the library. Prior the release 3.0 tables
    could have been located with limited set of strategies and with
    limitations in the strategy.

    = Timeouts, waits and delays =

    This section discusses different ways how to wait for elements to
    appear on web pages and to slow down execution speed otherwise.
    It also explains the `time format` that can be used when setting various
    timeouts, waits and delays.

    == Timeouts ==

    SeleniumLibrary contains various ``Wait ...`` keywords that can be used
    to wait, for example, for a dynamically created elements to appear on
    a page. All these keywords accept an optional ``timeout`` argument that
    tells the maximum time to wait.

    The default timeout these keywords use can be set globally either by
    using the `Set Selenium Timeout` keyword or with the ``timeout`` argument
    when `importing` the library. The same timeout also applies to the
    `Execute Async Javascript` keyword.

    == Implicit wait ==

    Implicit wait specifies the maximum time how long Selenium waits when
    searching for elements. It can be set by using the `Set Selenium Implicit
    Wait` keyword or with the ``implicit_wait`` argument when `importing`
    the library. See [http://seleniumhq.org/docs/04_webdriver_advanced.html|
    Selenium documentation] for more information about this functionality.

    == Selenium speed ==

    Selenium execution speed can be slowed down globally by using `Set
    Selenium speed` keyword. This functionality is designed to be used for
    demonstrating or debugging purposes. Using it to make sure that elements
    appear on a page is not a good idea, and the above explained timeouts
    and waits should be used instead.

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
    it is either empty or case-insensitively equal to ``false``, ``no`` or
    ``none``. Other strings are considered true regardless their value, and
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
    ``false``, ``no`` and ``none``, were considered true.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = __version__

    def __init__(self, timeout=5.0, implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None):

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
        """
        self.timeout = timestr_to_secs(timeout)
        self.implicit_wait = timestr_to_secs(implicit_wait)
        self.speed = 0.0
        self.run_on_failure_keyword \
            = RunOnFailureKeywords.resolve_keyword(run_on_failure)
        self._running_on_failure_keyword = False
        self.screenshot_root_directory = screenshot_root_directory
        libraries = [
            AlertKeywords(self),
            BrowserManagementKeywords(self),
            RunOnFailureKeywords(self),
            ElementKeywords(self),
            TableElementKeywords(self),
            FormElementKeywords(self),
            SelectElementKeywords(self),
            JavaScriptKeywords(self),
            CookieKeywords(self),
            ScreenshotKeywords(self),
            WaitingKeywords(self)
        ]
        self._browsers = BrowserCache()
        DynamicCore.__init__(self, libraries)
        self.ROBOT_LIBRARY_LISTENER = LibraryListener()
        self.element_finder = ElementFinder(self)
        self.table_element_finder = TableElementFinder(self)

    _speed_in_secs = Deprecated('_speed_in_secs', 'speed')
    _timeout_in_secs = Deprecated('_timeout_in_secs', 'timeout')
    _implicit_wait_in_secs = Deprecated('_implicit_wait_in_secs',
                                        'implicit_wait')
    _run_on_failure_keyword = Deprecated('_run_on_failure_keyword',
                                         'run_on_failure_keyword')

    def run_keyword(self, name, args, kwargs):
        try:
            return DynamicCore.run_keyword(self, name, args, kwargs)
        except Exception:
            self.failure_occurred()
            raise

    def register_browser(self, browser, alias):
        return self._browsers.register(browser, alias)

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
    def browser(self):
        """Current active browser"""
        if not self._browsers.current:
            raise RuntimeError('No browser is open')
        return self._browsers.current

    @property
    def _cache(self):
        warnings.warn('"SeleniumLibrary._cache" is deprecated, '
                      'use public API instead.', DeprecationWarning)
        return self._browsers

    def _current_browser(self):
        warnings.warn('"SeleniumLibrary._current_browser" is deprecated, '
                      'use "SeleniumLibrary.browser" instead.',
                      DeprecationWarning)
        return self.browser

    def _run_on_failure(self):
        warnings.warn('"SeleniumLibrary._run_on_failure" is deprecated, '
                      'use "SeleniumLibrary.failure_occurred" instead.',
                      DeprecationWarning)
        self.failure_occurred()
