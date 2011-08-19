#  Copyright 2008-2011 Nokia Siemens Networks Oyj
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


class Click(RunOnFailure):
    """Contains keywords for clicking different elements."""

    def click_element(self, locator, dont_wait='', coordinates=None):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.

        If you want to click the element at certain coordinates, you can
        specify the position with `coordinates` argument in format `x,y`.
        Support for coordinates was added in SeleniumLibrary 2.7.

        Examples:
        | Click Element | my_id |
        | Click Element | my_id | and don't wait |
        | Click Element | my_id |  | 100,150 |
        | Click Element | my_id | coordinates=100,150 | # Use named argument syntax available in RF 2.5 and newer |
        """
        self._info("Clicking element '%s'." % locator)
        self._click(self._parse_locator(locator), dont_wait, coordinates)

    def double_click_element(self, locator, dont_wait='', coordinates=None):
        """Double click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.

        If you want to double click the element at certain coordinates, you can
        specify the position with `coordinates` argument in format `x,y`.

        See `Click Element` for usage examples.

        This keyword is new in SeleniumLibrary 2.7.
        """
        self._info("Double clicking element '%s'." % locator)
        self._double_click(self._parse_locator(locator), dont_wait, coordinates)

    def click_link(self, locator, dont_wait=''):
        """Clicks a link identified by locator.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.
        """
        self._info("Clicking link '%s'." % locator)
        try:
            self._click(self._parse_locator(locator, 'link'), dont_wait)
        except Exception, err:
            if not self._error_contains(err, 'not found'):
                raise
            self._click("link=%s" % locator, dont_wait)

    def click_button(self, locator, dont_wait=''):
        """Clicks a button identified by `locator`.

        Key attributes for buttons are `id`, `name` and `value`. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.
        """
        self._info("Clicking button '%s'." % locator)
        try:
            self._click(self._parse_locator(locator, 'input'), dont_wait)
        except Exception, err:
            if not self._error_contains(err, 'ERROR: Element xpath=//'):
                raise
            self._click(self._parse_locator(locator, 'button'), dont_wait)

    def click_image(self, locator, dont_wait=''):
        """Clicks an image found by `locator`.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements and about meaning
        of `dont_wait` argument.
        """
        self._info("Clicking image '%s'." % locator)
        try:
            self._click(self._parse_locator(locator, 'image'), dont_wait)
        except Exception, err:
            if not self._error_contains(err, 'ERROR: Element xpath=//'):
                raise
            # A form may have an image as it's submit trigger.
            self._click(self._parse_locator(locator, 'input'), dont_wait)

    def _click(self, locator, dont_wait='', coordinates=None):
        self._click_or_click_at(locator, self._selenium.click,
                                self._selenium.click_at, coordinates,
                                dont_wait)

    def _double_click(self, locator, dont_wait='', coordinates=None):
        self._click_or_click_at(locator, self._selenium.double_click,
                                self._selenium.double_click_at, coordinates,
                                dont_wait)

    def _click_or_click_at(self, locator, action, action_with_coordinates,
                           coordinates, dont_wait):
        if coordinates:
            self._info("Clicking at coordinates '%s'." % coordinates)
            action_with_coordinates(locator, coordinates)
        else:
            action(locator)
        if not dont_wait:
            self.wait_until_page_loaded()

    def submit_form(self, locator='', dont_wait=''):
        """Submits a form identified by `locator`.

        If `locator` is empty, first form in the page will be submitted.
        Key attributes for forms are `id` and `name`. See `introduction` for
        details about locating elements and about meaning of `dont_wait`
        argument.
        """
        self._info("Submitting form '%s'." % locator)
        if not locator:
            locator = 'xpath=//form'
        else:
            locator = self._parse_locator(locator)
        self._selenium.submit(locator)
        if not dont_wait:
            self.wait_until_page_loaded()
