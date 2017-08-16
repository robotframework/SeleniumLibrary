from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys

from Selenium2Library.base import LibraryComponent, keyword
from Selenium2Library.keywords.formelement import FormElementKeywords
from Selenium2Library.utils import escape_xpath_value
from Selenium2Library.utils import is_truthy, is_falsy


class ElementKeywords(LibraryComponent):

    def __init__(self, ctx):
        LibraryComponent.__init__(self, ctx)
        self.form_element = FormElementKeywords(ctx)

    @keyword
    def get_webelement(self, locator):
        """Returns the first WebElement matching the given locator.

        See `introduction` for details about locating elements.
        """
        return self.find_element(locator)

    @keyword
    def get_webelements(self, locator):
        """Returns list of WebElement objects matching locator.

        See `introduction` for details about locating elements.
        """
        return self.find_element(locator, first_only=False)

    @keyword
    def current_frame_contains(self, text, loglevel='INFO'):
        """Verifies that current frame contains `text`.

        See `Page Should Contain ` for explanation about `loglevel` argument.
        """
        if not self.is_text_present(text):
            self.ctx.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self.info("Current page contains text '%s'." % text)

    @keyword
    def current_frame_should_not_contain(self, text, loglevel='INFO'):
        """Verifies that current frame contains `text`.

        See `Page Should Contain ` for explanation about `loglevel` argument.
        """
        if self.is_text_present(text):
            self.ctx.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s' "
                                 "but it did" % text)
        self.info("Current page should not contain text '%s'." % text)

    @keyword
    def element_should_contain(self, locator, expected, message=''):
        """Verifies element identified by `locator` contains text `expected`.

        If you wish to assert an exact (not a substring) match on the text
        of the element, use `Element Text Should Be`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Verifying element '%s' contains "
                  "text '%s'." % (locator, expected))
        actual = self._get_text(locator)
        if expected not in actual:
            if is_falsy(message):
                message = "Element '%s' should have contained text '%s' but "\
                          "its text was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    @keyword
    def element_should_not_contain(self, locator, expected, message=''):
        """Verifies element identified by `locator` does not contain text `expected`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `Element Should Contain` for more details.
        """
        self.info("Verifying element '%s' does not contain text '%s'."
                  % (locator, expected))
        actual = self._get_text(locator)
        if expected in actual:
            if is_falsy(message):
                message = "Element '%s' should not contain text '%s' but " \
                          "it did." % (locator, expected)
            raise AssertionError(message)

    @keyword
    def frame_should_contain(self, locator, text, loglevel='INFO'):
        """Verifies frame identified by `locator` contains `text`.

        See `Page Should Contain ` for explanation about `loglevel` argument.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        """
        if not self._frame_contains(locator, text):
            self.ctx.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self.info("Current page contains text '%s'." % text)

    @keyword
    def page_should_contain(self, text, loglevel='INFO'):
        """Verifies that current page contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Valid log levels are DEBUG, INFO (default), WARN, and NONE. If the
        log level is NONE or below the current active log level the source
        will not be logged.
        """
        if not self._page_contains(text):
            self.ctx.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self.info("Current page contains text '%s'." % text)

    @keyword
    def page_should_contain_element(self, locator, message='', loglevel='INFO'):
        """Verifies element identified by `locator` is found on the current page.

        `message` can be used to override default error message.

        See `Page Should Contain` for explanation about `loglevel` argument.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.assert_page_contains(locator, message=message, loglevel=loglevel)

    @keyword
    def locator_should_match_x_times(self, locator, expected_locator_count, message='', loglevel='INFO'):
        """Verifies that the page contains the given number of elements located by the given `locator`.

        See `introduction` for details about locating elements.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.
        """
        actual_locator_count = len(self.find_element(
            locator, first_only=False, required=False)
        )
        if int(actual_locator_count) != int(expected_locator_count):
            if is_falsy(message):
                message = "Locator %s should have matched %s times but matched %s times"\
                            %(locator, expected_locator_count, actual_locator_count)
            self.ctx.log_source(loglevel)
            raise AssertionError(message)
        self.info("Current page contains %s elements matching '%s'."
                  % (actual_locator_count, locator))

    @keyword
    def page_should_not_contain(self, text, loglevel='INFO'):
        """Verifies the current page does not contain `text`.

        See `Page Should Contain ` for explanation about `loglevel` argument.
        """
        if self._page_contains(text):
            self.ctx.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s'" % text)
        self.info("Current page does not contain text '%s'." % text)

    @keyword
    def page_should_not_contain_element(self, locator, message='', loglevel='INFO'):
        """Verifies element identified by `locator` is not found on the current page.

        `message` can be used to override the default error message.

        See `Page Should Contain ` for explanation about `loglevel` argument.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.assert_page_not_contains(locator, message=message,
                                      loglevel=loglevel)

    @keyword
    def assign_id_to_element(self, locator, id):
        """Assigns a temporary identifier to element specified by `locator`.

        This is mainly useful if the locator is complicated/slow XPath expression.
        Identifier expires when the page is reloaded.

        Example:
        | Assign ID to Element | xpath=//div[@id="first_div"] | my id |
        | Page Should Contain Element | my id |
        """
        self.info("Assigning temporary id '%s' to element '%s'" % (id, locator))
        element = self.find_element(locator)
        self.browser.execute_script("arguments[0].id = '%s';" % id, element)

    @keyword
    def element_should_be_disabled(self, locator):
        """Verifies that element identified with `locator` is disabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if self._is_enabled(locator):
            raise AssertionError("Element '%s' is enabled." % (locator))

    @keyword
    def element_should_be_enabled(self, locator):
        """Verifies that element identified with `locator` is enabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if not self._is_enabled(locator):
            raise AssertionError("Element '%s' is disabled." % (locator))

    @keyword
    def element_should_be_focused(self, locator):
        """Verifies that element identified with `locator` is focused.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        New in SeleniumLibrary 3.0.0.
        """
        element = self.find_element(locator)
        if self.browser.capabilities['browserName'] != "firefox":
            focused = self.browser.switch_to.active_element
        else:
            focused = self.browser.execute_script('return document.activeElement;')
        if element != focused:
            raise AssertionError("Element '%s' is not with focus." % (locator))

    @keyword
    def element_should_be_visible(self, locator, message=''):
        """Verifies that the element identified by `locator` is visible.

        Herein, visible means that the element is logically visible, not optically
        visible in the current browser viewport. For example, an element that carries
        display:none is not logically visible, so using this keyword on that element
        would fail.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Verifying element '%s' is visible." % locator)
        visible = self.is_visible(locator)
        if not visible:
            if is_falsy(message):
                message = ("The element '%s' should be visible, but it "
                           "is not." % locator)
            raise AssertionError(message)

    @keyword
    def element_should_not_be_visible(self, locator, message=''):
        """Verifies that the element identified by `locator` is NOT visible.

        This is the opposite of `Element Should Be Visible`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Verifying element '%s' is not visible." % locator)
        visible = self.is_visible(locator)
        if visible:
            if is_falsy(message):
                message = ("The element '%s' should not be visible, "
                           "but it is." % locator)
            raise AssertionError(message)

    @keyword
    def element_text_should_be(self, locator, expected, message=''):
        """Verifies element identified by `locator` exactly contains text `expected`.

        In contrast to `Element Should Contain`, this keyword does not try
        a substring match but an exact match on the element identified by `locator`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Verifying element '%s' contains exactly text '%s'."
                  % (locator, expected))
        element = self.find_element(locator)
        actual = element.text
        if expected != actual:
            if is_falsy(message):
                message = ("The text of element '%s' should have been '%s' "
                           "but in fact it was '%s'."
                           % (locator, expected, actual))
            raise AssertionError(message)

    @keyword
    def get_element_attribute(self, locator, attribute_name=None):
        """Returns value of the element attribute.

        There are two cases how to use this keyword.

        First, if only `locator` is provided, `locator` should consists of
        element locator followed by an @ sign and attribute name.
        This behavior is left for backward compatibility.

        Example:
        | ${id}= | Get Element Attribute | link=Link with id@id |

        Second, if `locator` and `attribute_name` are provided both, `locator`
        should be standard locator and `attribute_name` is name of the
        requested element attribute.

        Examples:
        | ${id}= | Get Element Attribute | link=Link with id | id |
        | ${element_by_dom}= | Get Webelement | dom=document.getElementsByTagName('a')[3] |
        | ${id}= | Get Element Attribute | ${element_by_dom} | id |
        """
        if is_falsy(attribute_name):
            locator, attribute_name = self._parse_attribute_locator(locator)
        element = self.find_element(locator, required=False)
        if not element:
            raise ValueError("Element '%s' not found." % (locator))
        return element.get_attribute(attribute_name)

    @keyword
    def get_horizontal_position(self, locator):
        """Returns horizontal position of element identified by `locator`.

        The position is returned in pixels off the left side of the page,
        as an integer. Fails if a matching element is not found.

        See also `Get Vertical Position`.
        """
        element = self.find_element(locator, required=False)
        if not element:
            raise AssertionError("Could not determine position for '%s'"
                                 % locator)
        return element.location['x']

    @keyword
    def get_element_size(self, locator):
        """Returns width and height of element identified by `locator`.

        The element width and height is returned.
        Fails if a matching element is not found.
        """
        element = self.find_element(locator)
        return element.size['width'], element.size['height']

    @keyword
    def get_value(self, locator):
        """Returns the value attribute of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self.ctx.element_finder.get_value(locator)

    @keyword
    def get_text(self, locator):
        """Returns the text value of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._get_text(locator)

    @keyword
    def clear_element_text(self, locator):
        """Clears the text value of text entry element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        element = self.find_element(locator)
        element.clear()

    @keyword
    def get_vertical_position(self, locator):
        """Returns vertical position of element identified by `locator`.

        The position is returned in pixels off the top of the page,
        as an integer. Fails if a matching element is not found.

        See also `Get Horizontal Position`.
        """
        element = self.find_element(locator, required=False)
        if element is None:
            raise AssertionError("Could not determine position for '%s'"
                                 % locator)
        return element.location['y']

    @keyword
    def click_element(self, locator):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Clicking element '%s'." % locator)
        self.find_element(locator).click()

    @keyword
    def click_element_at_coordinates(self, locator, xoffset, yoffset):
        """Click element identified by `locator` at x/y coordinates of the element.
        Cursor is moved and the center of the element and x/y coordinates are
        calculted from that point.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Click clicking element '%s' in coordinates "
                  "'%s', '%s'." % (locator, xoffset, yoffset))
        element = self.find_element(locator)
        action = ActionChains(self.browser)
        action.move_to_element(element)
        action.move_by_offset(xoffset, yoffset)
        action.click()
        action.perform()

    @keyword
    def double_click_element(self, locator):
        """Double click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Double clicking element '%s'." % locator)
        element = self.find_element(locator)
        action = ActionChains(self.browser)
        action.double_click(element).perform()

    @keyword
    def focus(self, locator):
        """Sets focus to element identified by `locator`."""
        element = self.find_element(locator)
        self.browser.execute_script("arguments[0].focus();", element)

    @keyword
    def drag_and_drop(self, source, target):
        """Drags element identified with `source` which is a locator.

        Element can be moved on top of another element with `target`
        argument.

        `target` is a locator of the element where the dragged object is
        dropped.

        Examples:
        | Drag And Drop | elem1 | elem2 | # Move elem1 over elem2. |
        """
        src_elem = self.find_element(source)
        trg_elem = self.find_element(target)
        action = ActionChains(self.browser)
        action.drag_and_drop(src_elem, trg_elem).perform()

    @keyword
    def drag_and_drop_by_offset(self, source, xoffset, yoffset):
        """Drags element identified with `source` which is a locator.

        Element will be moved by xoffset and yoffset, each of which is a
        negative or positive number specify the offset.

        Examples:
        | Drag And Drop By Offset | myElem | 50 | -35 | # Move myElem 50px right and 35px down. |
        """
        src_elem = self.find_element(source)
        action = ActionChains(self.browser)
        action.drag_and_drop_by_offset(src_elem, xoffset, yoffset)
        action.perform()

    @keyword
    def mouse_down(self, locator):
        """Simulates pressing the left mouse button on the element specified by `locator`.

        The element is pressed without releasing the mouse button.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        See also the more specific keywords `Mouse Down On Image` and
        `Mouse Down On Link`.
        """
        self.info("Simulating Mouse Down on element '%s'" % locator)
        element = self.find_element(locator, required=False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        action = ActionChains(self.browser)
        action.click_and_hold(element).perform()

    @keyword
    def mouse_out(self, locator):
        """Simulates moving mouse away from the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Simulating Mouse Out on element '%s'" % locator)
        element = self.find_element(locator, required=False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        size = element.size
        offsetx = (size['width'] / 2) + 1
        offsety = (size['height'] / 2) + 1
        action = ActionChains(self.browser)
        action.move_to_element(element).move_by_offset(offsetx, offsety)
        action.perform()

    @keyword
    def mouse_over(self, locator):
        """Simulates hovering mouse over the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Simulating Mouse Over on element '%s'" % locator)
        element = self.find_element(locator, required=False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        action = ActionChains(self.browser)
        action.move_to_element(element).perform()

    @keyword
    def mouse_up(self, locator):
        """Simulates releasing the left mouse button on the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self.info("Simulating Mouse Up on element '%s'" % locator)
        element = self.find_element(locator, required=False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        ActionChains(self.browser).release(element).perform()

    @keyword
    def open_context_menu(self, locator):
        """Opens context menu on element identified by `locator`."""
        element = self.find_element(locator)
        action = ActionChains(self.browser)
        action.context_click(element).perform()

    @keyword
    def simulate(self, locator, event):
        """Simulates `event` on element identified by `locator`.

        This keyword is useful if element has OnEvent handler that needs to be
        explicitly invoked.

        See `introduction` for details about locating elements.
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
        self.browser.execute_script(script, element, event)

    @keyword
    def press_key(self, locator, key):
        """Simulates user pressing key on element identified by `locator`.
        `key` is either a single character, a string, or a numerical ASCII code of the key
        lead by '\\\\'.
        Examples:
        | Press Key | text_field   | q |
        | Press Key | text_field   | abcde |
        | Press Key | login_button | \\\\13 | # ASCII code for enter key |
        """
        if key.startswith('\\') and len(key) > 1:
            key = self._map_ascii_key_code_to_key(int(key[1:]))
        element = self.find_element(locator)
        element.send_keys(key)

    @keyword
    def click_link(self, locator):
        """Clicks a link identified by locator.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self.info("Clicking link '%s'." % locator)
        link = self.find_element(locator, tag='a')
        link.click()

    @keyword
    def get_all_links(self):
        """Returns a list containing ids of all links found in current page.

        If a link has no id, an empty string will be in the list instead.
        """
        links = []
        elements = self.find_element("tag=a", tag='a', first_only=False,
                                     required=False)
        for anchor in elements:
            links.append(anchor.get_attribute('id'))
        return links

    @keyword
    def mouse_down_on_link(self, locator):
        """Simulates a mouse down event on a link.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        element = self.find_element(locator, tag='link')
        action = ActionChains(self.browser)
        action.click_and_hold(element).perform()

    @keyword
    def page_should_contain_link(self, locator, message='', loglevel='INFO'):
        """Verifies link identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self.assert_page_contains(locator, 'link', message, loglevel)

    @keyword
    def page_should_not_contain_link(self, locator, message='', loglevel='INFO'):
        """Verifies image identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self.assert_page_not_contains(locator, 'link', message, loglevel)

    @keyword
    def click_image(self, locator):
        """Clicks an image found by `locator`.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self.info("Clicking image '%s'." % locator)
        element = self.find_element(locator, tag='image', required=False)
        if not element:
            # A form may have an image as it's submit trigger.
            element = self.find_element(locator, tag='input')
        element.click()

    @keyword
    def mouse_down_on_image(self, locator):
        """Simulates a mouse down event on an image.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        element = self.find_element(locator, tag='image')
        action = ActionChains(self.browser)
        action.click_and_hold(element).perform()

    @keyword
    def page_should_contain_image(self, locator, message='', loglevel='INFO'):
        """Verifies image identified by `locator` is found from current page.
        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self.assert_page_contains(locator, 'image', message, loglevel)

    @keyword
    def page_should_not_contain_image(self, locator, message='', loglevel='INFO'):
        """Verifies image identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self.assert_page_not_contains(locator, 'image', message, loglevel)

    @keyword
    def get_matching_xpath_count(self, xpath, return_str=True):
        """Returns number of elements matching `xpath`

        The default return type is `str` but it can changed to `int` by setting
        the ``return_str`` argument to Python False.

        One should not use the xpath= prefix for 'xpath'. XPath is assumed.

        Correct:
        | count = | Get Matching Xpath Count | //div[@id='sales-pop']
        Incorrect:
        | count = | Get Matching Xpath Count | xpath=//div[@id='sales-pop']

        If you wish to assert the number of matching elements, use
        `Xpath Should Match X Times`.
        """
        count = len(self.find_element("xpath=" + xpath, first_only=False,
                                      required=False))
        return str(count) if is_truthy(return_str) else count

    @keyword
    def xpath_should_match_x_times(self, xpath, expected_xpath_count, message='', loglevel='INFO'):
        """Verifies that the page contains the given number of elements located by the given `xpath`.

        One should not use the xpath= prefix for 'xpath'. XPath is assumed.

        Correct:
        | Xpath Should Match X Times | //div[@id='sales-pop'] | 1
        Incorrect:
        | Xpath Should Match X Times | xpath=//div[@id='sales-pop'] | 1

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.
        """
        actual_xpath_count = len(self.find_element(
            "xpath=" + xpath, first_only=False, required=False))
        if int(actual_xpath_count) != int(expected_xpath_count):
            if is_falsy(message):
                message = ("Xpath %s should have matched %s times but "
                           "matched %s times"
                           % (xpath, expected_xpath_count, actual_xpath_count))
            self.ctx.log_source(loglevel)
            raise AssertionError(message)
        self.info("Current page contains %s elements matching '%s'."
                  % (actual_xpath_count, xpath))

    @keyword
    def add_location_strategy(self, strategy_name, strategy_keyword, persist=False):
        """Adds a custom location strategy based on a keyword.

        Location strategies are automatically removed after leaving the current
        scope by default. Setting `persist` to Python True will cause the
        location strategy to stay registered throughout the life of the test.

        Trying to add a custom location strategy with the same name as one that
        already exists will cause the keyword to fail.

        Custom locator keyword example:
        | Custom Locator Strategy |
        |   | [Arguments] | ${browser} | ${criteria} | ${tag} | ${constraints} |
        |   | ${retVal}= | Execute Javascript | return window.document.getElementById('${criteria}'); |
        |   | [Return] | ${retVal} |

        Usage example:
        | Add Location Strategy | custom | Custom Locator Strategy |
        | Page Should Contain Element | custom=my_id |

        See `Remove Location Strategy` for details about removing a custom
        location strategy.
        """
        self.element_finder.register(strategy_name, strategy_keyword, persist)

    @keyword
    def remove_location_strategy(self, strategy_name):
        """Removes a previously added custom location strategy.

        Will fail if a default strategy is specified.

        See `Add Location Strategy` for details about adding a custom location strategy.
        """
        self.element_finder.unregister(strategy_name)

    def _frame_contains(self, locator, text):
        element = self.find_element(locator)
        self.browser.switch_to.frame(element)
        self.info("Searching for text from frame '%s'." % locator)
        found = self.is_text_present(text)
        self.browser.switch_to.default_content()
        return found

    def _get_text(self, locator):
        element = self.find_element(locator)
        if element is not None:
            return element.text
        return None

    def _is_enabled(self, locator):
        element = self.find_element(locator)
        if not self.form_element._is_form_element(element):
            raise AssertionError("ERROR: Element %s is not an input." % locator)
        if not element.is_enabled():
            return False
        read_only = element.get_attribute('readonly')
        if read_only == 'readonly' or read_only == 'true':
            return False
        return True

    def is_text_present(self, text):
        locator = "xpath=//*[contains(., %s)]" % escape_xpath_value(text)
        return self.find_element(locator, required=False)

    def is_visible(self, locator):
        element = self.find_element(locator, required=False)
        if element is not None:
            return element.is_displayed()
        return None

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

    def _parse_attribute_locator(self, attribute_locator):
        parts = attribute_locator.rpartition('@')
        if len(parts[0]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an element locator." % (attribute_locator))
        if len(parts[2]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an attribute name." % (attribute_locator))
        return parts[0], parts[2]

    def _page_contains(self, text):
        self.browser.switch_to.default_content()

        if self.is_text_present(text):
            return True

        subframes = self.find_element("xpath=//frame|//iframe",
                                      first_only=False,
                                      required=False)
        self.debug('Current frame has %d subframes' % len(subframes))
        for frame in subframes:
            self.browser.switch_to.frame(frame)
            found_text = self.is_text_present(text)
            self.browser.switch_to.default_content()
            if found_text:
                return True
        return False
