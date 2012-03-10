import os
from keywords import *

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
execfile(os.path.join(THIS_DIR, 'version.py'))

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
    _WaitingKeywords
):
    """Selenium2Library is a web testing library for Robot Framework.

    It uses the Selenium 2 (WebDriver) libraries internally to control a web browser.
    See http://seleniumhq.org/docs/03_webdriver.html for more information on Selenium 2
    and WebDriver.

    Selenium2Library runs tests in a real browser instance. It should work in
    most modern browsers and can be used with both Python and Jython interpreters.

    *Before running tests*

    Prior to running test cases using Selenium2Library, Selenium2Library must be
    imported into your Robot test suite (see `importing` section), and the 
    `Open Browser` keyword must be used to open a browser to the desired location.

    *Locating elements*

    All keywords in Selenium2Library that need to find an element on the page
    take an argument, `locator`. By default, when a locator value is provided,
    it is matched against the key attributes of the particular element type.
    For example, `id` and `name` are key attributes to all elements, and
    locating elements is easy using just the `id` as a `locator`. For example::

    Click Element  my_element

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
    | css        | Click Element `|` css=div.my_class      | Matches by CSS selector                         |
    | tag        | Click Element `|` tag=div               | Matches by HTML tag name                        |

    Table related keywords, such as `Table Should Contain`, work differently.
    By default, when a table locator value is provided, it will search for
    a table with the specified `id` attribute. For example:

    Table Should Contain  my_table  text

    More complex table lookup strategies are also supported:

    | *Strategy* | *Example*                                                          | *Description*                     |
    | css        | Table Should Contain `|` css=table.my_class `|` text               | Matches by @id or @name attribute |
    | xpath      | Table Should Contain `|` xpath=//table/[@name="my_table"] `|` text | Matches by @id or @name attribute |

    *Timeouts*

    There are several `Wait ...` keywords that take timeout as an
    argument. All of these timeout arguments are optional. The timeout
    used by all of them can be set globally using the
    `Set Selenium Timeout` keyword.

    All timeouts can be given as numbers considered seconds (e.g. 0.5 or 42)
    or in Robot Framework's time syntax (e.g. '1.5 seconds' or '1 min 30 s').
    For more information about the time syntax see:
    http://robotframework.googlecode.com/svn/trunk/doc/userguide/RobotFrameworkUserGuide.html#time-format.
    """

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, timeout=5.0, implicit_wait=0.0, run_on_failure='Capture Page Screenshot'):
        """Selenium2Library can be imported with optional arguments.

        `timeout` is the default timeout used to wait for all waiting actions.
        It can be later set with `Set Selenium Timeout`.

        'implicit_wait' is the implicit timeout that Selenium waits when
        looking for elements.
        It can be later set with 'Set Selenium Implicit Wait'.

        `run_on_failure` specifies the name of a keyword (from any available
        libraries) to execute when a Selenium2Library keyword fails. By default
        `Capture Page Screenshot` will be used to take a screenshot of the current page.
        Using the value "Nothing" will disable this feature altogether. See
        `Register Keyword To Run On Failure` keyword for more information about this
        functionality.

        Examples:
        | Library `|` Selenium2Library `|` 15                                     | # Sets default timeout to 15 seconds                                  |
        | Library `|` Selenium2Library `|` 5 `|` Log Source                       | # Sets default timeout to 5 seconds and runs `Log Source` on failure  |
        | Library `|` Selenium2Library `|` timeout=10 `|` run_on_failure=Nothing  | # Sets default timeout to 10 seconds and does nothing on failure      |
        """
        for base in Selenium2Library.__bases__:
            base.__init__(self)
        self.set_selenium_timeout(timeout)
        self.set_selenium_implicit_wait(implicit_wait)
        self.register_keyword_to_run_on_failure(run_on_failure)
