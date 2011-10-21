import time
import robot
from keywordgroup import KeywordGroup

class _WaitingKeywords(KeywordGroup):

    # Public

    def wait_for_condition(self, condition, timeout=None, error=None):
        """Waits until the given `condition` is true or `timeout` expires.

        `code` may contain multiple lines of code but must contain a 
        return statement (with the value to be returned) at the end

        The `condition` can be arbitrary JavaScript expression but must contain a 
        return statement (with the value to be returned) at the end.
        See `Execute JavaScript` for information about accessing the
        actual contents of the window through JavaScript.

        `error` can be used to override the default error message.

        See `introduction` for more information about `timeout` and its
        default value.

        See also `Wait Until Page Contains`, `Wait Until Page Contains
        Element` and BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Condition '%s' did not become true in <TIMEOUT>" % condition
        self._wait_until(timeout, error,
                         lambda: self._current_browser().execute_script(condition) == True)

    def wait_until_page_contains(self, text, timeout=None, error=None):
        """Waits until `text` appears on current page.

        Fails if `timeout` expires before the text appears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains Element`, `Wait For Condition` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Text '%s' did not appear in <TIMEOUT>" % text
        self._wait_until(timeout, error, self._is_text_present, text)

    def wait_until_page_contains_element(self, locator, timeout=None, error=None):
        """Waits until element specified with `locator` appears on current page.

        Fails if `timeout` expires before the element appears. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains`, `Wait For Condition` and
        BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
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