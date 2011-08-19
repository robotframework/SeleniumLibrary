import os
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(os.path.join(_THIS_DIR, "lib", "selenium-2.4.0", "py"))

from robot.variables import GLOBAL_VARIABLES
from robot import utils

from selenium import webdriver
    
FIREFOX_PROFILE_DIR = os.path.join(_THIS_DIR, 'firefoxprofile')
BROWSER_ALIASES = {'ff': '*firefox',
                    'firefox': '*firefox',
                    'ie': '*iexplore',
                    'internetexplorer': '*iexplore',
                    'googlechrome': '*googlechrome',
                    'gc': '*googlechrome'
                   }

class Selenium2Library():

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.5

    def __init__(self):
        self._cache = utils.ConnectionCache()
        self._browser = None

    def open_browser(self, url, browser='firefox', alias=None):
        self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        self._browser = self._get_browser_instance(browser)
        self._browser.get(url)
        self._debug('Opened browser with session id %s'
                    % self._browser.session_id)
        return self._cache.register(self._browser, alias)

    def close_browser(self):
        if (self._browser):
            self._debug('Closing browser with session id %s'
                        % self._browser.session_id)
            self._cache.current = None
            self._browser.close();

    def _get_browser_instance(self, browser_alias):
        browser_token = self._get_browser_token(browser_alias)
        if browser_token == '*firefox':
            return webdriver.Firefox(FirefoxProfile(FIREFOX_PROFILE_DIR))
        if browser_token == '*googlechrome':
            return webdriver.Chrome()
        if browser_token == '*iexplore':
            return webdriver.Ie()
        raise AssertionError(browser_alias + " is not a supported browser alias")

    def _get_browser_token(self, browser_alias):
        return BROWSER_ALIASES.get(browser_alias.lower().replace(' ', ''), browser_alias)

    def _get_log_dir(self):
        logfile = GLOBAL_VARIABLES['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return GLOBAL_VARIABLES['${OUTPUTDIR}']

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

    def _get_error_message(self, exception):
        # Cannot use unicode(exception) because it fails on Python 2.5 and
        # earlier if the message contains non-ASCII chars.
        # See for details: http://bugs.jython.org/issue1585
        return unicode(exception.args and exception.args[0] or '')

    def _error_contains(self, exception, message):
        return message in self._get_error_message(exception)

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s',''][len(items)==1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index+1, item))
        self._info('\n'.join(msg))
        return items
