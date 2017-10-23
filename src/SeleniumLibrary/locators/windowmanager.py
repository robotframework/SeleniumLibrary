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

from robot.api import logger
from selenium.common.exceptions import (NoSuchWindowException,
                                        WebDriverException)

from SeleniumLibrary.base import ContextAware
from SeleniumLibrary.errors import WindowNotFound
from SeleniumLibrary.utils import is_string


WindowInfo = namedtuple('WindowInfo', 'handle, id, name, title, url')


class WindowManager(ContextAware):
    _deprecated_locators = {
        None: 'main',
        'null': 'main',
        '': 'main',
        'popup': 'new',
        'self': 'current'
    }

    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)
        self._strategies = {
            'title': self._select_by_title,
            'name': self._select_by_name,
            'url': self._select_by_url,
            'default': self._select_by_default
        }

    def get_window_infos(self):
        infos = []
        try:
            starting_handle = self.browser.current_window_handle
        except NoSuchWindowException:
            starting_handle = None
        try:
            for handle in self.browser.window_handles:
                self.browser.switch_to.window(handle)
                infos.append(self._get_current_window_info(self.browser))
        finally:
            if starting_handle:
                self.browser.switch_to.window(starting_handle)
        return infos

    def select(self, locator):
        locator = self._handle_deprecated_locators(locator)
        if not is_string(locator):
            self._select_by_excludes(self.browser, locator)
        elif locator.upper() == 'CURRENT':
            pass
        elif locator.upper() == 'MAIN':
            self._select_main_window(self.browser)
        elif locator.upper() == 'NEW':
            self._select_by_last_index(self.browser)
        else:
            strategy, locator = self._parse_locator(locator)
            self._strategies[strategy](self.browser, locator)

    def _handle_deprecated_locators(self, locator):
        if not (is_string(locator) or locator is None):
            return locator
        normalized = locator.lower() if is_string(locator) else locator
        if normalized in self._deprecated_locators:
            new = self._deprecated_locators[normalized]
            logger.warn("Using '%s' as window locator is deprecated. "
                        "Use '%s' instead." % (locator, new))
            return new
        return locator

    def _parse_locator(self, locator):
        index = self._get_locator_separator_index(locator)
        if index != -1:
            prefix = locator[:index].strip()
            if prefix in self._strategies:
                return prefix, locator[index+1:].lstrip()
        return 'default', locator

    def _get_locator_separator_index(self, locator):
        if '=' not in locator:
            return locator.find(':')
        if ':' not in locator:
            return locator.find('=')
        return min(locator.find('='), locator.find(':'))

    def _select_by_title(self, browser, title):
        self._select_matching(
            browser,
            lambda window_info: window_info.title == title,
            "Unable to locate window with title '%s'." % title
        )

    def _select_by_name(self, browser, name):
        self._select_matching(
            browser,
            lambda window_info: window_info.name == name,
            "Unable to locate window with name '%s'." % name
        )

    def _select_by_url(self, browser, url):
        self._select_matching(
            browser,
            lambda window_info: window_info.url == url,
            "Unable to locate window with URL '%s'." % url
        )

    def _select_main_window(self, browser):
        handles = browser.window_handles
        browser.switch_to.window(handles[0])

    def _select_by_default(self, browser, criteria):
        try:
            starting_handle = browser.current_window_handle
        except NoSuchWindowException:
            starting_handle = None
        for handle in browser.window_handles:
            browser.switch_to.window(handle)
            if criteria == handle:
                return
            for item in self._get_current_window_info(browser)[2:4]:
                if item == criteria:
                    return
        if starting_handle:
            browser.switch_to.window(starting_handle)
        raise WindowNotFound("No window matching handle, name, title or URL "
                             "'%s' found." % criteria)

    def _select_by_last_index(self, browser):
        handles = browser.window_handles
        if handles[-1] == browser.current_window_handle:
            raise WindowNotFound('Window with last index is same as '
                                 'the current window.')
        browser.switch_to.window(handles[-1])

    def _select_by_excludes(self, browser, excludes):
        for handle in browser.window_handles:
            if handle not in excludes:
                browser.switch_to.window(handle)
                return
        raise WindowNotFound('No window not matching excludes %s found.'
                             % excludes)

    def _select_matching(self, browser, matcher, error):
        try:
            starting_handle = browser.current_window_handle
        except NoSuchWindowException:
            starting_handle = None
        for handle in browser.window_handles:
            browser.switch_to.window(handle)
            if matcher(self._get_current_window_info(browser)):
                return
        if starting_handle:
            browser.switch_to.window(starting_handle)
        raise WindowNotFound(error)

    def _get_current_window_info(self, browser):
        try:
            id, name = browser.execute_script("return [ window.id, window.name ];")
        except WebDriverException:
            # The webdriver implementation doesn't support Javascript so we
            # can't get window id or name this way.
            id = name = None
        return WindowInfo(browser.current_window_handle,
                          id if id is not None else 'undefined',
                          name or 'undefined',
                          browser.title or 'undefined',
                          browser.current_url or 'undefined')
