from types import *
from robot import utils
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import NoSuchWindowException

class WindowManager(object):

    def __init__(self):
        self._strategies = {
            'title': self._select_by_title,
            'name': self._select_by_name,
            'url': self._select_by_url,
            None: self._select_by_default
        }

    def get_window_ids(self, browser):
        return [ window_info[1] for window_info in self._get_window_infos(browser) ]

    def get_window_names(self, browser):
        return [ window_info[2] for window_info in self._get_window_infos(browser) ]

    def get_window_titles(self, browser):
        return [ window_info[3] for window_info in self._get_window_infos(browser) ]

    def select(self, browser, locator):
        assert browser is not None

        (prefix, criteria) = self._parse_locator(locator)
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Window locator with prefix '" + prefix + "' is not supported")
        return strategy(browser, criteria)

    # Strategy routines, private

    def _select_by_title(self, browser, criteria):
        self._select_matching(
            browser,
            lambda window_info: window_info[3].strip().lower() == criteria.lower(),
            "Unable to locate window with title '" + criteria + "'")

    def _select_by_name(self, browser, criteria):
        self._select_matching(
            browser,
            lambda window_info: window_info[2].strip().lower() == criteria.lower(),
            "Unable to locate window with name '" + criteria + "'")

    def _select_by_url(self, browser, criteria):
        self._select_matching(
            browser,
            lambda window_info: window_info[4].strip().lower() == criteria.lower(),
            "Unable to locate window with URL '" + criteria + "'")

    def _select_by_default(self, browser, criteria):
        if type(criteria) == list:
            for handle in browser.get_window_handles():
                if handle not in criteria:
                    browser.switch_to_window(handle)
                    return
            raise ValueError("Unable to locate new window")
        if criteria.lower() == "self":
            return
        if criteria is None or len(criteria) == 0 or criteria.lower() == "null":
            browser.switch_to_window(browser.get_window_handles()[0])
            return
        if criteria.lower() == "new" or criteria.lower() == "popup":
            try:
                start_handle = browser.get_current_window_handle()
            except NoSuchWindowException:
                 raise AssertionError("No current window. where are you making a popup window?")
            handles = browser.get_window_handles()
            if len(handles) < 2 or handles[-1] == start_handle:
               raise AssertionError("No new window found to select")
            browser.switch_to_window(handles[-1])
            return
        for handle in browser.get_window_handles():
            browser.switch_to_window(handle)
            if criteria == handle:
                return
            for item in browser.get_current_window_info()[2:4]:
                if item.strip().lower() == criteria.lower():
                    return
        raise ValueError("Unable to locate window with handle or name or title or URL '" + criteria + "'")

    # Private

    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if type(locator) == list:
            return (prefix, criteria)
        if locator is not None and len(locator) > 0:
            locator_parts = locator.partition('=')        
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
        if prefix is None or prefix == 'name':
            if criteria is None or criteria.lower() == 'main':
                criteria = ''
        return (prefix, criteria)

    def _get_window_infos(self, browser):
        window_infos = []
        try:
            starting_handle = browser.get_current_window_handle()
        except NoSuchWindowException:
            starting_handle = None
        try:
            for handle in browser.get_window_handles():
                browser.switch_to_window(handle)
                window_infos.append(browser.get_current_window_info())
        finally:
            if starting_handle:
                browser.switch_to_window(starting_handle)
        return window_infos

    def _select_matching(self, browser, matcher, error):
        try:
            starting_handle = browser.get_current_window_handle()
        except NoSuchWindowException:
            starting_handle = None
        for handle in browser.get_window_handles():
            browser.switch_to_window(handle)
            if matcher(browser.get_current_window_info()):
                return
        if starting_handle:
            browser.switch_to_window(starting_handle)
        raise ValueError(error)
