import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(ROOT_DIR, "lib", "selenium-2.8.1", "py"))
sys.path.insert(0, os.path.join(ROOT_DIR, "lib", "decorator-3.3.2"))

from keywords import *
from metadata import VERSION

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
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = VERSION

    def __init__(self, timeout=5.0, run_on_failure='Capture Page Screenshot'):
        for base in Selenium2Library.__bases__:
            base.__init__(self)
        self.set_selenium_timeout(timeout)
        self.register_keyword_to_run_on_failure(run_on_failure)
