import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(ROOT_DIR, "lib", "selenium-2.8.1", "py"))
sys.path.append(os.path.join(ROOT_DIR, "lib", "decorator-3.3.2"))

from keywords import *

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
    ROBOT_LIBRARY_VERSION = 0.5

    def __init__(self):
        for base in Selenium2Library.__bases__:
            base.__init__(self)
