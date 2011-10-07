import os
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(os.path.join(_THIS_DIR, "lib", "selenium-2.4.0", "py"))

from robot.variables import GLOBAL_VARIABLES
from robot.errors import DataError
from robot import utils
from robot.output import LOGGER, Message
from browsercache import BrowserCache
from elementfinder import ElementFinder
from windowmanager import WindowManager

from selenium import webdriver
import webdrivermonkeypatches
    
FIREFOX_PROFILE_DIR = os.path.join(_THIS_DIR, 'firefoxprofile')
BROWSER_NAMES = {'ff': '*firefox',
                 'firefox': '*firefox',
                 'ie': '*iexplore',
                 'internetexplorer': '*iexplore',
                 'googlechrome': '*googlechrome',
                 'gc': '*googlechrome'
                }

class Selenium2Library(object):

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.5

    def __init__(self):
        self._cache = BrowserCache()
        self._element_finder = ElementFinder()
        self._window_manager = WindowManager()
        self._speed_in_secs = float(0)
        self._timeout_in_secs = float(5)

    def open_browser(self, url, browser='firefox', alias=None):
        self._info("Opening browser '%s' to base url '%s'" % (browser, url))
        browser_name = browser
        browser = self._make_browser(browser_name)
        browser.get(url)
        self._debug('Opened browser with session id %s'
                    % browser.session_id)
        return self._cache.register(browser, alias)

    def close_browser(self):
        if self._cache.current:
            self._debug('Closing browser with session id %s'
                        % self._cache.current.session_id)
            self._cache.close()

    def close_all_browsers(self):
        self._debug('Closing all browsers')
        self._cache.close_all()

    def get_title(self):
        return self._current_browser().get_title()

    def title_should_be(self, title):
        actual = self.get_title()
        if actual != title:
            raise AssertionError("Title should have been '%s' but was '%s'"
                                  % (title, actual))
        self._info("Page title is '%s'." % title)

    def get_url(self):
        return self._current_browser().get_current_url()

    def location_should_be(self, url):
        actual = self.get_url()
        if  actual != url:
            raise AssertionError("Location should have been '%s' but was '%s'"
                                 % (url, actual))
        self._info("Current location is '%s'." % url)

    def location_should_contain(self, expected):
        actual = self.get_url()
        if not expected in actual:
            raise AssertionError("Location should have contained '%s' "
                                 "but it was '%s'." % (expected, actual))
        self._info("Current location contains '%s'." % expected)

    def get_source(self):
        return self._current_browser().get_page_source()

    def switch_browser(self, index_or_alias):
        try:
            self._cache.switch(index_or_alias)
            self._debug('Switched to browser with Selenium session id %s'
                         % self._cache.current.session_id)
        except (RuntimeError, DataError):  # RF 2.6 uses RE, earlier DE
            raise RuntimeError("No browser with index or alias '%s' found."
                               % index_or_alias)

    def go_to(self, url):
        self._info("Opening url '%s'" % url)
        self._current_browser().get(url)

    def click_link(self, locator):
        self._info("Clicking link '%s'." % locator)
        link = self._element_find(locator, True, True, tag='a')
        link.click()

    def select_window(self, locator=None):
        self._window_manager.select(self._current_browser(), locator)

    def close_window(self):
        self._current_browser().close()

    def get_window_identifiers(self):
        return self._window_manager.get_window_handles(self._current_browser())

    def get_selenium_speed(self):
        return utils.secs_to_timestr(self._speed_in_secs)

    def set_selenium_speed(self, seconds):
        old_speed = self.get_selenium_speed()
        self._speed_in_secs = utils.timestr_to_secs(seconds)
        for browser in self._cache.browsers:
            browser.set_speed(self._speed_in_secs)
        return old_speed

    def get_selenium_timeout(self):
        return utils.secs_to_timestr(self._timeout_in_secs)

    def set_selenium_timeout(self, seconds):
        old_timeout = self.get_selenium_timeout()
        self._timeout_in_secs = utils.timestr_to_secs(seconds)
        for browser in self._cache.get_open_browsers():
            browser.set_script_timeout(self._timeout_in_secs)
        return old_timeout

    def checkbox_should_be_selected(self, locator):
        self._info("Verifying checkbox '%s' is selected." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            raise AssertionError("Checkbox '%s' should have been selected "
                                 "but was not" % locator)

    def checkbox_should_not_be_selected(self, locator):
        self._info("Verifying checkbox '%s' is not selected." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            raise AssertionError("Checkbox '%s' should not have been selected"
                                  % locator)

    def select_checkbox(self, locator):
        self._info("Selecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if not element.is_selected():
            element.click()

    def unselect_checkbox(self, locator):
        self._info("Unselecting checkbox '%s'." % locator)
        element = self._get_checkbox(locator)
        if element.is_selected():
            element.click()

    def radio_button_should_be_set_to(self, group_name, value):
        self._info("Verifying radio button '%s' has selection '%s'." \
                   % (group_name, value))
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is None or actual_value != value:
            raise AssertionError("Selection of radio button '%s' should have "
                                 "been '%s' but was '%s'"
                                  % (group_name, value, actual_value))

    def select_radio_button(self, group_name, value):
        self._info("Selecting '%s' from radio button '%s'." % (value, group_name))
        element = self._get_radio_button_with_value(group_name, value)
        if not element.is_selected():
            element.click()

    def radio_button_should_not_be_selected(self, group_name):
        self._info("Verifying radio button '%s' has no selection." % group_name)
        elements = self._get_radio_buttons(group_name)
        actual_value = self._get_value_from_radio_buttons(elements)
        if actual_value is not None:
            raise AssertionError("Radio button group '%s' should not have had "
                                 "selection, but '%s' was selected"
                                  % (group_name, actual_value))

    def reload_page(self):
        self._current_browser().refresh()

    def element_text_should_be(self, locator, expected, message=''):
        self._info("Verifying element '%s' contains exactly text '%s'."
                    % (locator, expected))
        element = self._element_find(locator, True, True)
        actual = element.text
        if expected != actual:
            if not message:
                message = "The text of element '%s' should have been '%s' but "\
                          "in fact it was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def click_element(self, locator):
        self._info("Clicking element '%s'." % locator)
        self._element_find(locator, True, True).click()

    def log_source(self, level='INFO'):
        source = self.get_source()
        self._log(source, level.upper())
        return source

    def page_should_contain(self, text, loglevel='INFO'):
        if not self._page_contains(text):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def page_should_not_contain(self, text, loglevel='INFO'):
        if self._page_contains(text):
            self.log_source(loglevel)
            raise AssertionError("Page should not have contained text '%s'" % text)
        self._info("Current page does not contain text '%s'." % text)

    def page_should_contain_element(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, None, message, loglevel)

    def page_should_not_contain_element(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, None, message, loglevel)

    def element_should_contain(self, locator, expected, message=''):
        self._info("Verifying element '%s' contains text '%s'."
                    % (locator, expected))
        actual = self._get_text(locator)
        if not expected in actual:
            if not message:
                message = "Element '%s' should have contained text '%s' but "\
                          "its text was '%s'." % (locator, expected, actual)
            raise AssertionError(message)

    def element_should_be_visible(self, locator, message=''):
        self._info("Verifying element '%s' is visible." % locator)
        visible = self._is_visible(locator)
        if not visible:
            if not message:
                message = "The element '%s' should be visible, but it "\
                          "is not." % locator
            raise AssertionError(message)

    def element_should_not_be_visible(self, locator, message=''):
        self._info("Verifying element '%s' is not visible." % locator)
        visible = self._is_visible(locator)
        if visible:
            if not message:
                message = "The element '%s' should not be visible, "\
                          "but it is." % locator
            raise AssertionError(message)

    def page_should_contain_checkbox(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'checkbox', message, loglevel)

    def page_should_not_contain_checkbox(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'checkbox', message, loglevel)

    def page_should_contain_radio_button(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'radio button', message, loglevel)

    def page_should_not_contain_radio_button(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'radio button', message, loglevel)

    def page_should_contain_image(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'image', message, loglevel)

    def page_should_not_contain_image(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'image', message, loglevel)

    def page_should_contain_link(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'link', message, loglevel)

    def page_should_not_contain_link(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'link', message, loglevel)

    def page_should_contain_list(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'list', message, loglevel)

    def page_should_not_contain_list(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'list', message, loglevel)

    def page_should_contain_textfield(self, locator, message='', loglevel='INFO'):
        self._page_should_contain_element(locator, 'text field', message, loglevel)

    def page_should_not_contain_textfield(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'text field', message, loglevel)

    def textfield_should_contain(self, locator, expected, message=''):
        element = self._element_find(locator, True, False, 'text field')
        actual = element.get_attribute('value') if element is not None else None
        if not expected in actual:
            if not message:
                message = "Text field '%s' should have contained text '%s' "\
                          "but it contained '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Text field '%s' contains text '%s'." % (locator, expected))

    def input_text(self, locator, text):
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        element = self._element_find(locator, True, True, 'text field')
        element.send_keys(text)

    def textfield_value_should_be(self, locator, expected, message=''):
        element = self._element_find(locator, True, False, 'text field')
        actual = element.get_attribute('value') if element is not None else None
        if actual != expected:
            if not message:
                message = "Value of text field '%s' should have been '%s' "\
                          "but was '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Content of text field '%s' is '%s'." % (locator, expected))

    def page_should_contain_button(self, locator, message='', loglevel='INFO'):
        try:
            self._page_should_contain_element(locator, 'input', message, loglevel)
        except AssertionError:
            self._page_should_contain_element(locator, 'button', message, loglevel)

    def page_should_not_contain_button(self, locator, message='', loglevel='INFO'):
        self._page_should_not_contain_element(locator, 'button', message, loglevel)
        self._page_should_not_contain_element(locator, 'input', message, loglevel)

    def get_all_links(self):
        links = []
        for anchor in self._element_find("tag=a", False, False, 'a'):
            links.append(anchor.get_attribute('id'))
        return links

    def xpath_should_match_x_times(self, xpath, expected_xpath_count, message='', loglevel='INFO'):
        actual_xpath_count = len(self._element_find("xpath=" + xpath, False, False))
        if int(actual_xpath_count) != int(expected_xpath_count):
            if not message:
                message = "Xpath %s should have matched %s times but matched %s times"\
                            %(xpath, expected_xpath_count, actual_xpath_count)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Current page contains %s elements matching '%s'."
                   % (actual_xpath_count, xpath))

    def get_matching_xpath_count(self, xpath):
        count = len(self._element_find("xpath=" + xpath, False, False))
        return str(count)

    def delete_all_cookies(self):
        self._current_browser().delete_all_cookies()

    def get_cookies(self):
        pairs = []
        for cookie in self._current_browser().get_cookies():
            pairs.append(cookie['name'] + "=" + cookie['value'])
        return '; '.join(pairs)

    def get_cookie_value(self, name):
        cookie = self._current_browser().get_cookie(name)
        if cookie is not None:
            return cookie['value']
        return None

    def delete_cookie(self, name):
        self._current_browser().delete_cookie(name)

    def element_should_be_enabled(self, locator):
        if not self._is_enabled(locator):
            raise AssertionError("Element '%s' is disabled." % (locator))

    def element_should_be_disabled(self, locator):
        if self._is_enabled(locator):
            raise AssertionError("Element '%s' is enabled." % (locator))

    def get_element_attribute(self, attribute_locator):
        locator, attribute_name = self._parse_attribute_locator(attribute_locator)
        element = self._element_find(locator, True, False)
        if element is None:
            return None
        return element.get_attribute(attribute_name)

    def get_horizontal_position(self, locator):
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("Could not determine position for '%s'" % (locator))
        return element.location['x']

    def get_vertical_position(self, locator):
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("Could not determine position for '%s'" % (locator))
        return element.location['y']

    def _parse_attribute_locator(self, attribute_locator):
        parts = attribute_locator.partition('@')
        if len(parts[0]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an element locator" % (locator))
        if len(parts[2]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an attribute name" % (locator))
        return (parts[0], parts[2])

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

    def _is_form_element(self, element):
        if element is None:
            return False
        tag = element.tag_name.lower()
        return tag == 'input' or tag == 'select' or tag == 'textarea' or tag == 'button'

    def _is_visible(self, locator):
        element = self._element_find(locator, True, False)
        if element is not None:
            return element.is_displayed()
        return None

    def _get_text(self, locator):
        element = self._element_find(locator, True, False)
        if element is not None:
            return element.text
        return None

    def _is_element_present(self, locator, tag=None):
        return (self._element_find(locator, True, False, tag=tag) != None)

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

    def _is_text_present(self, text):
        locator = "xpath=//*[contains(., %s)]" % self._xpath_criteria_escape(text);
        return self._is_element_present(locator)

    def _page_contains(self, text):
        browser = self._current_browser()
        browser.switch_to_default_content()

        if self._is_text_present(text):
            return True

        js_for_num_subframes = "return window.document.getElementsByTagName('frame').length"
        num_subframes = int(browser.execute_script(js_for_num_subframes))
        self._debug('Current frame has %d subframes' % num_subframes)
        for i in range(num_subframes):
            browser.switch_to_frame(i)
            found_text = self._is_text_present(text)
            browser.switch_to_default_content()
            if found_text:
                return True

        return False

    def _xpath_criteria_escape(self, str):
        if '"' in str and '\'' in str:
            parts_wo_apos = str.split('\'')
            return "concat('%s')" % "', \"'\", '".join(parts_wo_apos)
        if '\'' in str:
            return "\"%s\"" % str
        return "'%s'" % str

    def _get_checkbox(self, locator):
        return self._element_find(locator, True, True, tag='input')

    def _get_radio_buttons(self, group_name):
        xpath = "xpath=//input[@type='radio' and @name='%s']" % group_name
        self._debug('Radio group locator: ' + xpath)
        return self._element_find(xpath, False, True)

    def _get_radio_button_with_value(self, group_name, value):
        xpath = "xpath=//input[@type='radio' and @name='%s' and (@value='%s' or @id='%s')]" \
                 % (group_name, value, value)
        self._debug('Radio group locator: ' + xpath)
        return self._element_find(xpath, True, True)

    def _get_value_from_radio_buttons(self, elements):
        for element in elements:
            if element.is_selected():
                return element.get_attribute('value')
        return None

    def _current_browser(self):
        if not self._cache.current:
            raise RuntimeError('No browser is open')
        return self._cache.current

    def _element_find(self, locator, first_only, required, tag=None):
        browser = self._current_browser()
        elements = self._element_finder.find(browser, locator, tag)
        if required and len(elements) == 0:
            raise ValueError("Element locator '" + locator + "' did not match any elements")
        if first_only:
            if len(elements) == 0: return None
            return elements[0]
        return elements

    def _make_browser(self, browser_name):
        browser_token = self._get_browser_token(browser_name)
        browser = None
        if browser_token == '*firefox':
            browser = webdriver.Firefox(webdriver.FirefoxProfile(FIREFOX_PROFILE_DIR))
        elif browser_token == '*googlechrome':
            browser = webdriver.Chrome()
        elif browser_token == '*iexplore':
            browser = webdriver.Ie()

        if browser is None:
            raise ValueError(browser_name + " is not a supported browser")

        browser.set_speed(self._speed_in_secs)
        browser.set_script_timeout(self._timeout_in_secs)

        return browser

    def _get_browser_token(self, browser_name):
        return BROWSER_NAMES.get(browser_name.lower().replace(' ', ''), browser_name)

    def _get_log_dir(self):
        logfile = GLOBAL_VARIABLES['${LOG FILE}']
        if logfile != 'NONE':
            return os.path.dirname(logfile)
        return GLOBAL_VARIABLES['${OUTPUTDIR}']

    def _log(self, message, level='INFO'):
        if level != 'NONE':
            LOGGER.log_message(Message(message, level))

    def _info(self, message):
        self._log(message)

    def _debug(self, message):
        self._log(message, 'DEBUG')

    def _warn(self, message):
        self._log(message,  "WARN")

    def _html(self, message):
        self._log(message, 'HTML')

    def _get_error_message(self, exception):
        # Cannot use unicode(exception) because it fails on Python 2.5 and
        # earlier if the message contains non-ASCII chars.
        # See for details: http://bugs.jython.org/issue1585
        return unicode(exception.args and exception.args[0] or '')

    def _error_contains(self, exception, message):
        return message in self._get_error_message(exception)

    def _log_list(self, items, what='item'):
        msg = ['Altogether %d %s%s.' % (len(items), what, ['s',''][len(items)==1])]
        for index, item in enumerate(items):
            msg.append('%d: %s' % (index+1, item))
        self._info('\n'.join(msg))
        return items
