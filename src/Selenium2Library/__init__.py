import os
_THIS_DIR = os.path.dirname(os.path.abspath(__file__))

import sys
sys.path.append(os.path.join(_THIS_DIR, "lib", "selenium-2.8.1", "py"))

import inspect
try:
    from decorator import decorator
except SyntaxError: # decorator module requires Python/Jython 2.4+
    decorator = None
if sys.platform == 'cli':
    decorator = None # decorator module doesn't work with IronPython 2.6

import robot
from robot.variables import GLOBAL_VARIABLES
from robot.errors import DataError
from robot.api import logger
from robot.libraries import BuiltIn

from selenium import webdriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
import webdrivermonkeypatches

from browsercache import BrowserCache
from elementfinder import ElementFinder
from windowmanager import WindowManager
from tableelementfinder import TableElementFinder
import utils
    
FIREFOX_PROFILE_DIR = os.path.join(_THIS_DIR, 'firefoxprofile')
BROWSER_NAMES = {'ff': '*firefox',
                 'firefox': '*firefox',
                 'ie': '*iexplore',
                 'internetexplorer': '*iexplore',
                 'googlechrome': '*googlechrome',
                 'gc': '*googlechrome'
                }
BUILTIN = BuiltIn.BuiltIn()

def _run_keyword_on_failure_decorator(method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except Exception, err:
        self = args[0]
        self._run_on_failure()
        raise

class Selenium2LibraryType(type):
    def __new__(cls, clsname, bases, dict):
        if decorator:
            for name, method in dict.items():
                if not name.startswith('_') and inspect.isroutine(method):
                    dict[name] = decorator(_run_keyword_on_failure_decorator, method)
        return type.__new__(cls, clsname, bases, dict)

class Selenium2Library(object):
    __metaclass__ = Selenium2LibraryType

    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    ROBOT_LIBRARY_VERSION = 0.5

    def __init__(self):
        self._cache = BrowserCache()
        self._element_finder = ElementFinder()
        self._table_element_finder = TableElementFinder(self._element_finder)
        self._window_manager = WindowManager()
        self._speed_in_secs = float(0)
        self._timeout_in_secs = float(5)
        self._cancel_on_next_confirmation = False
        self._run_on_failure_keyword = None
        self._screenshot_index = 0

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
        return robot.utils.secs_to_timestr(self._speed_in_secs)

    def set_selenium_speed(self, seconds):
        old_speed = self.get_selenium_speed()
        self._speed_in_secs = robot.utils.timestr_to_secs(seconds)
        for browser in self._cache.browsers:
            browser.set_speed(self._speed_in_secs)
        return old_speed

    def get_selenium_timeout(self):
        return robot.utils.secs_to_timestr(self._timeout_in_secs)

    def set_selenium_timeout(self, seconds):
        old_timeout = self.get_selenium_timeout()
        self._timeout_in_secs = robot.utils.timestr_to_secs(seconds)
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

    def double_click_element(self, locator):
        self._info("Double clicking element '%s'." % locator)
        element = self._element_find(locator, True, True)
        ActionChains(self._current_browser()).double_click(element).perform()

    def log_source(self, loglevel='INFO'):
        source = self.get_source()
        self._log(source, loglevel.upper())
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
        actual = self._get_value(locator, 'text field')
        if not expected in actual:
            if not message:
                message = "Text field '%s' should have contained text '%s' "\
                          "but it contained '%s'" % (locator, expected, actual)
            raise AssertionError(message)
        self._info("Text field '%s' contains text '%s'." % (locator, expected))

    def input_text(self, locator, text):
        self._info("Typing text '%s' into text field '%s'" % (text, locator))
        self._input_text_into_text_field(locator, text)

    def textfield_value_should_be(self, locator, expected, message=''):
        element = self._element_find(locator, True, False, 'text field')
        if element is None: element = self._element_find(locator, True, False, 'file upload')
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
            raise ValueError("Element '%s' not found." % (locator))
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

    def submit_form(self, locator=None):
        self._info("Submitting form '%s'." % locator)
        if not locator:
            locator = 'xpath=//form'
        element = self._element_find(locator, True, True, 'form')
        element.submit()

    def click_button(self, locator):
        self._info("Clicking button '%s'." % locator)
        element = self._element_find(locator, True, False, 'input')
        if element is None:
            element = self._element_find(locator, True, True, 'button')
        element.click()

    def get_value(self, locator):
        return self._get_value(locator)

    def choose_file(self, locator, file_path):
        if not os.path.isfile(file_path):
            self._info("File '%s' does not exist on the local file system"
                        % file_path)
        self._element_find(locator, True, True).send_keys(file_path)

    def click_image(self, locator):
        self._info("Clicking image '%s'." % locator)
        element = self._element_find(locator, True, False, 'image')
        if element is None:
            # A form may have an image as it's submit trigger.
            element = self._element_find(locator, True, True, 'input')
        element.click()

    def frame_should_contain(self, locator, text, loglevel='INFO'):
        if not self._frame_contains(locator, text):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def unselect_frame(self):
        self._current_browser().switch_to_default_content()

    def select_frame(self, locator):
        self._info("Selecting frame '%s'." % locator)
        element = self._element_find(locator, True, True, tag='frame')
        self._current_browser().switch_to_frame(element)

    def current_frame_contains(self, text, logLevel='INFO'):
        if not self._is_text_present(text):
            self.log_source(loglevel)
            raise AssertionError("Page should have contained text '%s' "
                                 "but did not" % text)
        self._info("Current page contains text '%s'." % text)

    def get_alert_message(self):
        return self._close_alert()

    def alert_should_be_present(self, text=''):
        alert_text = self.get_alert_message()
        if text and alert_text != text:
            raise AssertionError("Alert text should have been '%s' but was '%s'"
                                  % (text, alert_text))

    def mouse_down_on_image(self, locator):
        element = self._element_find(locator, True, True, 'image')
        ActionChains(self._current_browser()).click_and_hold(element).perform()

    def mouse_down_on_link(self, locator):
        element = self._element_find(locator, True, True, 'link')
        ActionChains(self._current_browser()).click_and_hold(element).perform()

    def confirm_action(self):
        text = self._close_alert(not self._cancel_on_next_confirmation)
        self._cancel_on_next_confirmation = False
        return text

    def choose_cancel_on_next_confirmation(self):
        self._cancel_on_next_confirmation = True

    def choose_ok_on_next_confirmation(self):
        self._cancel_on_next_confirmation = False

    def execute_javascript(self, *code):
        js = self._get_javascript_to_execute(''.join(code))
        self._info("Executing JavaScript:\n%s" % js)
        return self._current_browser().execute_script(js)

    def open_context_menu(self, locator):
        element = self._element_find(locator, True, True)
        ActionChains(self._current_browser()).context_click(element).perform()

    def get_list_items(self, locator):
        select, options = self._get_select_list_options(locator)
        return self._get_labels_for_options(options)

    def get_selected_list_value(self, locator):
        values = self.get_selected_list_values(locator)
        if len(values) == 0: return None
        return values[0]

    def get_selected_list_values(self, locator):
        select, options = self._get_select_list_options_selected(locator)
        return self._get_values_for_options(options)

    def get_selected_list_label(self, locator):
        labels = self.get_selected_list_labels(locator)
        if len(labels) == 0: return None
        return labels[0]

    def get_selected_list_labels(self, locator):
        select, options = self._get_select_list_options_selected(locator)
        return self._get_labels_for_options(options)

    def _select_option_from_single_select_list(self, select, options, index):
        select.click()
        options[index].click()

    def _select_option_from_multi_select_list(self, select, options, index):
        if not options[index].is_selected():
            options[index].click()

    def _unselect_option_from_multi_select_list(self, select, options, index):
        if options[index].is_selected():
            options[index].click()

    def _unselect_all_options_from_multi_select_list(self, select):
        self._current_browser().execute_script("arguments[0].selectedIndex = -1;", select)

    def select_from_list(self, locator, *items):
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self._info("Selecting %s from list '%s'." % (items_str, locator))
        items = list(items)

        select, options = self._get_select_list_options(locator)
        is_multi_select = self._is_multiselect_list(select)
        select_func = self._select_option_from_multi_select_list if is_multi_select else self._select_option_from_single_select_list

        if not items:
            for i in range(len(options)):
                select_func(select, options, i)
            return

        option_values = self._get_values_for_options(options)
        option_labels = self._get_labels_for_options(options)
        for item in items:
            option_index = None
            try: option_index = option_values.index(item)
            except:
                try: option_index = option_labels.index(item)
                except: continue
            select_func(select, options, option_index)

    def unselect_from_list(self, locator, *items):
        items_str = items and "option(s) '%s'" % ", ".join(items) or "all options"
        self._info("Unselecting %s from list '%s'." % (items_str, locator))
        items = list(items)

        select = self._get_select_list(locator)
        if not self._is_multiselect_list(select):
            raise RuntimeError("Keyword 'Unselect from list' works only for multiselect lists.")

        if not items:
            self._unselect_all_options_from_multi_select_list(select)
            return

        select, options = self._get_select_list_options(select)
        option_values = self._get_values_for_options(options)
        option_labels = self._get_labels_for_options(options)
        for item in items:
            option_index = None
            try: option_index = option_values.index(item)
            except:
                try: option_index = option_labels.index(item)
                except: continue
            self._unselect_option_from_multi_select_list(select, options, option_index)

    def select_all_from_list(self, locator):
        self._info("Selecting all options from list '%s'." % locator)

        select = self._get_select_list(locator)
        if not self._is_multiselect_list(select):
            raise RuntimeError("Keyword 'Select all from list' works only for multiselect lists.")

        select, options = self._get_select_list_options(select)
        for i in range(len(options)):
            self._select_option_from_multi_select_list(select, options, i)

    def list_selection_should_be(self, locator, *items):
        items_str = items and "option(s) [ %s ]" % " | ".join(items) or "no options"
        self._info("Verifying list '%s' has %s selected." % (locator, items_str))
        items = list(items)
        self.page_should_contain_list(locator)
        select, options = self._get_select_list_options_selected(locator)
        if not items and len(options) == 0:
            return
        selected_values = self._get_values_for_options(options)
        selected_labels = self._get_labels_for_options(options)
        err = "List '%s' should have had selection [ %s ] but it was [ %s ]" \
            % (locator, ' | '.join(items), ' | '.join(selected_labels))
        for item in items:
            if item not in selected_values + selected_labels:
                raise AssertionError(err)
        for selected_value, selected_label in zip(selected_values, selected_labels):
            if selected_value not in items and selected_label not in items:
                raise AssertionError(err)

    def list_should_have_no_selections(self, locator):
        self._info("Verifying list '%s' has no selection." % locator)
        select, options = self._get_select_list_options_selected(locator)
        if options:
            selected_labels = self._get_labels_for_options(options)
            items_str = " | ".join(selected_labels)
            raise AssertionError("List '%s' should have had no selection "
                                 "(selection was [ %s ])" % (locator, items_str))

    def mouse_over(self, locator):
        self._info("Simulating Mouse Over on element '%s'" % locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        ActionChains(self._current_browser()).move_to_element(element).perform()

    def mouse_out(self, locator):
        self._info("Simulating Mouse Out on element '%s'" % locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        size = element.size
        offsetx = (size['width'] / 2) + 1
        offsety = (size['height'] / 2) + 1
        ActionChains(self._current_browser()).move_to_element(element).move_by_offset(offsetx, offsety).perform()

    def mouse_down(self, locator):
        self._info("Simulating Mouse Down on element '%s'" % locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        ActionChains(self._current_browser()).click_and_hold(element).perform()

    def mouse_up(self, locator):
        self._info("Simulating Mouse Up on element '%s'" % locator)
        element = self._element_find(locator, True, False)
        if element is None:
            raise AssertionError("ERROR: Element %s not found." % (locator))
        ActionChains(self._current_browser()).click_and_hold(element).release(element).perform()

    def go_back(self):
        self._current_browser().back()

    def log_title(self):
        self._info(self.get_title())

    def log_url(self):
        self._info(self.get_url())

    def register_keyword_to_run_on_failure(self, keyword):
        old_keyword = self._run_on_failure_keyword
        old_keyword_text = old_keyword if old_keyword is not None else "No keyword"

        new_keyword = keyword if keyword.strip().lower() != "nothing" else None
        new_keyword_text = new_keyword if new_keyword is not None else "No keyword"

        self._run_on_failure_keyword = new_keyword
        self._info('%s will be run on failure.' % new_keyword_text)

        return old_keyword_text

    def capture_page_screenshot(self, filename=None):
        path, link = self._get_screenshot_paths(filename)
        self._current_browser().save_screenshot(path)

        # Image is shown on its own row and thus prev row is closed on purpose
        self._html('</td></tr><tr><td colspan="3"><a href="%s">'
                   '<img src="%s" width="800px"></a>' % (link, link))

    def input_password(self, locator, text):
        self._info("Typing password into text field '%s'" % locator)
        self._input_text_into_text_field(locator, text)

    def press_key(self, locator, key):
        if key.startswith('\\') and len(key) > 1:
            key = self._map_ascii_key_code_to_key(int(key[1:]))
        if len(key) > 1:
            raise ValueError("Key value '%s' is invalid.", key)
        element = self._element_find(locator, True, True)
        element.send_keys(key)

    def table_should_contain(self, table_locator, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_content(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Table identified by '%s' should have contained text '%s'." \
                % (table_locator, expected))

    def table_header_should_contain(self, table_locator, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_header(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Header in table identified by '%s' should have contained "
               "text '%s'." % (table_locator, expected))

    def table_footer_should_contain(self, table_locator, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_footer(self._current_browser(), table_locator, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Footer in table identified by '%s' should have contained "
                   "text '%s'." % (table_locator, expected))

    def table_row_should_contain(self, table_locator, row, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_row(self._current_browser(), table_locator, row, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Row #%s in table identified by '%s' should have contained "
                   "text '%s'." % (row, table_locator, expected))

    def table_column_should_contain(self, table_locator, col, expected, loglevel='INFO'):
        element = self._table_element_finder.find_by_col(self._current_browser(), table_locator, col, expected)
        if element is None:
            self.log_source(loglevel)
            raise AssertionError("Column #%s in table identified by '%s' "
                   "should have contained text '%s'."
                   % (col, table_locator, expected))

    def get_table_cell(self, table_locator, row, column, loglevel='INFO'):
        row = int(row) - 1
        column = int(column) - 1
        table = self._table_element_finder.find(self._current_browser(), table_locator)
        if table is not None:
            rows = table.find_elements_by_xpath('./tbody/tr')
            if row < len(rows):
                columns = rows[row].find_elements_by_tag_name('td')
                if column < len(columns):
                    return columns[column].text
        self.log_source(loglevel)
        raise AssertionError("Cell in table %s in row #%s and column #%s could not be found."
            % (table_locator, str(row), str(column)))

    def table_cell_should_contain(self, table_locator, row, column, expected, loglevel='INFO'):
        message = ("Cell in table '%s' in row #%s and column #%s "
                   "should have contained text '%s'."
                   % (table_locator, row, column, expected))
        try:
            content = self.get_table_cell(table_locator, row, column, loglevel='NONE')
        except AssertionError, err:
            self._warn(err)
            self.log_source(loglevel)
            raise AssertionError(message)
        self._info("Cell contains %s." % (content))
        if expected not in content:
            self.log_source(loglevel)
            raise AssertionError(message)

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

    def _input_text_into_text_field(self, locator, text):
        element = self._element_find(locator, True, True)
        element.clear()
        element.send_keys(text)

    def _get_screenshot_paths(self, filename):
        if not filename:
            self._screenshot_index += 1
            filename = 'selenium-screenshot-%d.png' % self._screenshot_index
        else:
            filename = filename.replace('/', os.sep)
        logdir = self._get_log_dir()
        path = os.path.join(logdir, filename)
        link = robot.utils.get_link_path(path, logdir)
        return path, link

    def _run_on_failure(self):
        if self._run_on_failure_keyword is not None:
            BUILTIN.run_keyword(self._run_on_failure_keyword)

    def _is_multiselect_list(self, select):
        multiple_value = select.get_attribute('multiple')
        if multiple_value is not None and (multiple_value == 'true' or multiple_value == 'multiple'):
            return True
        return False

    def _get_select_list(self, locator):
        return self._element_find(locator, True, True, 'select')

    def _get_select_list_options(self, select_list_or_locator):
        if isinstance(select_list_or_locator, WebElement):
            select = select_list_or_locator
        else:
            select = self._get_select_list(select_list_or_locator)
        return select, select.find_elements_by_tag_name('option')

    def _get_select_list_options_selected(self, select_list_or_locator):
        select, options = self._get_select_list_options(select_list_or_locator)
        selected = []
        for option in options:
            if option.is_selected():
                selected.append(option)
        return select, selected
    
    def _get_labels_for_options(self, options):
        labels = []
        for option in options:
            labels.append(option.text)
        return labels
    
    def _get_values_for_options(self, options):
        values = []
        for option in options:
             values.append(option.get_attribute('value'))
        return values

    def _get_javascript_to_execute(self, code):
        codepath = code.replace('/', os.sep)
        if not (os.path.isabs(codepath) and os.path.isfile(codepath)):
            return code
        self._html('Reading JavaScript from file <a href="file://%s">%s</a>.'
                   % (codepath.replace(os.sep, '/'), codepath))
        codefile = open(codepath)
        try:
            return codefile.read().strip()
        finally:
            codefile.close()

    def _close_alert(self, confirm=False):
        alert = None
        try:
            alert = self._current_browser().switch_to_alert()
            text = ' '.join(alert.text.splitlines()) # collapse new lines chars
            if not confirm: alert.dismiss()
            else: alert.accept()
            return text
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _get_value(self, locator, tag=None):
        element = self._element_find(locator, True, False, tag=tag)
        return element.get_attribute('value') if element is not None else None

    def _parse_attribute_locator(self, attribute_locator):
        parts = attribute_locator.partition('@')
        if len(parts[0]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an element locator." % (locator))
        if len(parts[2]) == 0:
            raise ValueError("Attribute locator '%s' does not contain an attribute name." % (locator))
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
        locator = "xpath=//*[contains(., %s)]" % utils.escape_xpath_value(text);
        return self._is_element_present(locator)

    def _page_contains(self, text):
        browser = self._current_browser()
        browser.switch_to_default_content()

        if self._is_text_present(text):
            return True

        subframes = self._element_find("tag=frame", False, False, 'frame')
        self._debug('Current frame has %d subframes' % len(subframes))
        for frame in subframes:
            browser.switch_to_frame(frame)
            found_text = self._is_text_present(text)
            browser.switch_to_default_content()
            if found_text:
                return True

        return False

    def _frame_contains(self, locator, text):
        browser = self._current_browser()
        element = self._element_find(locator, True, True, 'frame')
        browser.switch_to_frame(element)
        self._info("Searching for text from frame '%s'." % locator)
        found = self._is_text_present(text)
        browser.switch_to_default_content()
        return found

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
            raise ValueError("Element locator '" + locator + "' did not match any elements.")
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
            raise ValueError(browser_name + " is not a supported browser.")

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
        level = level.upper()
        if (level == 'INFO'): self._info(message)
        elif (level == 'DEBUG'): self._debug(message)
        elif (level == 'WARN'): self._warn(message)
        elif (level == 'HTML'): self._html(message)

    def _info(self, message):
        logger.info(message)

    def _debug(self, message):
        logger.debug(message)

    def _warn(self, message):
        logger.warn(message)

    def _html(self, message):
        logger.info(message, True, False)
