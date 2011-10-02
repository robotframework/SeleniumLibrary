from robot import utils
from types import *

class WindowSelector(object):

    def __init__(self):
        self._strategies = {
            'title': self._select_by_title,
            'name': self._select_by_name,
            'url': self._select_by_url,
            None: self._select_by_default
        }
        self._title_matcher = lambda browser, criteria: browser.get_title().strip().lower() == criteria.lower()
        self._name_matcher = lambda browser, criteria: browser.get_current_window_handle().strip() == criteria
        self._url_matcher = lambda browser, criteria: browser.get_current_url().strip().lower() == criteria.lower()

    def select(self, browser, locator):
        assert browser is not None

        (prefix, criteria) = self._parse_locator(locator)
        strategy = self._strategies.get(prefix)
        if strategy is None:
            raise ValueError("Window locator with prefix '" + prefix + "' is not supported")
        return strategy(browser, criteria)

    # Strategy routines, private

    def _select_by_title(self, browser, criteria):
        self._select_matching(browser, criteria, self._title_matcher,
            "Could not find window with title '" + criteria + "'")

    def _select_by_name(self, browser, criteria):
        self._select_matching(browser, criteria, self._name_matcher,
            "Could not find window with name '" + criteria + "'")

    def _select_by_url(self, browser, criteria):
        self._select_matching(browser, criteria, self._url_matcher,
            "Could not find window with URL '" + criteria + "'")

    def _select_by_default(self, browser, criteria):
        if criteria is None or len(criteria) == 0 or criteria.lower() == "null":
            browser.switch_to_window(None)
            return
        if self._try_select_matching(browser, criteria, self._name_matcher):
            return
        if self._try_select_matching(browser, criteria, self._title_matcher):
            return
        raise ValueError("Could not find window with name or title '" + criteria + "'")

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

    def _select_matching(self, browser, criteria, matcher, error):
        if not self._try_select_matching(browser, criteria, matcher):
            raise ValueError(error)

    def _try_select_matching(self, browser, criteria, matcher):
        starting_handle = browser.get_current_window_handle()
        for handle in browser.get_window_handles():
            browser.switch_to_window(handle)
            if matcher(browser, criteria):
                return True
        browser.switch_to_window(starting_handle)
        return False
