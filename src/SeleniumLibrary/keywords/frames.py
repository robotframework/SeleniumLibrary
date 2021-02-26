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
from typing import Union

from selenium.webdriver.remote.webelement import WebElement

from SeleniumLibrary.base import LibraryComponent, keyword


class FrameKeywords(LibraryComponent):
    @keyword
    def select_frame(self, locator: Union[WebElement, str]):
        """Sets frame identified by ``locator`` as the current frame.

        See the `Locating elements` section for details about the locator
        syntax.

        Works both with frames and iframes. Use `Unselect Frame` to cancel
        the frame selection and return to the main frame.

        Example:
        | `Select Frame`   | top-frame | # Select frame with id or name 'top-frame'   |
        | `Click Link`     | example   | # Click link 'example' in the selected frame |
        | `Unselect Frame` |           | # Back to main frame.                        |
        | `Select Frame`   | //iframe[@name='xxx'] | # Select frame using xpath       |
        """
        self.info(f"Selecting frame '{locator}'.")
        element = self.find_element(locator)
        self.driver.switch_to.frame(element)

    @keyword
    def unselect_frame(self):
        """Sets the main frame as the current frame.

        In practice cancels the previous `Select Frame` call.
        """
        self.driver.switch_to.default_content()

    @keyword
    def current_frame_should_contain(self, text: str, loglevel: str = "TRACE"):
        """Verifies that the current frame contains ``text``.

        See `Page Should Contain` for an explanation about the ``loglevel``
        argument.

        Prior to SeleniumLibrary 3.0 this keyword was named
        `Current Frame Contains`.
        """
        if not self.is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError(
                f"Frame should have contained text '{text}' but did not."
            )
        self.info(f"Current frame contains text '{text}'.")

    @keyword
    def current_frame_should_not_contain(self, text: str, loglevel: str = "TRACE"):
        """Verifies that the current frame does not contain ``text``.

        See `Page Should Contain` for an explanation about the ``loglevel``
        argument.
        """
        if self.is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError(
                f"Frame should not have contained text '{text}' but it did."
            )
        self.info(f"Current frame did not contain text '{text}'.")

    @keyword
    def frame_should_contain(
        self, locator: Union[WebElement, str], text: str, loglevel: str = "TRACE"
    ):
        """Verifies that frame identified by ``locator`` contains ``text``.

        See the `Locating elements` section for details about the locator
        syntax.

        See `Page Should Contain` for an explanation about the ``loglevel``
        argument.
        """
        if not self._frame_contains(locator, text):
            self.log_source(loglevel)
            raise AssertionError(
                f"Frame '{locator}' should have contained text '{text}' but did not."
            )
        self.info(f"Frame '{locator}' contains text '{text}'.")

    def _frame_contains(self, locator: Union[WebElement, str], text: str):
        element = self.find_element(locator)
        self.driver.switch_to.frame(element)
        self.info(f"Searching for text from frame '{locator}'.")
        found = self.is_text_present(text)
        self.driver.switch_to.default_content()
        return found
