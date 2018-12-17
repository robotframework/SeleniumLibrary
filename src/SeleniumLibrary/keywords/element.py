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

from robot.utils import plural_or_not
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys


from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import (is_falsy, is_noney, is_truthy,
                                   plural_or_not as s)
from SeleniumLibrary.errors import ElementNotFound


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
    def element_should_not_contain(self, locator, expected, message=None, ignore_case=False):
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
    def page_should_contain(self, text, loglevel='TRACE'):
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
                                    loglevel='TRACE', limit=None):
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
    def locator_should_match_x_times(self, locator, x, message=None, loglevel='TRACE'):
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
    def page_should_not_contain(self, text, loglevel='TRACE'):
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
    def page_should_not_contain_element(self, locator, message=None, loglevel='TRACE'):
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
    def cover_element(self, locator):
        """Will cover elements identified by ``locator`` with a blue div without breaking page layout.
        
        See the `Locating elements` section for details about the locator
        syntax.
        
        New in SeleniumLibrary 3.3.0
        
        Example:
        |`Cover Element` | css:div#container |
        """
        elements = self.find_elements(locator)
        if not elements:
            raise ElementNotFound("No element with locator '%s' found."
                                  % locator)
        for element in elements:
            script = """
old_element = arguments[0];
let newDiv = document.createElement('div');
newDiv.setAttribute("name", "covered");
newDiv.style.backgroundColor = 'blue';
newDiv.style.zIndex = '999';
newDiv.style.top = old_element.offsetTop + 'px';
newDiv.style.left = old_element.offsetLeft + 'px';
newDiv.style.height = old_element.offsetHeight + 'px';
newDiv.style.width = old_element.offsetWidth + 'px';
old_element.parentNode.insertBefore(newDiv, old_element);
old_element.remove();
newDiv.parentNode.style.overflow = 'hidden';
        """
            self.driver.execute_script(script, element)

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
    def click_button(self, locator, modifier=False):
        """Clicks button identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, buttons are
        searched using ``id``, ``name`` and ``value``.

        See the `Click Element` keyword for details about the
        ``modifier`` argument.

        The ``modifier`` argument is new in SeleniumLibrary 3.3
        """
        if is_falsy(modifier):
            self.info("Clicking button '%s'." % locator)
            element = self.find_element(locator, tag='input', required=False)
            if not element:
                element = self.find_element(locator, tag='button')
            element.click()
        else:
            self._click_with_modifier(locator, ['button', 'input'], modifier)

    @keyword
    def click_image(self, locator, modifier=False):
        """Clicks an image identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, images are searched
        using ``id``, ``name``, ``src`` and ``alt``.

        See the `Click Element` keyword for details about the
        ``modifier`` argument.

        The ``modifier`` argument is new in SeleniumLibrary 3.3
        """
        if is_falsy(modifier):
            self.info("Clicking image '%s'." % locator)
            element = self.find_element(locator, tag='image', required=False)
            if not element:
                # A form may have an image as it's submit trigger.
                element = self.find_element(locator, tag='input')
            element.click()
        else:
            self._click_with_modifier(locator, ['image', 'input'], modifier)

    @keyword
    def click_link(self, locator, modifier=False):
        """Clicks a link identified by ``locator``.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.

        See the `Click Element` keyword for details about the
        ``modifier`` argument.

        The ``modifier`` argument is new in SeleniumLibrary 3.3
        """
        if is_falsy(modifier):
            self.info("Clicking link '%s'." % locator)
            self.find_element(locator, tag='link').click()
        else:
            self._click_with_modifier(locator, ['link', 'link'], modifier)

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
            self._click_with_modifier(locator, [None, None], modifier)

    def _click_with_modifier(self, locator, tag, modifier):
        self.info("Clicking %s '%s' with %s." % (tag if tag[0] else 'element', locator, modifier))
        modifier = self.parse_modifier(modifier)
        action = ActionChains(self.driver)
        for item in modifier:
            action.key_down(item)
        element = self.find_element(locator, tag=tag[0], required=False)
        if not element:
            element = self.find_element(locator, tag=tag[1])
        action.click(element)
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
        """Deprecated use `Press Keys` instead."""
        if key.startswith('\\') and len(key) > 1:
            key = self._map_ascii_key_code_to_key(int(key[1:]))
        element = self.find_element(locator)
        element.send_keys(key)

    @keyword
    def press_keys(self, locator=None, *keys):
        """Simulates user pressing key(s) to an element or on the active browser.


        If ``locator`` evaluates as false, see `Boolean arguments` for more
        details, then the ``keys`` are sent to the currently active browser.
        Otherwise element is searched and ``keys`` are send to the element
        identified by the ``locator``. In later case, keyword fails if element
        is not found. See the `Locating elements` section for details about
        the locator syntax.

        ``keys`` arguments can contain one or many strings, but it can not
        be empty. ``keys`` can also be a combination of
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html|Selenium Keys]
        and strings or a single Selenium Key. If Selenium Key is combined
        with strings, Selenium key and strings must be separated by the
        `+` character, like in `CONTROL+c`. Selenium Keys
        are space and case sensitive and Selenium Keys are not parsed
        inside of the string. Example AALTO, would send string `AALTO`
        and `ALT` not parsed inside of the string. But `A+ALT+O` would
        found Selenium ALT key from the ``keys`` argument. It also possible
        to press many Selenium Keys down at the same time, example
        'ALT+ARROW_DOWN`.

        If Selenium Keys are detected in the ``keys`` argument, keyword
        will press the Selenium Key down, send the strings and
         then release the Selenium Key. If keyword needs to send a Selenium
        Key as a string, then each character must be separated with
        `+` character, example `E+N+D`.

        `CTRL` is alias for
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys.CONTROL|Selenium CONTROL]
        and ESC is alias for
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver/selenium.webdriver.common.keys.html#selenium.webdriver.common.keys.Keys.ESCAPE|Selenium ESCAPE]

        New in SeleniumLibrary 3.3

        Examples:
        | `Press Keys` | text_field | AAAAA          |            | # Sends string "AAAAA" to element.                                                |
        | `Press Keys` | None       | BBBBB          |            | # Sends string "BBBBB" to currently active browser.                               |
        | `Press Keys` | text_field | E+N+D          |            | # Sends string "END" to element.                                                  |
        | `Press Keys` | text_field | XXX            | YY         | # Sends strings "XXX" and "YY" to element.                                        |
        | `Press Keys` | text_field | XXX+YY         |            | # Same as above.                                                                  |
        | `Press Keys` | text_field | ALT+ARROW_DOWN |            | # Pressing "ALT" key down, then pressing ARROW_DOWN and then releasing both keys. |
        | `Press Keys` | text_field | ALT            | ARROW_DOWN | # Pressing "ALT" key and then pressing ARROW_DOWN.                                |
        | `Press Keys` | text_field | CTRL+c         |            | # Pressing CTRL key down, sends string "c" and then releases CTRL key.            |
        | `Press Keys` | button     | RETURN         |            | # Pressing "ENTER" key to element.                                                |
        """
        parsed_keys = self._parse_keys(*keys)
        if is_truthy(locator):
            self.info('Sending key(s) %s to %s element.' % (keys, locator))
        else:
            self.info('Sending key(s) %s to page.' % str(keys))
        self._press_keys(locator, parsed_keys)

    def _press_keys(self, locator, parsed_keys):
        if is_truthy(locator):
            element = self.find_element(locator)
        else:
            element = None
        for parsed_key in parsed_keys:
            actions = ActionChains(self.driver)
            special_keys = []
            for key in parsed_key:
                if self._selenium_keys_has_attr(key.original):
                    special_keys = self._press_keys_special_keys(actions, element, parsed_key,
                                                                 key, special_keys)
                else:
                    self._press_keys_normal_keys(actions, element, key)
            for special_key in special_keys:
                self.info('Releasing special key %s.' % special_key.original)
                actions.key_up(special_key.converted)
            actions.perform()

    def _press_keys_normal_keys(self, actions, element, key):
        self.info('Sending key%s %s' % (plural_or_not(key.converted), key.converted))
        if element:
            actions.send_keys_to_element(element, key.converted)
        else:
            actions.send_keys(key.converted)

    def _press_keys_special_keys(self, actions, element, parsed_key, key, special_keys):
        if len(parsed_key) == 1 and element:
            self.info('Pressing special key %s to element.' % key.original)
            actions.send_keys_to_element(element, key.converted)
        elif len(parsed_key) == 1 and not element:
            self.info('Pressing special key %s to browser.' % key.original)
            actions.send_keys(key.converted)
        else:
            self.info('Pressing special key %s down.' % key.original)
            actions.key_down(key.converted)
            special_keys.append(key)
        return special_keys

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
    def page_should_contain_link(self, locator, message=None, loglevel='TRACE'):
        """Verifies link identified by ``locator`` is found from current page.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.
        """
        self.assert_page_contains(locator, 'link', message, loglevel)

    @keyword
    def page_should_not_contain_link(self, locator, message=None, loglevel='TRACE'):
        """Verifies link identified by ``locator`` is not found from current page.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, links are searched
        using ``id``, ``name``, ``href`` and the link text.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.
        """
        self.assert_page_not_contains(locator, 'link', message, loglevel)

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
    def page_should_contain_image(self, locator, message=None, loglevel='TRACE'):
        """Verifies image identified by ``locator`` is found from current page.

        See the `Locating elements` section for details about the locator
        syntax. When using the default locator strategy, images are searched
        using ``id``, ``name``, ``src`` and ``alt``.

        See `Page Should Contain Element` for explanation about ``message``
        and ``loglevel`` arguments.
        """
        self.assert_page_contains(locator, 'image', message, loglevel)

    @keyword
    def page_should_not_contain_image(self, locator, message=None, loglevel='TRACE'):
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
    def xpath_should_match_x_times(self, xpath, x, message=None, loglevel='TRACE'):
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
            item = self._parse_aliases(item)
            if hasattr(Keys, item):
                keys.append(getattr(Keys, item))
            else:
                raise ValueError("'%s' modifier does not match to Selenium Keys"
                                 % item)
        return keys

    def _parse_keys(self, *keys):
        if not keys:
            raise AssertionError('"keys" argument can not be empty.')
        list_keys = []
        for key in keys:
            separate_keys = self._separate_key(key)
            separate_keys = self._convert_special_keys(separate_keys)
            list_keys.append(separate_keys)
        return list_keys

    def _parse_aliases(self, key):
        if key == 'CTRL':
            return 'CONTROL'
        if key == 'ESC':
            return 'ESCAPE'
        return key

    def _separate_key(self, key):
        one_key = ''
        list_keys = []
        for char in key:
            if char == '+' and one_key != '':
                list_keys.append(one_key)
                one_key = ''
            else:
                one_key += char
        if one_key:
            list_keys.append(one_key)
        return list_keys

    def _convert_special_keys(self, keys):
        KeysRecord = namedtuple('KeysRecord', 'converted, original')
        converted_keys = []
        for key in keys:
            key = self._parse_aliases(key)
            if self._selenium_keys_has_attr(key):
                converted_keys.append(KeysRecord(getattr(Keys, key), key))
            else:
                converted_keys.append(KeysRecord(key, key))
        return converted_keys

    def _selenium_keys_has_attr(self, key):
        try:
            return hasattr(Keys, key)
        except UnicodeError:  # To support Python 2 and non ascii characters.
            return False
