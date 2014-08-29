import time
import robot
from keywordgroup import KeywordGroup

class _WaitingKeywords(KeywordGroup):

    # Public

    def wait_for_condition(self, condition, timeout=None, error=None):
        """Waits until the given `condition` is true or `timeout` expires.

        The `condition` can be arbitrary JavaScript expression but must contain a 
        return statement (with the value to be returned) at the end.
        See `Execute JavaScript` for information about accessing the
        actual contents of the window through JavaScript.

        `error` can be used to override the default error message.

        See `introduction` for more information about `timeout` and its
        default value.

        See also `Wait Until Page Contains`, `Wait Until Page Contains
        Element`, `Wait Until Element Is Visible` and BuiltIn keyword
        `Wait Until Keyword Succeeds`.
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

        See also `Wait Until Page Contains Element`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until
        Keyword Succeeds`.
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

        See also `Wait Until Page Contains`, `Wait For Condition`,
        `Wait Until Element Is Visible` and BuiltIn keyword `Wait Until
        Keyword Succeeds`.
        """
        if not error:
            error = "Element '%s' did not appear in <TIMEOUT>" % locator
        self._wait_until(timeout, error, self._is_element_present, locator)

    def wait_until_element_is_visible(self, locator, timeout=None, error=None):
        """Waits until element specified with `locator` is visible.

        Fails if `timeout` expires before the element is visible. See
        `introduction` for more information about `timeout` and its
        default value.

        `error` can be used to override the default error message.

        See also `Wait Until Page Contains`, `Wait Until Page Contains 
        Element`, `Wait For Condition` and BuiltIn keyword `Wait Until Keyword
        Succeeds`.
        """
        def check_visibility():
            visible = self._is_visible(locator)
            if visible:
                return
            elif visible is None:
                return error or "Element locator '%s' did not match any elements after %s" % (locator, self._format_timeout(timeout))
            else:
                return error or "Element '%s' was not visible in %s" % (locator, self._format_timeout(timeout))
        self._wait_until_no_error(timeout, check_visibility)

    # Private

    def _wait_until(self, timeout, error, function, *args):
        error = error.replace('<TIMEOUT>', self._format_timeout(timeout))
        def wait_func():
            return None if function(*args) else error
        self._wait_until_no_error(timeout, wait_func)

    def _wait_until_no_error(self, timeout, wait_func, *args):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        maxtime = time.time() + timeout
        while True:
            timeout_error = wait_func(*args)
            if not timeout_error: return
            if time.time() > maxtime:
                raise AssertionError(timeout_error)
            time.sleep(0.2)

    def _format_timeout(self, timeout):
        timeout = robot.utils.timestr_to_secs(timeout) if timeout is not None else self._timeout_in_secs
        return robot.utils.secs_to_timestr(timeout)
