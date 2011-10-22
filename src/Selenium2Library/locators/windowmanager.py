from types import *
from robot import utils
from selenium.common.exceptions import NoSuchWindowException

class WindowManager(object):

    def __init__(self):
        self._strategies = {
            'title': self._select_by_title,
            'name': self._select_by_name,
            'url': self._select_by_url,
            None: self._select_by_default
        }

    def get_window_handles(self, browser):
        return browser.get_window_handles()

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
            lambda browser: browser.get_title().strip().lower() == criteria.lower(),
            "Unable to locate window with title '" + criteria + "'")

    def _select_by_name(self, browser, criteria):
        try:
            browser.switch_to_window(criteria)
        except NoSuchWindowException:
            raise ValueError("Unable to locate window with name '" + criteria + "'")

    def _select_by_url(self, browser, criteria):
        self._select_matching(
            browser,
            lambda browser: browser.get_current_url().strip().lower() == criteria.lower(),
            "Unable to locate window with URL '" + criteria + "'")

    def _select_by_default(self, browser, criteria):
        if criteria is None or len(criteria) == 0 or criteria.lower() == "null":
            browser.switch_to_window('')
            return

        try:
            self._select_by_name(browser, criteria)
            return
        except ValueError: pass

        try:
            self._select_by_title(browser, criteria)
            return
        except ValueError: pass

        raise ValueError("Unable to locate window with name or title '" + criteria + "'")

    # Private

    def _parse_locator(self, locator):
        prefix = None
        criteria = locator
        if locator is not None and len(locator) > 0:
            locator_parts = locator.partition('=')        
            if len(locator_parts[1]) > 0:
                prefix = locator_parts[0].strip().lower()
                criteria = locator_parts[2].strip()
        return (prefix, criteria)

    def _select_matching(self, browser, matcher, error):
        starting_handle = browser.get_current_window_handle()
        for handle in browser.get_window_handles():
            browser.switch_to_window(handle)
            if matcher(browser):
                return
        browser.switch_to_window(starting_handle)
        raise ValueError(error)
