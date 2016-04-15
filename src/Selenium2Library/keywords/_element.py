from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.remote.webelement import WebElement
from Selenium2Library import utils
from Selenium2Library.locators import ElementFinder
from Selenium2Library.locators import CustomLocator
from keywordgroup import KeywordGroup

try:
    basestring  # attempt to evaluate basestring
    def isstr(s):
        return isinstance(s, basestring)
except NameError:
    def isstr(s):
        return isinstance(s, str)

class _ElementKeywords(KeywordGroup):

    def __init__(self):
        self._element_finder = ElementFinder()

    # Public, get element(s)

    def get_webelement(self, locator):
        """Returns the first WebElement matching the given locator.

        See `introduction` for details about locating elements.
        """
        return self._element_find(locator, True, True)

    def get_webelements(self, locator):
        """Returns list of WebElement objects matching locator.

        See `introduction` for details about locating elements.
        """
        return self._element_find(locator, False, True)

    # Public, element lookups

    def current_frame_contains(self, text, loglevel='INFO'):
        """Verifies that current frame contains `text`.

        See `Page Should Contain ` for explanation about `loglevel` argument.
        """
        if not self._is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)


    def current_frame_should_not_contain(self, text, loglevel='INFO'):
        """Verifies that current frame contains `text`.

        See `Page Should Contain ` for explanation about `loglevel` argument.
        """
        if self._is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s' "
                                 "but it did" % text)
        self._info("Current page should not contain text '%s'." % text)

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
        actual = self._get_text(locator)
        if not expected in actual:
            if not message:
                message = "Element '%s' should have contained text '%s' but "\
                          "its text was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def element_should_not_contain(self, locator, expected, message=''):
        """Verifies element identified by `locator` does not contain text `expected`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `Element Should Contain` for more details.
        """
        self._info("Verifying element '%s' does not contain text '%s'."
                   % (locator, expected))
        actual = self._get_text(locator)
        if expected in actual:
            if not message:
                message = "Element '%s' should not contain text '%s' but " \
                          "it did." % (locator, expected)
            raise AssertionError(message)

    def frame_should_contain(self, locator, text, loglevel='INFO'):
        """Verifies frame identified by `locator` contains `text`.

        See `Page Should Contain ` for explanation about `loglevel` argument.

        Key attributes for frames are `id` and `name.` See `introduction` for
        details about locating elements.
        """
        if not self._frame_contains(locator, text):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def page_should_contain(self, text, loglevel='INFO'):
        """Verifies that current page contains `text`.

        If this keyword fails, it automatically logs the page source
        using the log level specified with the optional `loglevel` argument.
        Valid log levels are DEBUG, INFO (default), WARN, and NONE. If the
        log level is NONE or below the current active log level the source
        will not be logged.
        """
        if not self._page_contains(text):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def page_should_contain_element(self, locator, message='', loglevel='INFO'):
        """Verifies element identified by `locator` is found on the current page.

        `message` can be used to override default error message.

        See `Page Should Contain` for explanation about `loglevel` argument.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, None, message, loglevel)

    def locator_should_match_x_times(self, locator, expected_locator_count, message='', loglevel='INFO'):
        """Verifies that the page contains the given number of elements located by the given `locator`.

        See `introduction` for details about locating elements.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.
        """
        actual_locator_count = len(self._element_find(locator, False, False))
        if int(actual_locator_count) != int(expected_locator_count):
            if not message:
                message = "Locator %s should have matched %s times but matched %s times"\
                            %(locator, expected_locator_count, actual_locator_count)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Current page contains %s elements matching '%s'."
                   % (actual_locator_count, locator))

    def page_should_not_contain(self, text, loglevel='INFO'):
        """Verifies the current page does not contain `text`.

        See `Page Should Contain ` for explanation about `loglevel` argument.
        """
        if self._page_contains(text):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s'" % text)
        self._info("Current page does not contain text '%s'." % text)

    def page_should_not_contain_element(self, locator, message='', loglevel='INFO'):
        """Verifies element identified by `locator` is not found on the current page.

        `message` can be used to override the default error message.

        See `Page Should Contain ` for explanation about `loglevel` argument.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, None, message, loglevel)

    # Public, attributes

    def assign_id_to_element(self, locator, id):
        """Assigns a temporary identifier to element specified by `locator`.

        This is mainly useful if the locator is complicated/slow XPath expression.
        Identifier expires when the page is reloaded.

        Example:
        | Assign ID to Element | xpath=//div[@id="first_div"] | my id |
        | Page Should Contain Element | my id |
        """
        self._info("Assigning temporary id '%s' to element '%s'" % (id, locator))
        element = self._element_find(locator, True, True)
        self._current_browser().execute_script("arguments[0].id = '%s';" % id, element)

    def element_should_be_disabled(self, locator):
        """Verifies that element identified with `locator` is disabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if self._is_enabled(locator):
            raise AssertionError("Element '%s' is enabled." % (locator))

    def element_should_be_enabled(self, locator):
        """Verifies that element identified with `locator` is enabled.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        if not self._is_enabled(locator):
            raise AssertionError("Element '%s' is disabled." % (locator))

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
        self._info("Verifying element '%s' is visible." % locator)
        visible = self._is_visible(locator)
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
        """
        self._info("Verifying element '%s' is not visible." % locator)
        visible = self._is_visible(locator)
        if visible:
            if not message:
                message = "The element '%s' should not be visible, "\
                          "but it is." % locator
            raise AssertionError(message)

    def element_text_should_be(self, locator, expected, message=''):
        """Verifies element identified by `locator` exactly contains text `expected`.

        In contrast to `Element Should Contain`, this keyword does not try
        a substring match but an exact match on the element identified by `locator`.

        `message` can be used to override the default error message.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Verifying element '%s' contains exactly text '%s'."
                    % (locator, expected))
        element = self._element_find(locator, True, True)
        actual = element.text
        if expected != actual:
            if not message:
                message = "The text of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def get_element_attribute(self, attribute_locator):
        """Return value of element attribute.

        `attribute_locator` consists of element locator followed by an @ sign
        and attribute name, for example "element_id@class".
        """
        locator, attribute_name = self._parse_attribute_locator(attribute_locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise ValueError("Element '%s' not found." % (locator))
        return element.get_attribute(attribute_name)

    def get_horizontal_position(self, locator):
        """Returns horizontal position of element identified by `locator`.

        The position is returned in pixels off the left side of the page,
        as an integer. Fails if a matching element is not found.

        See also `Get Vertical Position`.
        """
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("Could not determine position for '%s'" % (locator))
        return element.location['x']

    def get_element_size(self, locator):
        """Returns width and height of element identified by `locator`.

        The element width and height is returned.
        Fails if a matching element is not found.
        """
        element = self._element_find(locator, True, True)

        return element.size['width'], element.size['height']

    def get_value(self, locator):
        """Returns the value attribute of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._get_value(locator)

    def get_text(self, locator):
        """Returns the text value of element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        return self._get_text(locator)

    def clear_element_text(self, locator):
        """Clears the text value of text entry element identified by `locator`.

        See `introduction` for details about locating elements.
        """
        element = self._element_find(locator, True, True)
        element.clear()

    def get_vertical_position(self, locator):
        """Returns vertical position of element identified by `locator`.

        The position is returned in pixels off the top of the page,
        as an integer. Fails if a matching element is not found.

        See also `Get Horizontal Position`.
        """
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("Could not determine position for '%s'" % (locator))
        return element.location['y']

    # Public, mouse input/events

    def click_element(self, locator):
        """Click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Clicking element '%s'." % locator)
        self._element_find(locator, True, True).click()

    def click_element_at_coordinates(self, locator, xoffset, yoffset):
        """Click element identified by `locator` at x/y coordinates of the element.
        Cursor is moved and the center of the element and x/y coordinates are
        calculted from that point.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Click clicking element '%s' in coordinates '%s', '%s'." % (locator, xoffset, yoffset))
        element = self._element_find(locator, True, True)
        #self._element_find(locator, True, True).click()
        #ActionChains(self._current_browser()).move_to_element_with_offset(element, xoffset, yoffset).click().perform()
        ActionChains(self._current_browser()).move_to_element(element).move_by_offset(xoffset, yoffset).click().perform()

    def double_click_element(self, locator):
        """Double click element identified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Double clicking element '%s'." % locator)
        element = self._element_find(locator, True, True)
        ActionChains(self._current_browser()).double_click(element).perform()

    def focus(self, locator):
        """Sets focus to element identified by `locator`."""
        element = self._element_find(locator, True, True)
        self._current_browser().execute_script("arguments[0].focus();", element)

    def drag_and_drop(self, source, target):
        """Drags element identified with `source` which is a locator.

        Element can be moved on top of another element with `target`
        argument.

        `target` is a locator of the element where the dragged object is
        dropped.

        Examples:
        | Drag And Drop | elem1 | elem2 | # Move elem1 over elem2. |
        """
        src_elem = self._element_find(source,True,True)
        trg_elem =  self._element_find(target,True,True)
        ActionChains(self._current_browser()).drag_and_drop(src_elem, trg_elem).perform()


    def drag_and_drop_by_offset(self, source, xoffset, yoffset):
        """Drags element identified with `source` which is a locator.

        Element will be moved by xoffset and yoffset, each of which is a
        negative or positive number specify the offset.

        Examples:
        | Drag And Drop By Offset | myElem | 50 | -35 | # Move myElem 50px right and 35px down. |
        """
        src_elem = self._element_find(source, True, True)
        ActionChains(self._current_browser()).drag_and_drop_by_offset(src_elem, xoffset, yoffset).perform()

    def mouse_down(self, locator):
        """Simulates pressing the left mouse button on the element specified by `locator`.

        The element is pressed without releasing the mouse button.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.

        See also the more specific keywords `Mouse Down On Image` and
        `Mouse Down On Link`.
        """
        self._info("Simulating Mouse Down on element '%s'" % locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        ActionChains(self._current_browser()).click_and_hold(element).perform()

    def mouse_out(self, locator):
        """Simulates moving mouse away from the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Simulating Mouse Out on element '%s'" % locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        size = element.size
        offsetx = (size['width'] / 2) + 1
        offsety = (size['height'] / 2) + 1
        ActionChains(self._current_browser()).move_to_element(element).move_by_offset(offsetx, offsety).perform()

    def mouse_over(self, locator):
        """Simulates hovering mouse over the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Simulating Mouse Over on element '%s'" % locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        ActionChains(self._current_browser()).move_to_element(element).perform()

    def mouse_up(self, locator):
        """Simulates releasing the left mouse button on the element specified by `locator`.

        Key attributes for arbitrary elements are `id` and `name`. See
        `introduction` for details about locating elements.
        """
        self._info("Simulating Mouse Up on element '%s'" % locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        ActionChains(self._current_browser()).release(element).perform()

    def open_context_menu(self, locator):
        """Opens context menu on element identified by `locator`."""
        element = self._element_find(locator, True, True)
        ActionChains(self._current_browser()).context_click(element).perform()

    def simulate(self, locator, event):
        """Simulates `event` on element identified by `locator`.

        This keyword is useful if element has OnEvent handler that needs to be
        explicitly invoked.

        See `introduction` for details about locating elements.
        """
        element = self._element_find(locator, True, True)
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
        self._current_browser().execute_script(script, element, event)

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
        element = self._element_find(locator, True, True)
        #select it
        element.send_keys(key)

    # Public, links

    def click_link(self, locator):
        """Clicks a link identified by locator.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._info("Clicking link '%s'." % locator)
        link = self._element_find(locator, True, True, tag='a')
        link.click()

    def get_all_links(self):
        """Returns a list containing ids of all links found in current page.

        If a link has no id, an empty string will be in the list instead.
        """
        links = []
        for anchor in self._element_find("tag=a", False, False, 'a'):
            links.append(anchor.get_attribute('id'))
        return links

    def mouse_down_on_link(self, locator):
        """Simulates a mouse down event on a link.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        element = self._element_find(locator, True, True, 'link')
        ActionChains(self._current_browser()).click_and_hold(element).perform()

    def page_should_contain_link(self, locator, message='', loglevel='INFO'):
        """Verifies link identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'link', message, loglevel)

    def page_should_not_contain_link(self, locator, message='', loglevel='INFO'):
        """Verifies image identified by `locator` is not found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'link', message, loglevel)

    # Public, images

    def click_image(self, locator):
        """Clicks an image found by `locator`.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._info("Clicking image '%s'." % locator)
        element = self._element_find(locator, True, False, 'image')
        if element is None:
            # A form may have an image as it's submit trigger.
            element = self._element_find(locator, True, True, 'input')
        element.click()

    def mouse_down_on_image(self, locator):
        """Simulates a mouse down event on an image.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        element = self._element_find(locator, True, True, 'image')
        ActionChains(self._current_browser()).click_and_hold(element).perform()

    def page_should_contain_image(self, locator, message='', loglevel='INFO'):
        """Verifies image identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._page_should_contain_element(locator, 'image', message, loglevel)

    def page_should_not_contain_image(self, locator, message='', loglevel='INFO'):
        """Verifies image identified by `locator` is found from current page.

        See `Page Should Contain Element` for explanation about `message` and
        `loglevel` arguments.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._page_should_not_contain_element(locator, 'image', message, loglevel)

    # Public, xpath

    def get_matching_xpath_count(self, xpath):
        """Returns number of elements matching `xpath`

        One should not use the xpath= prefix for 'xpath'. XPath is assumed.

        Correct:
        | count = | Get Matching Xpath Count | //div[@id='sales-pop']
        Incorrect:
        | count = | Get Matching Xpath Count | xpath=//div[@id='sales-pop']

        If you wish to assert the number of matching elements, use
        `Xpath Should Match X Times`.
        """
        count = len(self._element_find("xpath=" + xpath, False, False))
        return str(count)

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
        actual_xpath_count = len(self._element_find("xpath=" + xpath, False, False))
        if int(actual_xpath_count) != int(expected_xpath_count):
            if not message:
                message = "Xpath %s should have matched %s times but matched %s times"\
                            %(xpath, expected_xpath_count, actual_xpath_count)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Current page contains %s elements matching '%s'."
                   % (actual_xpath_count, xpath))

    # Public, custom
    def add_location_strategy(self, strategy_name, strategy_keyword, persist=False):
        """Adds a custom location strategy based on a user keyword. Location strategies are
        automatically removed after leaving the current scope by default. Setting `persist`
        to any non-empty string will cause the location strategy to stay registered throughout
        the life of the test.

        Trying to add a custom location strategy with the same name as one that already exists will
        cause the keyword to fail.

        Custom locator keyword example:
        | Custom Locator Strategy | [Arguments] | ${browser} | ${criteria} | ${tag} | ${constraints} |
        |   | ${retVal}= | Execute Javascript | return window.document.getElementById('${criteria}'); |
        |   | [Return] | ${retVal} |

        Usage example:
        | Add Location Strategy | custom | Custom Locator Strategy |
        | Page Should Contain Element | custom=my_id |

        See `Remove Location Strategy` for details about removing a custom location strategy.
        """
        strategy = CustomLocator(strategy_name, strategy_keyword)
        self._element_finder.register(strategy, persist)

    def remove_location_strategy(self, strategy_name):
        """Removes a previously added custom location strategy.
        Will fail if a default strategy is specified.

        See `Add Location Strategy` for details about adding a custom location strategy.
        """
        self._element_finder.unregister(strategy_name)

    # Private

    def _element_find(self, locator, first_only, required, tag=None):
        browser = self._current_browser()
        if isstr(locator):
            elements = self._element_finder.find(browser, locator, tag)
            if required and len(elements) == 0:
                raise ValueError("Element locator '" + locator + "' did not match any elements.")
            if first_only:
                if len(elements) == 0: return None
                return elements[0]
        elif isinstance(locator, WebElement):
            elements = locator
        # do some other stuff here like deal with list of webelements
        # ... or raise locator/element specific error if required
        return elements

    def _frame_contains(self, locator, text):
        browser = self._current_browser()
        element = self._element_find(locator, True, True)
        browser.switch_to_frame(element)
        self._info("Searching for text from frame '%s'." % locator)
        found = self._is_text_present(text)
        browser.switch_to_default_content()
        return found

    def _get_text(self, locator):
        element = self._element_find(locator, True, True)
        if element is not None:
            return element.text
        return None

    def _get_value(self, locator, tag=None):
        element = self._element_find(locator, True, False, tag=tag)
        return element.get_attribute('value') if element is not None else None

    def _is_enabled(self, locator):
        element = self._element_find(locator, True, True)
        if not self._is_form_element(element):
            raise AssertionError("ERROR: Element %s is not an input." % (locator))
        if not element.is_enabled():
            return False
        read_only = element.get_attribute('readonly')
        if read_only == 'readonly' or read_only == 'true':
            return False
        return True

    def _is_text_present(self, text):
        locator = "xpath=//*[contains(., %s)]" % utils.escape_xpath_value(text);
        return self._is_element_present(locator)

    def _is_visible(self, locator):
        element = self._element_find(locator, True, False)
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
           self._debug(message)
           raise ValueError(message)

    def _parse_attribute_locator(self, attribute_locator):
        parts = attribute_locator.rpartition('@')
        if len(parts[0]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an element locator." % (attribute_locator))
        if len(parts[2]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an attribute name." % (attribute_locator))
        return (parts[0], parts[2])

    def _is_element_present(self, locator, tag=None):
        return (self._element_find(locator, True, False, tag=tag) is not None)

    def _page_contains(self, text):
        browser = self._current_browser()
        browser.switch_to_default_content()

        if self._is_text_present(text):
            return True

        subframes = self._element_find("xpath=//frame|//iframe", False, False)
        self._debug('Current frame has %d subframes' % len(subframes))
        for frame in subframes:
            browser.switch_to_frame(frame)
            found_text = self._is_text_present(text)
            browser.switch_to_default_content()
            if found_text:
                return True

        return False

    def _page_should_contain_element(self, locator, tag, message, loglevel):
        element_name = tag if tag is not None else 'element'
        if not self._is_element_present(locator, tag):
            if not message:
                message = "Page should have contained %s '%s' but did not"\
                           % (element_name, locator)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Current page contains %s '%s'." % (element_name, locator))

    def _page_should_not_contain_element(self, locator, tag, message, loglevel):
        element_name = tag if tag is not None else 'element'
        if self._is_element_present(locator, tag):
            if not message:
                message = "Page should not have contained %s '%s'"\
                           % (element_name, locator)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Current page does not contain %s '%s'."
                   % (element_name, locator))
