#  Copyright 2008-2009 Nokia Siemens Networks Oyj
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

class Assertion(object):

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

    def page_should_contain(self, text, level='INFO'):
        """Verifies that current page contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `level` argument.
        This argument was added in SeleniumLibrary 2.3.1.
        """
        if not (self._selenium.is_text_present(text) or
                    self._search_text_in_frames(text)):
            self.log_source(level)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def page_should_not_contain(self, text):
        """Verifies the current page does not contain `text`."""
        if self._selenium.is_text_present(text):
            self.log_source()
            raise AssertionError("Page should not have contained text '%s'" % text)
        self._info("Current page does not contain text '%s'." % text)

    current_frame_should_contain = current_frame_contains = page_should_contain

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

    def element_should_contain(self, locator, excepted, message=''):
        """Verifies element identified by `locator` contains text `expected`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Verifying element '%s' contains text '%s'."
                    % (locator, excepted))
        actual = self._selenium.get_text(self._parse_locator(locator))
        if not excepted in actual:
            if not message:
                message = "Element '%s' should have contained text '%s' but "\
                          "it's text is '%s'." % (locator, excepted, actual)
            raise AssertionError(message)

    def page_should_contain_checkbox(self, locator, message=''):
        """Verifies checkbox identified by `locator` is found from current page.

        `message` can be used to override default error message.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_contain_element(locator, 'checkbox', message)

    def page_should_not_contain_checkbox(self, locator, message=''):
        """Verifies checkbox identified by `locator` is not found from current page.

        `message` can be used to override default error message.

        Key attributes for checkboxes are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'checkbox', message)

    def page_should_contain_radio_button(self, locator, message=''):
        """Verifies radio button identified by `locator` is found from current page.

        `message` can be used to override default error message.

        Key attributes for radio buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'radio button', message)

    def page_should_not_contain_radio_button(self, locator, message=''):
        """Verifies radio button identified by `locator` is not found from current page.

        `message` can be used to override default error message.

        Key attributes for radio buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'radio button', message)

    def page_should_contain_element(self, locator, message=''):
        """Verifies element identified by `locator` is found from current page.

        `message` can be used to override default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'element', message)

    def page_should_not_contain_element(self, locator, message=''):
        """Verifies element identified by `locator` is not found from current page.

        `message` can be used to override default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'element', message)

    def page_should_contain_image(self, locator, message=''):
        """Verifies image identified by `locator` is found from current page.

        `message` can be used to override default error message.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'image', message)

    def page_should_not_contain_image(self, locator, message=''):
        """Verifies image identified by `locator` is not found from current page.

        `message` can be used to override default error message.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'image', message)

    def page_should_contain_link(self, locator, message=''):
        """Verifies link identified by `locator` is found from current page.

        `message` can be used to override default error message.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'link', message)

    def page_should_not_contain_link(self, locator, message=''):
        """Verifies link identified by `locator` is not found from current page.

        `message` can be used to override default error message.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'link', message)

    def page_should_contain_list(self, locator, message=''):
        """Verifies list identified by `locator` is found from current page.

        `message` can be used to override default error message.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._page_should_contain_element(locator, 'list', message)

    def page_should_not_contain_list(self, locator, message=''):
        """Verifies list identified by `locator` is not found from current page.

        `message` can be used to override default error message.

        Key attributes for lists are `id` and `name`. See `introduction` for
        details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'list', message)

    def page_should_contain_textfield(self, locator, message=''):
        """Verifies text field identified by `locator` is found from current page.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_contain_element(locator, 'text field', message)

    def page_should_not_contain_textfield(self, locator, message=''):
        """Verifies text field identified by `locator` is not found from current page.

        `message` can be used to override default error message.

        Key attributes for text fields are `id` and `name`. See `introduction`
        for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'text field', message)

    def page_should_contain_button(self, locator, message=''):
        """Verifies button identified by `locator` is found from current page.

        `message` can be used to override default error message.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        try:
            self._page_should_contain_element(locator, 'input', message)
        except AssertionError:
            self._page_should_contain_element(locator, 'button', message)

    def page_should_not_contain_button(self, locator, message=''):
        """Verifies button identified by `locator` is not found from current page.

        `message` can be used to override default error message.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'button', message)
        self._page_should_not_contain_element(locator, 'input', message)

    def _page_should_contain_element(self, locator, element_name, message):
        if not self._selenium.is_element_present(self._parse_locator(
                                                 locator, element_name)):
            if not message:
                message = "Page should have contained %s '%s' but did not"\
                           % (element_name, locator)
            self.log_source()
            raise AssertionError(message)
        self._info("Current page contains %s '%s'." % (element_name, locator))

    def _page_should_not_contain_element(self, locator, element_name, message):
        if self._selenium.is_element_present(self._parse_locator(
                                             locator, element_name)):
            if not message:
                message = "Page should not have contained %s '%s'"\
                           % (element_name, locator)
            self.log_source()
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

