import time
import robot
from keywordgroup import KeywordGroup

class _WaitingKeywords(KeywordGroup):

    # Public

    def wait_for_condition(self, condition, timeout=None, error=None):
        if not error:
            error = "Condition '%s' did not become true in <TIMEOUT>" % condition
        self._wait_until(timeout, error,
                         lambda: self._current_browser().execute_script(condition) == True)

    def wait_until_page_contains(self, text, timeout=None, error=None):
        if not error:
            error = "Text '%s' did not appear in <TIMEOUT>" % text
        self._wait_until(timeout, error, self._is_text_present, text)

    def wait_until_page_contains_element(self, locator, timeout=None, error=None):
        if not error:
            error = "Element '%s' did not appear in <TIMEOUT>" % locator
        self._wait_until(timeout, error, self._is_element_present, locator)

    # Private

    def _wait_until(self, timeout, error, function, *args):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        error = error.replace('<TIMEOUT>', robot.utils.secs_to_timestr(timeout))
        maxtime = time.time() + timeout
        while not function(*args):
            if time.time() > maxtime:
                raise AssertionError(error)
            time.sleep(0.2)