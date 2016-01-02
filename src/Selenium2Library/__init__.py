import os
from keywords import *
from version import VERSION
from utils import LibraryListener

__version__ = VERSION

class Selenium2Library(
    _LoggingKeywords,
    _RunOnFailureKeywords,
    _BrowserManagementKeywords,
    _ElementKeywords,
    _TableElementKeywords,
    _FormElementKeywords,
    _SelectElementKeywords,
    _JavaScriptKeywords,
    _CookieKeywords,
    _ScreenshotKeywords,
    _WaitingKeywords,
    _AlertKeywords
):
    """Selenium2Library is a web testing library for Robot Framework.

    It uses the Selenium 2 (WebDriver) libraries internally to control a web browser.
    See http://seleniumhq.org/docs/03_webdriver.html for more information on Selenium 2
    and WebDriver.

    Selenium2Library runs tests in a real browser instance. It should work in
    most modern browsers and can be used with both Python and Jython interpreters.

    = Before running tests =

    Prior to running test cases using Selenium2Library, Selenium2Library must be
    imported into your Robot test suite (see `importing` section), and the
    `Open Browser` keyword must be used to open a browser to the desired location.


    *--- Note important change starting with Version 1.7.0 release ---*
    = Locating or specifying elements =

    All keywords in Selenium2Library that need to find an element on the page
    take an argument, either a `locator` or now a `webelement`. `locator`
    is a string that describes how to locate an element using a syntax
    specifying different location strategies. `webelement` is a variable that
    holds a WebElement instance, which is a representation of the element.

    *Using locators*
    ---------------
    By default, when a locator value is provided, it is matched against the
    key attributes of the particular element type. For example, `id` and
    `name` are key attributes to all elements, and locating elements is easy
    using just the `id` as a `locator`. For example:

    | Click Element    my_element

    It is also possible to specify the approach Selenium2Library should take
    to find an element by specifying a lookup strategy with a locator
    prefix. Supported strategies are:

    | *Strategy* | *Example*                               | *Description*                                   |
    | identifier | Click Element `|` identifier=my_element | Matches by @id or @name attribute               |
    | id         | Click Element `|` id=my_element         | Matches by @id attribute                        |
    | name       | Click Element `|` name=my_element       | Matches by @name attribute                      |
    | xpath      | Click Element `|` xpath=//div[@id='my_element'] | Matches with arbitrary XPath expression |
    | dom        | Click Element `|` dom=document.images[56] | Matches with arbitrary DOM express            |
    | link       | Click Element `|` link=My Link          | Matches anchor elements by their link text      |
    | partial link | Click Element `|` partial link=y Lin  | Matches anchor elements by their partial link text |
    | css        | Click Element `|` css=div.my_class      | Matches by CSS selector                         |
    | jquery     | Click Element `|` jquery=div.my_class   | Matches by jQuery/sizzle selector                         |
    | sizzle     | Click Element `|` sizzle=div.my_class   | Matches by jQuery/sizzle selector                         |
    | tag        | Click Element `|` tag=div               | Matches by HTML tag name                        |
    | default*   | Click Link    `|` default=page?a=b      | Matches key attributes with value after first '=' |
    * Explicitly specifying the default strategy is only necessary if locating
    elements by matching key attributes is desired and an attribute value
    contains a '='. The following would fail because it appears as if _page?a_
    is the specified lookup strategy:
    | Click Link    page?a=b
    This can be fixed by changing the locator to:
    | Click Link    default=page?a=b

    *Using webelements*
    ------------------
    Starting with version 1.7 of the Selenium2Library, one can pass an argument
    that contains a WebElement instead of a string locator. To get a WebElement,
    use the new `Get WebElements` keyword.  For example:

    | ${elem} =      | Get WebElement | id=my_element |
    | Click Element  | ${elem} |                      |

    Locating Tables, Table Rows, Columns, etc.
    ------------------------------------------
    Table related keywords, such as `Table Should Contain`, work differently.
    By default, when a table locator value is provided, it will search for
    a table with the specified `id` attribute. For example:

    | Table Should Contain    my_table    text

    More complex table lookup strategies are also supported:

    | *Strategy* | *Example*                                                          | *Description*                     |
    | css        | Table Should Contain `|` css=table.my_class `|` text               | Matches by @id or @name attribute |
    | xpath      | Table Should Contain `|` xpath=//table/[@name="my_table"] `|` text | Matches by @id or @name attribute |

    = Custom Locators =

    If more complex lookups are required than what is provided through the default locators, custom lookup strategies can
    be created. Using custom locators is a two part process. First, create a keyword that returns the WebElement
    that should be acted on.

    | Custom Locator Strategy | [Arguments] | ${browser} | ${criteria} | ${tag} | ${constraints} |
    |   | ${retVal}= | Execute Javascript | return window.document.getElementById('${criteria}'); |
    |   | [Return] | ${retVal} |

    This keyword is a reimplementation of the basic functionality of the `id` locator where `${browser}` is a reference
    to the WebDriver instance and `${criteria}` is the text of the locator (i.e. everything that comes after the = sign).
    To use this locator it must first be registered with `Add Location Strategy`.

    | Add Location Strategy    custom    Custom Locator Strategy

    The first argument of `Add Location Strategy` specifies the name of the lookup strategy (which must be unique). After
    registration of the lookup strategy, the usage is the same as other locators. See `Add Location Strategy` for more details.

    = Timeouts =

    There are several `Wait ...` keywords that take timeout as an
    argument. All of these timeout arguments are optional. The timeout
    used by all of them can be set globally using the
    `Set Selenium Timeout` keyword. The same timeout also applies to
    `Execute Async Javascript`.

    All timeouts can be given as numbers considered seconds (e.g. 0.5 or 42)
    or in Robot Framework's time syntax (e.g. '1.5 seconds' or '1 min 30 s').
    For more information about the time syntax see:
    http://robotframework.googlecode.com/svn/trunk/doc/userguide/RobotFrameworkUserGuide.html#time-format.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self,
                 timeout=5.0,
                 implicit_wait=0.0,
                 run_on_failure='Capture Page Screenshot',
                 screenshot_root_directory=None
    ):

        """Selenium2Library can be imported with optional arguments.

        `timeout` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Selenium Timeout`.

        'implicit_wait' is the implicit timeout that Selenium waits when
        looking for elements.
        It can be later set with `Set Selenium Implicit Wait`.
        See `WebDriver: Advanced Usage`__ section of the SeleniumHQ documentation
        for more information about WebDriver's implicit wait functionality.

        __ http://seleniumhq.org/docs/04_webdriver_advanced.html#explicit-and-implicit-waits

        `run_on_failure` specifies the name of a keyword (from any available
        libraries) to execute when a Selenium2Library keyword fails. By default
        `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value "Nothing" will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        `screenshot_root_directory` specifies the default root directory that screenshots should be
        stored in. If not provided the default directory will be where robotframework places its logfile.

        Examples:
        | Library `|` Selenium2Library `|` 15                                            | # Sets default timeout to 15 seconds                                       |
        | Library `|` Selenium2Library `|` 0 `|` 5                                       | # Sets default timeout to 0 seconds and default implicit_wait to 5 seconds |
        | Library `|` Selenium2Library `|` 5 `|` run_on_failure=Log Source               | # Sets default timeout to 5 seconds and runs `Log Source` on failure       |
        | Library `|` Selenium2Library `|` implicit_wait=5 `|` run_on_failure=Log Source | # Sets default implicit_wait to 5 seconds and runs `Log Source` on failure |
        | Library `|` Selenium2Library `|` timeout=10      `|` run_on_failure=Nothing    | # Sets default timeout to 10 seconds and does nothing on failure           |
        """
        for base in Selenium2Library.__bases__:
            base.__init__(self)
        self.screenshot_root_directory = screenshot_root_directory
        self.set_selenium_timeout(timeout)
        self.set_selenium_implicit_wait(implicit_wait)
        self.register_keyword_to_run_on_failure(run_on_failure)
        self.ROBOT_LIBRARY_LISTENER = LibraryListener()
