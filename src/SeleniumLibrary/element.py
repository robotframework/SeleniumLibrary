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


class Element(RunOnFailure):
    """Contains keywords for operating on arbitrary elements."""

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
        self._info("Verifying element '%s' contains exactly text '%s'."
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

    def get_element_attribute(self, attribute_locator):
        """Return value of element attribute.

        `attribute_locator` consists of element locator followed by an @ sign
        and attribute name, for example "element_id@class".
        """
        return self._selenium.get_attribute(attribute_locator)

    def get_value(self, locator):
        """Returns the value attribute of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._selenium.get_value(self._parse_locator(locator))

    def get_text(self, locator):
        """Returns the text of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._selenium.get_text(self._parse_locator(locator))

    def focus(self, locator):
        """Sets focus to element identified by `locator`.

        This is useful for instance to direct native keystrokes to particular
        element using `Press Key Native`.
        """
        self._selenium.focus(locator)

    def drag_and_drop(self, locator, movement):
        """Drags element identified with `locator` by `movement`

        `movement is a string in format "+70 -300" interpreted as pixels in
        relation to elements current position.
        """
        self._selenium.dragdrop(self._parse_locator(locator), movement)

    def press_key(self, locator, key, wait=''):
        """Simulates user pressing key on element identified by `locator`.

        `key` is either a single character, or a numerical ASCII code of the key
        lead by '\\'.

        See `introduction` for details about `wait` argument.

        Examples:
        | Press Key | text_field   | q |
        | Press Key | login_button | \\13 | # ASCII code for enter key |

        Sometimes this keyword does not trigger the correct JavaScript event
        on the clicked element. In those cases `Press Key Native` can be
        used as a workaround.

        The selenium command `key_press` [1] that this keyword used exposes some
        erratic behavior [2], especially when used with the Internet Explorer.
        If you do not get the expected results, try `Press Key Native` instead.

        [1] http://release.seleniumhq.org/selenium-remote-control/1.0-beta-2/doc/python/selenium.selenium-class.html#key_press
        [2] http://jira.openqa.org/browse/SRC-385
        """
        self._selenium.key_press(locator, key)
        if wait:
            self.wait_until_page_loaded()

    def press_key_native(self, keycode, wait=''):
        """Simulates user pressing key by sending an operating system keystroke.

        `keycode` corresponds to `java.awt.event.KeyEvent` constants, which can
        be found from
        http://java.sun.com/javase/6/docs/api/constant-values.html#java.awt.event.KeyEvent.CHAR_UNDEFINED

        The key press does not target a particular element. An element can be
        chosen by first using `Focus` keyword.

        See `introduction` for details about `wait` argument.

        Examples:
        | Press Key Native | 517          | # Exclamation mark |
        | Focus            | login_button |
        | Press Key Native | 10           | # Enter key  |

        Notice that this keyword is very fragile and, for example, using the
        keyboard or mouse while tests are running often causes problems. It can
        be beneficial to bring the window to the front again with executing JavaScript:

        | Execute Javascript | window.focus() |          |
        | Focus              | login_button   |          |
        | Press Key Native   | 10             | and wait |
        """
        self._selenium.key_press_native(keycode)
        if wait:
            self.wait_until_page_loaded()

    def get_horizontal_position(self, locator):
        """Returns horizontal position of element identified by `locator`.

        The position is returned in pixels off the left side of the page,
        as an integer. Fails if a matching element is not found.

        See also `Get Vertical Position`.
        """
        return self._get_position(self._selenium.get_element_position_left,
                                  locator)

    def get_vertical_position(self, locator):
        """Returns vertical position of element identified by `locator`.

        The position is returned in pixels off the top of the page,
        as an integer. Fails if a matching element is not found.

        See also `Get Horizontal Position`.
        """
        return self._get_position(self._selenium.get_element_position_top,
                                  locator)

    def _get_position(self, getter, locator):
        not_found = "Could not determine position for '%s'" % locator
        try:
            pos = getter(self._parse_locator(locator))
        except Exception, err:
            if not self._error_contains(err, 'not found'):
                raise
            raise RuntimeError(not_found)
        if not pos:
            raise RuntimeError(not_found)
        return int(pos)

    def simulate(self, locator, event):
        """Simulates `event` on element identified by `locator`.

        This keyword is useful if element has OnEvent handler that needs to be
        explicitly invoked.

        See `introduction` for details about locating elements.
        """
        self._selenium.fire_event(self._parse_locator(locator), event)

    def open_context_menu(self, locator, offset=None):
        """Opens context menu on element identified by `locator`."""
        locator = self._parse_locator(locator)
        if offset:
            self._selenium.context_menu_at(locator, offset)
        else:
            self._selenium.context_menu(locator)
