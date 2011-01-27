#  Copyright 2008-2011 Nokia Siemens Networks Oyj
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

import os.path

from runonfailure import RunOnFailure


class JavaScript(RunOnFailure):

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
        | Execute JavaScript | ${CURDIR}/js_to_execute.js |
        """
        js = self._get_javascript_to_execute(''.join(code))
        self._info("Executing JavaScript:\n%s" % js)
        return self._selenium.get_eval(js)

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
        """Cancel will be selected the next time `Confirm Action` is used."""
        self._selenium.choose_cancel_on_next_confirmation()

    def wait_for_condition(self, condition, timeout=None, error=None):
        """Waits until the given `condition` is true or `timeout` expires.

        The `condition` can be arbitrary JavaScript expression. It can
        be multiple lines, but only the statement in the last line is
        used for evaluation. See `Execute JavaScript` for information
        about accessing the actual contents of the window through
        JavaScript.

        `error` can be used to override the default error message.

        See `introduction` for more information about `timeout` and its
        default value.

        See also `Wait Until Page Contains`, `Wait Until Page Contains
        Element` and BuiltIn keyword `Wait Until Keyword Succeeds`.
        """
        if not error:
            error = "Condition '%s' did not become true in %%(timeout)s" \
                % condition
        self._wait_until(lambda: self._selenium.get_eval(condition) == 'true',
                         error, timeout)
