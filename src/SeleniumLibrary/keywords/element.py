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

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import (is_falsy, is_noney, is_truthy,
                                   plural_or_not as s)


class ElementKeywords(LibraryComponent):

    @keyword(name='Get WebElement')
    def get_webelement(self, locator):
        """Returns the first WebElement matching the given ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        return self.find_element(locator)

    @keyword(name='Get WebElements')
    def get_webelements(self, locator):
        """Returns list of WebElement objects matching the ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Starting from SeleniumLibrary 3.0, the keyword returns an empty
        list if there are no matching elements. In previous releases the
        keyword failed in this case.
        """
        return self.find_elements(locator)

    @keyword
    def element_should_contain(self, locator, expected, message=None, ignore_case=False):
        """Verifies that element ``locator`` contains text ``expected``.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``message`` argument can be used to override the default error
        message.

        The ``ignore_case`` argument can be set to True to compare case
        insensitive, default is False. New in SeleniumLibrary 3.1.

        ``ignore_case`` argument new in SeleniumLibrary 3.1.

        Use `Element Text Should Be` if you want to match the exact text,
        not a substring.
        """
        actual = actual_before = self.find_element(locator).text
        expected_before = expected
        if is_truthy(ignore_case):
            actual = actual.lower()
            expected = expected.lower()
        if expected not in actual:
            if is_noney(message):
                message = "Element '%s' should have contained text '%s' but "\
                          "its text was '%s'." % (locator, expected_before, actual_before)
            raise AssertionError(message)
        self.info("Element '%s' contains text '%s'." % (locator, expected_before))

    @keyword
    def element_should_not_contain(self, locator, expected, message=None, ignore_case=False ):
        """Verifies that element ``locator`` does not contains text ``expected``.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``message`` argument can be used to override the default error
        message.

        The ``ignore_case`` argument can be set to True to compare case
        insensitive, default is False.

        ``ignore_case`` argument new in SeleniumLibrary 3.1.
        """
        actual = self.find_element(locator).text
        expected_before = expected
        if is_truthy(ignore_case):
            actual = actual.lower()
            expected = expected.lower()
        if expected in actual:
            if is_noney(message):
                message = "Element '%s' should not contain text '%s' but " \
                          "it did." % (locator, expected_before)
            raise AssertionError(message)
        self.info("Element '%s' does not contain text '%s'."
                  % (locator, expected_before))

    @keyword
    def page_should_contain(self, text, loglevel='INFO'):
        """Verifies that current page contains ``text``.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional ``loglevel``
        argument. Valid log levels are ``DEBUG``, ``INFO`` (default),
        ``WARN``, and ``NONE``. If the log level is ``NONE`` or below
        the current active log level the source will not be logged.
        """
        if not self._page_contains(text):
            self.ctx.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not." % text)
        self.info("Current page contains text '%s'." % text)

    @keyword
    def page_should_contain_element(self, locator, message=None,
                                    loglevel='INFO', limit=None):
        """Verifies that element ``locator`` is found on the current page.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``message`` argument can be used to override the default error
        message.

        The ``limit`` argument can used to define how many elements the
        page should contain. When ``limit`` is ``None`` (default) page can
        contain one or more elements. When limit is a number, page must
        contain same number of elements.

        See `Page Should Contain` for explanation about the ``loglevel``
        argument.

        Examples assumes that locator matches to two elements.
        | `Page Should Contain Element` | div_name | limit=1    | # Keyword fails.                  |
        | `Page Should Contain Element` | div_name | limit=2    | # Keyword passes.                 |
        | `Page Should Contain Element` | div_name | limit=none | # None is considered one or more. |
        | `Page Should Contain Element` | div_name |            | # Same as above.                  |

        The ``limit`` argument is new in SeleniumLibrary 3.0.
        """
        if is_noney(limit):
            return self.assert_page_contains(locator, message=message,
                                             loglevel=loglevel)
        limit = int(limit)
        count = len(self.find_elements(locator))
        if count == limit:
            self.info('Current page contains {} element(s).'.format(count))
        else:
            if is_noney(message):
                message = ('Page should have contained "{}" element(s), '
                           'but it did contain "{}" element(s).'
                           .format(limit, count))
            self.ctx.log_source(loglevel)
            raise AssertionError(message)

    @keyword
    def locator_should_match_x_times(self, locator, x, message=None, loglevel='INFO'):
        """Deprecated, use `Page Should Contain Element` with ``limit`` argument instead."""
        count = len(self.find_elements(locator))
        x = int(x)
        if count != x:
            if is_falsy(message):
                message = ("Locator '%s' should have matched %s time%s but "
                           "matched %s time%s."
                           % (locator, x, s(x), count, s(count)))
            self.ctx.log_source(loglevel)
            raise AssertionError(message)
        self.info("Current page contains %s elements matching '%s'."
                  % (count, locator))

    @keyword
    def page_should_not_contain(self, text, loglevel='INFO'):
        """Verifies the current page does not contain ``text``.

        See `Page Should Contain` for explanation about the ``loglevel``
        argument.
        """
        if self._page_contains(text):
            self.ctx.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s'."
                                 % text)
        self.info("Current page does not contain text '%s'." % text)

    @keyword
    def page_should_not_contain_element(self, locator, message=None, loglevel='INFO'):
        """Verifies that element ``locator`` is found on the current page.

        See the `Locating elements` section for details about the locator
        syntax.

        See `Page Should Contain` for explanation about ``message`` and
        ``loglevel`` arguments.
        """
        self.assert_page_not_contains(locator, message=message,
                                      loglevel=loglevel)

    @keyword
    def assign_id_to_element(self, locator, id):
        """Assigns temporary ``id`` to element specified by ``locator``.

        This is mainly useful if the locator is complicated and/or slow XPath
        expression and it is needed multiple times. Identifier expires when
        the page is reloaded.

        See the `Locating elements` section for details about the locator
        syntax.

        Example:
        | `Assign ID to Element` | //ul[@class='example' and ./li[contains(., 'Stuff')]] | my id |
        | `Page Should Contain Element` | my id |
        """
        self.info("Assigning temporary id '%s' to element '%s'." % (id, locator))
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].id = '%s';" % id, element)

    @keyword
    def element_should_be_disabled(self, locator):
        """Verifies that element identified with ``locator`` is disabled.

        This keyword considers also elements that are read-only to be
        disabled.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if self.is_element_enabled(locator):
            raise AssertionError("Element '%s' is enabled." % locator)

    @keyword
    def element_should_be_enabled(self, locator):
        """Verifies that element identified with ``locator`` is enabled.

        This keyword considers also elements that are read-only to be
        disabled.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        if not self.is_element_enabled(locator):
            raise AssertionError("Element '%s' is disabled." % locator)

    @keyword
    def element_should_be_focused(self, locator):
        """Verifies that element identified with ``locator`` is focused.

        See the `Locating elements` section for details about the locator
        syntax.

        New in SeleniumLibrary 3.0.
        """
        element = self.find_element(locator)
        focused = self.driver.switch_to.active_element
        # Selenium 3.6.0 with Firefox return dict wich contains the selenium WebElement
        if isinstance(focused, dict):
            focused = focused['value']
        if element != focused:
            raise AssertionError("Element '%s' does not have focus." % locator)

    @keyword
    def element_should_be_visible(self, locator, message=None):
        """Verifies that the element identified by ``locator`` is visible.

        Herein, visible means that the element is logically visible, not
        optically visible in the current browser viewport. For example,
        an element that carries ``display:none`` is not logically visible,
        so using this keyword on that element would fail.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``message`` argument can be used to override the default error
        message.
        """
        if not self.find_element(locator).is_displayed():
            if is_noney(message):
                message = ("The element '%s' should be visible, but it "
                           "is not." % locator)
            raise AssertionError(message)
        self.info("Element '%s' is displayed." % locator)

    @keyword
    def element_should_not_be_visible(self, locator, message=None):
        """Verifies that the element identified by ``locator`` is NOT visible.

        Passes if element does not exists. See `Element Should Be Visible`
        for more information about visibility and supported arguments.
        """
        element = self.find_element(locator, required=False)
        if element is None:
            self.info("Element '%s' did not exist." % locator)
        elif not element.is_displayed():
            self.info("Element '%s' exists but is not displayed." % locator)
        else:
            if is_noney(message):
                message = ("The element '%s' should not be visible, "
                           "but it is." % locator)
            raise AssertionError(message)

    @keyword
    def element_text_should_be(self, locator, expected, message=None, ignore_case=False):
        """Verifies that element ``locator`` contains exact text ``expected``.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``message`` argument can be used to override the default error
        message.

        The ``ignore_case`` argument can be set to True to compare case
        insensitive, default is False.

        ``ignore_case`` argument new in SeleniumLibrary 3.1.

        Use `Element Should Contain` if a substring match is desired.
        """
        self.info("Verifying element '%s' contains exact text '%s'."
                  % (locator, expected))
        text = before_text = self.find_element(locator).text
        if is_truthy(ignore_case):
            text = text.lower()
            expected = expected.lower()
        if text != expected:
            if is_noney(message):
                message = ("The text of element '%s' should have been '%s' "
                           "but it was '%s'."
                           % (locator, expected, before_text))
            raise AssertionError(message)

    @keyword
    def element_text_should_not_be(self, locator, not_expected, message=None, ignore_case=False):
        """Verifies that element ``locator`` does not contain exact text ``not_expected``.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``message`` argument can be used to override the default error
        message.

        The ``ignore_case`` argument can be set to True to compare case
        insensitive, default is False.

        New in SeleniumLibrary 3.1.1
        """
        self.info("Verifying element '%s' does not contains exact text '%s'."
                  % (locator, not_expected))
        text = self.find_element(locator).text
        before_not_expected = not_expected
        if is_truthy(ignore_case):
            text = text.lower()
            not_expected = not_expected.lower()
        if text == not_expected:
            if is_noney(message):
                message = ("The text of element '%s' was not supposed to be '%s'."
                           % (locator, before_not_expected))
            raise AssertionError(message)

    @keyword
    def get_element_attribute(self, locator, attribute):
        """Returns value of ``attribute`` from element ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Example:
        | ${id}= | `Get Element Attribute` | css:h1 | id |

        Passing attribute name as part of the ``locator`` was removed
        in SeleniumLibrary 3.2. The explicit ``attribute`` argument
        should be used instead.
        """
        return self.find_element(locator).get_attribute(attribute)

    @keyword
    def element_attribute_value_should_be(self, locator, attribute, expected, message=None):
        """Verifies element identified by ``locator`` contains expected attribute value.

        See the `Locating elements` section for details about the locator
        syntax.

        Example:
        `Element Attribute Value Should Be` | css:img | href | value

        New in SeleniumLibrary 3.2.
        """
        current_expected = self.find_element(locator).get_attribute(attribute)
        if current_expected != expected:
            if is_noney(message):
                message = ("Element '%s' attribute should have value '%s' but "
                          "its value was '%s'." % (locator, expected, current_expected))
            raise AssertionError(message)
        self.info("Element '%s' attribute '%s' contains value '%s'." % (locator, attribute, expected))

    @keyword
    def get_horizontal_position(self, locator):
        """Returns horizontal position of element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        The position is returned in pixels off the left side of the page,
        as an integer.

        See also `Get Vertical Position`.
        """
        return self.find_element(locator).location['x']

    @keyword
    def get_element_size(self, locator):
        """Returns width and height of element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Both width and height are returned as integers.

        Example:
        | ${width} | ${height} = | `Get Element Size` | css:div#container |
        """
        element = self.find_element(locator)
        return element.size['width'], element.size['height']

    @keyword
    def get_value(self, locator):
        """Returns the value attribute of element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        return self.get_element_attribute(locator, 'value')

    @keyword
    def get_text(self, locator):
        """Returns the text value of element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        return self.find_element(locator).text

    @keyword
    def clear_element_text(self, locator):
        """Clears the value of text entry element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.find_element(locator).clear()

    @keyword
    def get_vertical_position(self, locator):
        """Returns vertical position of element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        The position is returned in pixels off the top of the page,
        as an integer.

        See also `Get Horizontal Position`.
        """
        return self.find_element(locator).location['y']

    @keyword
    def click_element(self, locator, modifier=False):
        """Click element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        The ``modifier`` argument can be used to pass
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys|Selenium Keys]
        when clicking the element. The `+` can be used as a separator
        for different Selenium Keys. The `CTRL` is internally translated to
        `CONTROL` key. The ``modifier`` is space and case insensitive, example
        "alt" and " aLt " are supported formats to
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys.ALT|ALT key]
        . If ``modifier`` does not match to Selenium Keys, keyword fails.

        Example:
        | Click Element | id:button | | # Would click element without any modifiers. |
        | Click Element | id:button | CTRL | # Would click element with CTLR key pressed down. |
        | Click Element | id:button | CTRL+ALT | # Would click element with CTLR and ALT keys pressed down. |

        The ``modifier`` argument is new in SeleniumLibrary 3.2
        """
        if is_falsy(modifier):
            self.info("Clicking element '%s'." % locator)
            self.find_element(locator).click()
        else:
            modifier = self.parse_modifier(modifier)
            action = ActionChains(self.driver)
            for item in modifier:
                action.key_down(item)
            action.click(self.find_element(locator))
            for item in modifier:
                action.key_up(item)
            action.perform()

    @keyword
    def click_element_at_coordinates(self, locator, xoffset, yoffset):
        """Click element ``locator`` at ``xoffset/yoffset``.

        Cursor is moved and the center of the element and x/y coordinates are
        calculated from that point.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Clicking element '%s' at coordinates x=%s, y=%s."
                  % (locator, xoffset, yoffset))
        element = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(element)
        action.move_by_offset(xoffset, yoffset)
        action.click()
        action.perform()

    @keyword
    def double_click_element(self, locator):
        """Double click element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Double clicking element '%s'." % locator)
        element = self.find_element(locator)
        action = ActionChains(self.driver)
        action.double_click(element).perform()

    @keyword
    def set_focus_to_element(self, locator):
        """Sets focus to element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        Prior to SeleniumLibrary 3.0 this keyword was named `Focus`.
        """
        element = self.find_element(locator)
        self.driver.execute_script("arguments[0].focus();", element)

    @keyword
    def focus(self, locator):
        """*DEPRECATED in SeleniumLibrary 3.2.* Use `Set Focus To Element` instead."""
        self.set_focus_to_element(locator)

    @keyword
    def scroll_element_into_view(self, locator):
        """Scrolls an element identified by ``locator`` into view.

        See the `Locating elements` section for details about the locator
        syntax.

        New in SeleniumLibrary 3.2.0
        """
        element = self.find_element(locator)
        ActionChains(self.driver).move_to_element(element).perform()

    @keyword
    def drag_and_drop(self, locator, target):
        """Drags element identified by ``locator`` into ``target`` element.

        The ``locator`` argument is the locator of the dragged element
        and the ``target`` is the locator of the target. See the
        `Locating elements` section for details about the locator syntax.

        Example:
        | `Drag And Drop` | css:div#element | css:div.target |
        """
        element = self.find_element(locator)
        target = self.find_element(target)
        action = ActionChains(self.driver)
        action.drag_and_drop(element, target).perform()

    @keyword
    def drag_and_drop_by_offset(self, locator, xoffset, yoffset):
        """Drags element identified with ``locator`` by ``xoffset/yoffset``.

        See the `Locating elements` section for details about the locator
        syntax.

        Element will be moved by ``xoffset`` and ``yoffset``, each of which
        is a negative or positive number specifying the offset.

        Example:
        | `Drag And Drop By Offset` | myElem | 50 | -35 | # Move myElem 50px right and 35px down |
        """
        element = self.find_element(locator)
        action = ActionChains(self.driver)
        action.drag_and_drop_by_offset(element, int(xoffset), int(yoffset))
        action.perform()

    @keyword
    def mouse_down(self, locator):
        """Simulates pressing the left mouse button on the element ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        The element is pressed without releasing the mouse button.

        See also the more specific keywords `Mouse Down On Image` and
        `Mouse Down On Link`.
        """
        self.info("Simulating Mouse Down on element '%s'." % locator)
        element = self.find_element(locator)
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()

    @keyword
    def mouse_out(self, locator):
        """Simulates moving mouse away from the element ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Simulating Mouse Out on element '%s'." % locator)
        element = self.find_element(locator)
        size = element.size
        offsetx = (size['width'] / 2) + 1
        offsety = (size['height'] / 2) + 1
        action = ActionChains(self.driver)
        action.move_to_element(element).move_by_offset(offsetx, offsety)
        action.perform()

    @keyword
    def mouse_over(self, locator):
        """Simulates hovering mouse over the element ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Simulating Mouse Over on element '%s'." % locator)
        element = self.find_element(locator)
        action = ActionChains(self.driver)
        action.move_to_element(element).perform()

    @keyword
    def mouse_up(self, locator):
        """Simulates releasing the left mouse button on the element ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.
        """
        self.info("Simulating Mouse Up on element '%s'." % locator)
        element = self.find_element(locator)
        ActionChains(self.driver).release(element).perform()

    @keyword
    def open_context_menu(self, locator):
        """Opens context menu on element identified by ``locator``."""
        element = self.find_element(locator)
        action = ActionChains(self.driver)
        action.context_click(element).perform()

    @keyword
    def simulate_event(self, locator, event):
        """Simulates ``event`` on element identified by ``locator``.

        This keyword is useful if element has ``OnEvent`` handler that
        needs to be explicitly invoked.

        See the `Locating elements` section for details about the locator
        syntax.

        Prior to SeleniumLibrary 3.0 this keyword was named `Simulate`.
        """
        element = self.find_element(locator)
        script = """
element = arguments[0];
eventName = arguments[1];
if (document.createEventObject) { // IE
    return element.fireEvent('on' + eventName, document.createEventObject());
}
var evt = document.createEvent("HTMLEvents");
evt.initEvent(eventName, true, true);
return !element.dispatchEvent(evt);
        """
        self.driver.execute_script(script, element, event)

    @keyword
    def simulate(self, locator, event):
        """*DEPRECATED in SeleniumLibrary 3.2.* Use `Simulate Event` instead."""
        self.simulate_event(locator, event)

    @keyword
    def press_key(self, locator, key):
        r"""Simulates user pressing key on element identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax.

        ``key`` is either a single character, a string, or a numerical ASCII
        code of the key lead by '\\'.

        Examples:
        | `Press Key` | text_field   | q     |
        | `Press Key` | text_field   | abcde |
        | `Press Key` | login_button | \\13  | # ASCII code for enter key |
        """
        if key.startswith('\\') and len(key) > 1:
            key = self._map_ascii_key_code_to_key(int(key[1:]))
        element = self.find_element(locator)
        element.send_keys(key)

    @keyword
    def click_link(self, locator):
        """Clicks a link identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.
        """
        self.info("Clicking link '%s'." % locator)
        self.find_element(locator, tag='link').click()

    @keyword
    def get_all_links(self):
        """Returns a list containing ids of all links found in current page.

        If a link has no id, an empty string will be in the list instead.
        """
        links = self.find_elements("tag=a")
        return [link.get_attribute('id') for link in links]

    @keyword
    def mouse_down_on_link(self, locator):
        """Simulates a mouse down event on a link identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.
        """
        element = self.find_element(locator, tag='link')
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()

    @keyword
    def page_should_contain_link(self, locator, message=None, loglevel='INFO'):
        """Verifies link identified by ``locator`` is found from current page.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.
        """
        self.assert_page_contains(locator, 'link', message, loglevel)

    @keyword
    def page_should_not_contain_link(self, locator, message=None, loglevel='INFO'):
        """Verifies link identified by ``locator`` is not found from current page.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.
        """
        self.assert_page_not_contains(locator, 'link', message, loglevel)

    @keyword
    def click_image(self, locator):
        """Clicks an image identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, images are searched
        using ``id``, ``name``, ``src`` and ``alt``.
        """
        self.info("Clicking image '%s'." % locator)
        element = self.find_element(locator, tag='image', required=False)
        if not element:
            # A form may have an image as it's submit trigger.
            element = self.find_element(locator, tag='input')
        element.click()

    @keyword
    def mouse_down_on_image(self, locator):
        """Simulates a mouse down event on an image identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, images are searched
        using ``id``, ``name``, ``src`` and ``alt``.
        """
        element = self.find_element(locator, tag='image')
        action = ActionChains(self.driver)
        action.click_and_hold(element).perform()

    @keyword
    def page_should_contain_image(self, locator, message=None, loglevel='INFO'):
        """Verifies image identified by ``locator`` is found from current page.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, images are searched
        using ``id``, ``name``, ``src`` and ``alt``.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.
        """
        self.assert_page_contains(locator, 'image', message, loglevel)

    @keyword
    def page_should_not_contain_image(self, locator, message=None, loglevel='INFO'):
        """Verifies image identified by ``locator`` is found from current page.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, images are searched
        using ``id``, ``name``, ``src`` and ``alt``.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.
        """
        self.assert_page_not_contains(locator, 'image', message, loglevel)

    @keyword
    def get_matching_xpath_count(self, xpath, return_str=True):
        """*DEPRECATED in SeleniumLibrary 3.2.* Use `Get Element Count` instead."""
        count = self.get_element_count('xpath:' + xpath)
        return str(count) if is_truthy(return_str) else count

    @keyword
    def xpath_should_match_x_times(self, xpath, x, message=None, loglevel='INFO'):
        """*DEPRECATED in SeleniumLibrary 3.2.* Use `Page Should Contain Element` with ``limit`` argument instead."""
        self.locator_should_match_x_times('xpath:'+xpath, x, message, loglevel)

    @keyword
    def get_element_count(self, locator):
        """Returns number of elements matching ``locator``.

        If you wish to assert the number of matching elements, use
        `Page Should Contain Element` with ``limit`` argument. Keyword will
        always return an integer.

        Example:
        | ${count} =       | `Get Element Count` | name:div_name  |
        | `Should Be True` | ${count} > 2        |                |

        New in SeleniumLibrary 3.0.
        """
        return len(self.find_elements(locator))

    @keyword
    def add_location_strategy(self, strategy_name, strategy_keyword, persist=False):
        """Adds a custom location strategy.

        See `Custom locators` for information how to create and use
        custom strategies. `Remove Location Strategy` can be used to
        remove a registered strategy.

        Location strategies are automatically removed after leaving the
        current scope by default. Setting ``persist`` to a true value (see
        `Boolean arguments`) will cause the location strategy to stay
        registered throughout the life of the test.
        """
        self.element_finder.register(strategy_name, strategy_keyword, persist)

    @keyword
    def remove_location_strategy(self, strategy_name):
        """Removes a previously added custom location strategy.

        See `Custom locators` for information how to create and use
        custom strategies.
        """
        self.element_finder.unregister(strategy_name)

    def _map_ascii_key_code_to_key(self, key_code):
        map = {
            0: Keys.NULL,
            8: Keys.BACK_SPACE,
            9: Keys.TAB,
            10: Keys.RETURN,
            13: Keys.ENTER,
            24: Keys.CANCEL,
            27: Keys.ESCAPE,
            32: Keys.SPACE,
            42: Keys.MULTIPLY,
            43: Keys.ADD,
            44: Keys.SEPARATOR,
            45: Keys.SUBTRACT,
            56: Keys.DECIMAL,
            57: Keys.DIVIDE,
            59: Keys.SEMICOLON,
            61: Keys.EQUALS,
            127: Keys.DELETE
        }
        key = map.get(key_code)
        if key is None:
            key = chr(key_code)
        return key

    def _map_named_key_code_to_special_key(self, key_name):
        try:
            return getattr(Keys, key_name)
        except AttributeError:
            message = "Unknown key named '%s'." % (key_name)
            self.debug(message)
            raise ValueError(message)

    def _page_contains(self, text):
        self.driver.switch_to.default_content()

        if self.is_text_present(text):
            return True

        subframes = self.find_elements("xpath://frame|//iframe")
        self.debug('Current frame has %d subframes.' % len(subframes))
        for frame in subframes:
            self.driver.switch_to.frame(frame)
            found_text = self.is_text_present(text)
            self.driver.switch_to.default_content()
            if found_text:
                return True
        return False

    def parse_modifier(self, modifier):
        modifier = modifier.upper()
        modifiers = modifier.split('+')
        keys = []
        for item in modifiers:
            item = item.strip()
            if item == 'CTRL':
                item = 'CONTROL'
            if hasattr(Keys, item):
                keys.append(getattr(Keys, item))
            else:
                raise ValueError("'%s' modifier does not match to Selenium Keys"
                                 % item)
        return keys
