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

from SeleniumLibrary.base import LibraryComponent, keyword


class FrameKeywords(LibraryComponent):

    @keyword
    def select_frame(self, locator):
        """Sets frame identified by ``locator`` as the current frame.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.

        See `Unselect Frame` to cancel the frame selection and return to the Main frame.

        Please note that the frame search always start from the document root or main frame.

        Example:
        | Select Frame   | xpath: //frame[@name='top]/iframe[@name='left'] | # Selects the 'left' iframe |
        | Click Link     | foo                                             | # Clicks link 'foo' in 'left' iframe |
        | Unselect Frame |                                                 | # Returns to main frame |
        | Select Frame   | left                                            | # Selects the 'top' frame |
        """
        self.info("Selecting frame '%s'." % locator)
        element = self.find_element(locator)
        self.browser.switch_to.frame(element)

    @keyword
    def unselect_frame(self):
        """Sets the top frame as the current frame.

        In practice cancels a previous `Select Frame` call.
        """
        self.browser.switch_to.default_content()

    @keyword
    def current_frame_should_contain(self, text, loglevel='INFO'):
        """Verifies that current frame contains ``text``.

        See `Page Should Contain` for explanation about the ``loglevel``
        argument.

        Prior to SeleniumLibrary 3.0 this keyword was named
        `Current Frame Contains`.
        """
        if not self.is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError("Frame should have contained text '%s' "
                                 "but did not." % text)
        self.info("Current frame contains text '%s'." % text)

    @keyword
    def current_frame_contains(self, text, loglevel='INFO'):
        """Deprecated. Use `Current Frame Should Contain` instead."""
        self.current_frame_should_contain(text, loglevel)

    @keyword
    def current_frame_should_not_contain(self, text, loglevel='INFO'):
        """Verifies that current frame contains ``text``.

        See `Page Should Contain` for explanation about the ``loglevel``
        argument.
        """
        if self.is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError("Frame should not have contained text '%s' "
                                 "but it did." % text)
        self.info("Current frame did not contain text '%s'." % text)

    @keyword
    def frame_should_contain(self, locator, text, loglevel='INFO'):
        """Verifies that frame identified by ``locator`` contains ``text``.

        See the `Locating elements` section for details about the locator
        syntax.

        See `Page Should Contain` for explanation about the ``loglevel``
        argument.
        """
        if not self._frame_contains(locator, text):
            self.log_source(loglevel)
            raise AssertionError("Frame '%s' should have contained text '%s' "
                                 "but did not." % (locator, text))
        self.info("Frame '%s' contains text '%s'." % (locator, text))

    def _frame_contains(self, locator, text):
        element = self.find_element(locator)
        self.browser.switch_to.frame(element)
        self.info("Searching for text from frame '%s'." % locator)
        found = self.is_text_present(text)
        self.browser.switch_to.default_content()
        return found

