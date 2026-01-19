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

import time
from collections import namedtuple

from selenium.common.exceptions import NoSuchWindowException, WebDriverException

from SeleniumLibrary.base import ContextAware
from SeleniumLibrary.errors import WindowNotFound


WindowInfo = namedtuple("WindowInfo", "handle, id, name, title, url")


class WindowManager(ContextAware):
    def __init__(self, ctx):
        ContextAware.__init__(self, ctx)
        self._strategies = {
            "title": self._select_by_title,
            "name": self._select_by_name,
            "url": self._select_by_url,
            "default": self._select_by_default,
        }

    def get_window_handles(self, browser):
        if isinstance(browser, str) and browser == "ALL":
            handles = []
            current_index = self.drivers.current_index
            for index, driver in enumerate(self.drivers, 1):
                self.drivers.switch(index)
                handles.extend(self.driver.window_handles)
            self.drivers.switch(current_index)
            return handles
        elif isinstance(browser, str) and browser == "CURRENT":
            return self.driver.window_handles
        else:
            current_index = self.drivers.current_index
            self.drivers.switch(browser)
            handles = self.driver.window_handles
            self.drivers.switch(current_index)
            return handles

    def get_window_infos(self, browser="CURRENT"):
        try:
            current_index = self.drivers.current_index
        except AttributeError:
            current_index = None
        if isinstance(browser, str) and browser.upper() == "ALL":
            infos = []
            for index, driver in enumerate(self.drivers, 1):
                self.drivers.switch(index)
                infos.extend(self._get_window_infos())
            self.drivers.switch(current_index)
            return infos
        elif isinstance(browser, str) and browser.upper() == "CURRENT":
            return self._get_window_infos()
        else:
            self.drivers.switch(browser)
            infos = self._get_window_infos()
            self.drivers.switch(current_index)
            return infos

    def _get_window_infos(self):
        infos = []
        try:
            starting_handle = self.driver.current_window_handle
        except NoSuchWindowException:
            starting_handle = None
        try:
            for handle in self.driver.window_handles:
                self.driver.switch_to.window(handle)
                infos.append(self._get_current_window_info())
        finally:
            if starting_handle:
                self.driver.switch_to.window(starting_handle)
        return infos

    def select(self, locator, timeout=0):
        while True:
            try:
                return self._select(locator)
            except WindowNotFound:
                if time.time() > timeout:
                    raise
                time.sleep(0.1)

    def _select(self, locator):
        if not isinstance(locator, str):
            self._select_by_excludes(locator)
        elif locator.upper() == "CURRENT":
            pass
        elif locator.upper() == "MAIN":
            self._select_main_window()
        elif locator.upper() == "NEW":
            self._select_by_last_index()
        else:
            strategy, locator = self._parse_locator(locator)
            self._strategies[strategy](locator)

    def _parse_locator(self, locator):
        index = self._get_locator_separator_index(locator)
        if index != -1:
            prefix = locator[:index].strip()
            if prefix in self._strategies:
                return prefix, locator[index + 1 :].lstrip()
        return "default", locator

    def _get_locator_separator_index(self, locator):
        if "=" not in locator:
            return locator.find(":")
        if ":" not in locator:
            return locator.find("=")
        return min(locator.find("="), locator.find(":"))

    def _select_by_title(self, title):
        self._select_matching(
            lambda window_info: window_info.title == title,
            f"Unable to locate window with title '{title}'.",
        )

    def _select_by_name(self, name):
        self._select_matching(
            lambda window_info: window_info.name == name,
            f"Unable to locate window with name '{name}'.",
        )

    def _select_by_url(self, url):
        self._select_matching(
            lambda window_info: window_info.url == url,
            f"Unable to locate window with URL '{url}'.",
        )

    def _select_main_window(self):
        handles = self.driver.window_handles
        self.driver.switch_to.window(handles[0])

    def _select_by_default(self, criteria):
        try:
            starting_handle = self.driver.current_window_handle
        except NoSuchWindowException:
            starting_handle = None
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if criteria == handle:
                return
            for item in self._get_current_window_info()[2:4]:
                if item == criteria:
                    return
        if starting_handle:
            self.driver.switch_to.window(starting_handle)
        raise WindowNotFound(
            f"No window matching handle, name, title or URL '{criteria}' found."
        )

    def _select_by_last_index(self):
        handles = self.driver.window_handles
        if handles[-1] == self.driver.current_window_handle:
            raise WindowNotFound(
                "Window with last index is same as the current window."
            )
        self.driver.switch_to.window(handles[-1])

    def _select_by_excludes(self, excludes):
        for handle in self.driver.window_handles:
            if handle not in excludes:
                self.driver.switch_to.window(handle)
                return
        raise WindowNotFound(f"No window not matching excludes {excludes} found.")

    def _select_matching(self, matcher, error):
        try:
            starting_handle = self.driver.current_window_handle
        except NoSuchWindowException:
            starting_handle = None
        for handle in self.driver.window_handles:
            self.driver.switch_to.window(handle)
            if matcher(self._get_current_window_info()):
                return
        if starting_handle:
            self.driver.switch_to.window(starting_handle)
        raise WindowNotFound(error)

    def _get_current_window_info(self):
        try:
            id, name = self.driver.execute_script("return [ window.id, window.name ];")
        except WebDriverException:
            # The webdriver implementation doesn't support Javascript so we
            # can't get window id or name this way.
            id = name = None
        return WindowInfo(
            self.driver.current_window_handle,
            id if id is not None else "undefined",
            name or "undefined",
            self.driver.title or "undefined",
            self.driver.current_url or "undefined",
        )
