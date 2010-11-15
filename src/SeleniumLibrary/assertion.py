#  Copyright 2008-2010 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

from runonfailure import RunOnFailure


class Assertion(RunOnFailure):

    def title_should_be(self, title):
        """Verifies that current page title equals `title`."""
        actual = self._selenium.get_title()
        if  actual != title:
            raise AssertionError("Title should have been '%s' but was '%s'"
                                  % (title, actual))
        self._info("Page title is '%s'." % title)

    def location_should_be(self, url):
        """Verifies that current URL is exactly `url`."""
        actual = self._selenium.get_location()
        if  actual != url:
            raise AssertionError("Location should have been '%s' but was '%s'"
                                 % (url, actual))
        self._info("Current location is '%s'." % url)

    def location_should_contain(self, expected):
        """Verifies that current URL contains `expected`."""
        actual = self._selenium.get_location()
        if not expected in actual:
            raise AssertionError("Location should have contained '%s' "
                                 "but it was '%s'." % (expected, actual))
        self._info("Current location contains '%s'." % expected)

    def page_should_contain(self, text, loglevel='INFO'):
        """Verifies that current page contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.

        The `loglevel` argument was added in SeleniumLibrary 2.3.1 and the special
        `NONE` argument value in SeleniumLibrary 2.5.
        """
        if not self._page_contains(text):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def page_should_not_contain(self, text, loglevel='INFO'):
        """Verifies the current page does not contain `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.

        The `loglevel`argument was added in SeleniumLibrary 2.5.
        """
        if self._page_contains(text):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s'" % text)
        self._info("Current page does not contain text '%s'." % text)

    current_frame_should_contain = current_frame_contains = page_should_contain

    def _page_contains(self, text):
        return self._selenium.is_text_present(text) or \
            self._search_text_in_frames(text)

    def _search_text_in_frames(self, text):
        js = "window.document.getElementsByTagName('frame').length"
        num_of_subframes = int(self._selenium.get_eval(js))
        self._debug('Current frame has %d subframes' % num_of_subframes)
        for i in range(num_of_subframes):
            xpath = 'xpath=//frame[%d]' % (i+1)
            self.select_frame(xpath)
            if self._selenium.is_text_present(text):
                self.unselect_frame()
                return True
            self.unselect_frame()
        return False

    def frame_should_contain(self, locator, text):
        """Verifies frame identified by `locator` contains `text`.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        """
        self._selenium.select_frame(self._parse_locator(locator))
        self._info("Searching for text from frame '%s'." % locator)
        try:
            self.page_should_contain(text)
        finally:
            self.unselect_frame()

    frame_should_contain_text = frame_should_contain

    def element_should_contain(self, locator, expected, message=''):
        """Verifies element identified by `locator` contains text `expected`.

        If you wish to assert an exact (not a substring) match on the text
        of the element, use `Element Text Should Be`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Verifying element '%s' contains text '%s'."
                    % (locator, expected))
        actual = self._selenium.get_text(self._parse_locator(locator))
        if not expected in actual:
            if not message:
                message = "Element '%s' should have contained text '%s' but "\
                          "its text was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def element_text_should_be(self, locator, expected, message=''):
        """Verifies element identified by `locator` exactly contains text `expected`.

        In contrast to `Element Should Contain`, this keyword does not try
        a substring match but an exact match on the element identified by `locator`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Verifying element '%s' exactly contains text '%s'."
                    % (locator, expected))
        actual = self._selenium.get_text(self._parse_locator(locator))
        if expected != actual:
            if not message:
                message = "The text of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def element_should_be_visible(self, locator, message=''):
        """Verifies that the element identified by `locator` is visible.

        Herein, visible means that the element is logically visible, not optically
        visible in the current browser viewport. For example, an element that carries
        display:none is not logically visible, so using this keyword on that element
        would fail.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Verifying element '%s' is visible." % locator)
        visible = self._selenium.is_visible(locator)
        if not visible:
            if not message:
                message = "The element '%s' should be visible, but it "\
                          "is not." % locator
            raise AssertionError(message)

    def element_should_not_be_visible(self, locator, message=''):
        """Verifies that the element identified by `locator` is NOT visible.

        This is the opposite of `Element Should Be Visible`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        This keyword was added in SeleniumLibrary 2.5.
        """
        self._info("Verifying element '%s' is not visible." % locator)
        visible = self._selenium.is_visible(locator)
        if visible:
            if not message:
                message = "The element '%s' should not be visible, "\
                          "but it is." % locator
            raise AssertionError(message)

    def page_should_contain_element(self, locator, message='', loglevel='INFO'):
        """Verifies element identified by `locator` is found from current page.

        `message` can be used to override default error message.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Giving `NONE` as level disables logging.

        The `loglevel` argument was added in SeleniumLibrary 2.5.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'element', message, loglevel)

    def page_should_not_contain_element(self, locator, message='', loglevel='INFO'):
        """Verifies element identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'element', message, loglevel)

    def page_should_contain_checkbox(self, locator, message='', loglevel='INFO'):
        """Verifies checkbox identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_contain_element(locator, 'checkbox', message, loglevel)

    def page_should_not_contain_checkbox(self, locator, message='', loglevel='INFO'):
        """Verifies checkbox identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'checkbox', message, loglevel)

    def page_should_contain_radio_button(self, locator, message='', loglevel='INFO'):
        """Verifies radio button identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for radio buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'radio button', message, loglevel)

    def page_should_not_contain_radio_button(self, locator, message='', loglevel='INFO'):
        """Verifies radio button identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for radio buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'radio button', message, loglevel)

    def page_should_contain_image(self, locator, message='', loglevel='INFO'):
        """Verifies image identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'image', message, loglevel)

    def page_should_not_contain_image(self, locator, message='', loglevel='INFO'):
        """Verifies image identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'image', message, loglevel)

    def page_should_contain_link(self, locator, message='', loglevel='INFO'):
        """Verifies link identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'link', message, loglevel)

    def page_should_not_contain_link(self, locator, message='', loglevel='INFO'):
        """Verifies link identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'link', message, loglevel)

    def page_should_contain_list(self, locator, message='', loglevel='INFO'):
        """Verifies list identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._page_should_contain_element(locator, 'list', message, loglevel)

    def page_should_not_contain_list(self, locator, message='', loglevel='INFO'):
        """Verifies list identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'list', message, loglevel)

    def page_should_contain_textfield(self, locator, message='', loglevel='INFO'):
        """Verifies text field identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_contain_element(locator, 'text field', message, loglevel)

    def page_should_not_contain_textfield(self, locator, message='', loglevel='INFO'):
        """Verifies text field identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'text field', message, loglevel)

    def page_should_contain_button(self, locator, message='', loglevel='INFO'):
        """Verifies button identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        try:
            self._page_should_contain_element(locator, 'input', message, loglevel)
        except AssertionError:
            self._page_should_contain_element(locator, 'button', message, loglevel)

    def page_should_not_contain_button(self, locator, message='', loglevel='INFO'):
        """Verifies button identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'button', message, loglevel)
        self._page_should_not_contain_element(locator, 'input', message, loglevel)

    def xpath_should_match_x_times(self, xpath, expected_xpath_count, message='', loglevel='INFO'):
        """Verifies that the page contains the given number of elements located by the given `xpath`.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        This keyword was added in SeleniumLibrary 2.5.
        """
        actual_xpath_count = self._selenium.get_xpath_count(xpath)
        expected_xpath_count = str(expected_xpath_count)
        if actual_xpath_count != expected_xpath_count:
            if not message:
                message = "Xpath %s should have matched %s times but matched %s times"\
                            %(xpath, expected_xpath_count, actual_xpath_count)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Current page contains %s elements matching '%s'." % (actual_xpath_count, xpath))

    def _page_should_contain_element(self, locator, element_name, message, loglevel):
        if not self._selenium.is_element_present(self._parse_locator(
                                                 locator, element_name)):
            if not message:
                message = "Page should have contained %s '%s' but did not"\
                           % (element_name, locator)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Current page contains %s '%s'." % (element_name, locator))

    def _page_should_not_contain_element(self, locator, element_name, message, loglevel):
        if self._selenium.is_element_present(self._parse_locator(
                                             locator, element_name)):
            if not message:
                message = "Page should not have contained %s '%s'"\
                           % (element_name, locator)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Current page does not contain %s '%s'."
                   % (element_name, locator))

    def text_field_should_contain(self, locator, expected, message=''):
        """Verifies text field identified by `locator` contains text `expected`.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self.get_value(locator)
        if not expected in actual:
            if not message:
                message = "Text field '%s' should have contained text '%s' "\
                          "but it contained '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Text field '%s' contains text '%s'." % (locator, expected))

    def textfield_value_should_be(self, locator, expected, message=''):
        """Verifies the value in text field identified by `locator` is exactly `expected`.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        actual = self.get_value(locator)
        if actual != expected:
            if not message:
                message = "Value of text field '%s' should have been '%s' "\
                          "but was '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Content of text field '%s' is '%s'." % (locator, expected))
