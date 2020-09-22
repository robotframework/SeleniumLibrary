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
from typing import Any, Optional, List

from selenium.webdriver.remote.webelement import WebElement

from SeleniumLibrary.utils import escape_xpath_value


class ContextAware:
    def __init__(self, ctx):
        """Base class exposing attributes from the common context.

        :param ctx: The library itself as a context object.
        :type ctx: SeleniumLibrary.SeleniumLibrary
        """
        self.ctx = ctx

    @property
    def driver(self):
        return self.ctx.driver

    @property
    def drivers(self):
        return self.ctx._drivers

    @property
    def element_finder(self):
        return self.ctx._element_finder

    @element_finder.setter
    def element_finder(self, value: Any):
        self.ctx._element_finder = value

    @property
    def event_firing_webdriver(self):
        return self.ctx.event_firing_webdriver

    @event_firing_webdriver.setter
    def event_firing_webdriver(self, event_firing_webdriver: Any):
        self.ctx.event_firing_webdriver = event_firing_webdriver

    def find_element(
        self,
        locator: str,
        tag: Optional[str] = None,
        required: bool = True,
        parent: WebElement = None,
    ) -> WebElement:
        """Find element matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :type locator: str or selenium.webdriver.remote.webelement.WebElement
        :param tag: Limit searching only to these elements.
        :type tag: str
        :param required: Raise `ElementNotFound` if element not found when
            true, return `None` otherwise.
        :type required: True or False
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default, search starts from the root using `WebDriver`.
        :type parent: selenium.webdriver.remote.webelement.WebElement
        :return: Found `WebElement` or `None` if element not found and
            `required` is false.
        :rtype: selenium.webdriver.remote.webelement.WebElement
        :raises SeleniumLibrary.errors.ElementNotFound: If element not found
            and `required` is true.
        """
        return self.element_finder.find(locator, tag, True, required, parent)

    def find_elements(
        self, locator: str, tag: Optional[str] = None, parent: WebElement = None
    ) -> List[WebElement]:
        """Find all elements matching `locator`.

        :param locator: Locator to use when searching the element.
            See library documentation for the supported locator syntax.
        :type locator: str or selenium.webdriver.remote.webelement.WebElement
        :param tag: Limit searching only to these elements.
        :type tag: str
        :param parent: Optional parent `WebElememt` to search child elements
            from. By default, search starts from the root using `WebDriver`.
        :type parent: selenium.webdriver.remote.webelement.WebElement
        :return: list of found `WebElement` or empty if elements are not found.
        :rtype: list[selenium.webdriver.remote.webelement.WebElement]
        """
        return self.element_finder.find(locator, tag, False, False, parent)

    def is_text_present(self, text: str):
        locator = f"xpath://*[contains(., {escape_xpath_value(text)})]"
        return self.find_element(locator, required=False) is not None

    def is_element_enabled(self, locator: str, tag: Optional[str] = None) -> bool:
        element = self.find_element(locator, tag)
        return element.is_enabled() and element.get_attribute("readonly") is None

    def is_visible(self, locator: str) -> bool:
        element = self.find_element(locator, required=False)
        return element.is_displayed() if element else None
