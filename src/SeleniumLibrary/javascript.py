#  Copyright 2008-2010 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import time
import os.path

from robot import utils


class JavaScript(object):

    def execute_javascript(self, *code):
        """Executes the given JavaScript code.

        `code` may contain multiple statements and the return value of last
        statement is returned by this keyword.

        `code` may be divided into multiple cells in the test data. In that
        case, the parts are catenated together without adding spaces.

        If `code` is an absolute path to an existing file, the JavaScript
        to execute will be read from that file. Forward slashes work as
        a path separator on all operating systems. The functionality to
        read the code from a file was added in SeleniumLibrary 2.5.

        Note that, by default, the code will be executed in the context of the
        Selenium object itself, so `this` will refer to the Selenium object.
        Use `window` to refer to the window of your application, e.g.
        `window.document.getElementById('foo')`.

        Example:
        | Execute JavaScript | window.my_js_function('arg1', 'arg2') |
        | Execute JavaScript | ${CURDIR}/js_to_execute.txt |
        """
        js = self._get_javascript_to_execute(''.join(code))
        self._info("Executing JavaScript:\n\n%s" % js)
        return self._selenium.get_eval(js)

    def _get_javascript_to_execute(self, code):
        codepath = code.replace('/', os.sep)
        if not (os.path.isabs(codepath) and os.path.isfile(codepath)):
            return code
        codefile = open(codepath)
        try:
            return codefile.read().strip()
        finally:
            codefile.close()

    def get_alert_message(self):
        """Returns the text of current JavaScript alert.

        This keyword will fail if no alert is present. Note that when running
        tests with selenium, the alerts will not be visible in the browser.
        Nevertheless, following keywords will fail unless the alert is
        dismissed by this keyword or by `Alert Should Be Present`.
        """
        try:
            return self._selenium.get_alert()
        except Exception, err:
            if self._error_contains(err, 'alerts'):
                raise RuntimeError('There were no alerts')
            raise

    def alert_should_be_present(self, text=''):
        """Verifies an alert is present and dismisses it.

        If `text` is a non-empty string, then it is also verified that the
        message of the alert equals to `text`.

        Will fail if no alert is present. Note that when running tests with
        selenium, the alerts will not be visible in the browser. Nevertheless,
        following keywords will fail unless the alert is dismissed by this
        keyword or by `Get Alert Message`.
        """
        alert_text = self.get_alert_message()
        if text and alert_text != text:
            raise AssertionError("Alert text should have been '%s' but was '%s'"
                                  % (text, alert_text))

    def confirm_action(self):
        """Dismisses currently shown confirmation dialog and returns it's message.

        By default, this keyword chooses 'Ok' option from the dialog. If
        'cancel' needs to be chosen, keyword `Choose Cancel On Next
        Confirmation` must be called before the action that causes the
        confirmation dialog to be shown.

        Examples:

        | Click Button | Send | # Shows a confirmation dialog |
        | ${message}= | Confirm Action | # Chooses Ok |
        | Should Be Equal | ${message} | Are your sure? |
        |                |    |              |
        | Choose Cancel On Next Confirmation | | |
        | Click Button | Send | # Shows a confirmation dialog |
        | Confirm Action |    | # Chooses Cancel |
        """
        return self._selenium.get_confirmation()

    def choose_cancel_on_next_confirmation(self):
        """Cancel will be selected the next time `Confirm Action` is used.
        """
        self._selenium.choose_cancel_on_next_confirmation()

    def simulate(self, locator, event):
        """Simulates `event` on component identified by `locator`.

        This keyword is useful if component has OnEvent handler that needs to be
        explicitly invoked.

        See `introduction` for details about locating elements.
        """
        self._selenium.fire_event(self._parse_locator(locator), event)

    def mouse_down_on_image(self, locator):
        """Simulates a mouse down event on an image.

        Key attributes for images are `id`, `src` and `alt`. See
        `introduction` for details about locating elements.
        """
        self._selenium.mouse_down(self._parse_locator(locator, 'image'))

    def mouse_down_on_link(self, locator):
        """Simulates a mouse down event on a link.

        Key attributes for links are `id`, `name`, `href` and link text. See
        `introduction` for details about locating elements.
        """
        self._selenium.mouse_down(self._parse_locator(locator, 'link'))

    def wait_for_condition(self, condition, timeout='5 seconds', error=None):
        """Waits either for given condition to be true or until timeout expires.

        `condition` can be arbitrary JavaScript expression. It can be multiple
        lines, but only the statement in the last line is used for evaluation.

        `timeout` must given using Robot Framework time syntax, see
        http://robotframework.googlecode.com/svn/trunk/doc/userguide/RobotFrameworkUserGuide.html#time-format.

        `error` can be used to override the default error message.
        New in version 2.2.3.

        See `Execute JavaScript` for information about accessing the
        actual contents of the window through JavaScript.
        """
        if not error:
            error = "Condition '%s' did not become true in %s" \
                    % (condition, timeout)
        self._info("Waiting %s for condition '%s' to be true."
                   % (timeout, condition))
        self._wait_until(lambda: self._selenium.get_eval(condition) == 'true',
                         utils.timestr_to_secs(timeout), error)

    def _wait_until(self, callable, timeout, error):
        maxtime = time.time() + timeout
        while not callable():
            if time.time() > maxtime:
                raise AssertionError(error)
            time.sleep(0.2)

    def wait_until_page_contains(self, text, timeout, error=None):
        """Waits until `text` appears on current page or `timeout` expires.

        `timeout` must given using Robot Framework time syntax, see
        http://robotframework.googlecode.com/svn/trunk/doc/userguide/RobotFrameworkUserGuide.html#time-format.

        `error` can be used to override the default error message.
        New in version 2.2.3.

        Robot Framework built-in keyword `Wait Until Keyword Succeeds` can be used
        to get this kind of functionality for any Selenium keyword.
        """
        if not error:
            error = "Text '%s' did not appear in '%s'" % (text, timeout)
        self._wait_until(lambda: self._selenium.is_text_present(text),
                         utils.timestr_to_secs(timeout), error)

    def wait_until_page_contains_element(self, locator, timeout, error=None):
        """Waits until element specified with `locator` appears on current page or `timeout` expires.

        `timeout` must given using Robot Framework time syntax, see
        http://robotframework.googlecode.com/svn/trunk/doc/userguide/RobotFrameworkUserGuide.html#time-format.

        `error` can be used to override the default error message.

        This keyword was added in SeleniumLibrary 2.2.3.

        Robot Framework built-in keyword `Wait Until Keyword Succeeds` can be used
        to get this kind of functionality for any Selenium keyword.
        """
        if not error:
            error = "Element '%s' did not appear in '%s'" % (locator, timeout)
        locator = self._parse_locator(locator)
        self._wait_until(lambda: self._selenium.is_element_present(locator),
                         utils.timestr_to_secs(timeout), error)

    def open_context_menu(self, locator, offset=None):
        """Opens context menu on element identified by `locator`."""
        locator = self._parse_locator(locator)
        if offset:
            self._selenium.context_menu_at(locator, offset)
        else:
            self._selenium.context_menu(locator)
