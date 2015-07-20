import os
from selenium.common.exceptions import WebDriverException
from keywordgroup import KeywordGroup

class _JavaScriptKeywords(KeywordGroup):

    def __init__(self):
        self._cancel_on_next_confirmation = False

    # Public

    def alert_should_be_present(self, text=''):
        """Verifies an alert is present and dismisses it.

        If `text` is a non-empty string, then it is also verified that the
        message of the alert equals to `text`.

        Will fail if no alert is present. Note that following keywords
        will fail unless the alert is dismissed by this
        keyword or another like `Get Alert Message`.
        """
        alert_text = self.get_alert_message()
        if text and alert_text != text:
            raise AssertionError("Alert text should have been '%s' but was '%s'"
                                  % (text, alert_text))

    def choose_cancel_on_next_confirmation(self):
        """Cancel will be selected the next time `Confirm Action` is used."""
        self._cancel_on_next_confirmation = True

    def choose_ok_on_next_confirmation(self):
        """Undo the effect of using keywords `Choose Cancel On Next Confirmation`. Note
        that Selenium's overridden window.confirm() function will normally automatically
        return true, as if the user had manually clicked OK, so you shouldn't
        need to use this command unless for some reason you need to change
        your mind prior to the next confirmation. After any confirmation, Selenium will resume using the
        default behavior for future confirmations, automatically returning 
        true (OK) unless/until you explicitly use `Choose Cancel On Next Confirmation` for each
        confirmation.
        
        Note that every time a confirmation comes up, you must
        consume it by using a keywords such as `Get Alert Message`, or else
        the following selenium operations will fail.
        """
        self._cancel_on_next_confirmation = False

    def confirm_action(self):
        """Dismisses currently shown confirmation dialog and returns it's message.

        By default, this keyword chooses 'OK' option from the dialog. If
        'Cancel' needs to be chosen, keyword `Choose Cancel On Next
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
        text = self._close_alert(not self._cancel_on_next_confirmation)
        self._cancel_on_next_confirmation = False
        return text

    def execute_javascript(self, *code):
        """Executes the given JavaScript code.

        `code` may contain multiple lines of code and may be divided into
        multiple cells in the test data. In that case, the parts are
        catenated together without adding spaces.

        If `code` is an absolute path to an existing file, the JavaScript
        to execute will be read from that file. Forward slashes work as
        a path separator on all operating systems.

        The JavaScript executes in the context of the currently selected
        frame or window as the body of an anonymous function. Use _window_ to
        refer to the window of your application and _document_ to refer to the
        document object of the current frame or window, e.g.
        _document.getElementById('foo')_.

        This keyword returns None unless there is a return statement in the
        JavaScript. Return values are converted to the appropriate type in
        Python, including WebElements.

        Examples:
        | Execute JavaScript | window.my_js_function('arg1', 'arg2') |               |
        | Execute JavaScript | ${CURDIR}/js_to_execute.js            |               |
        | ${sum}=            | Execute JavaScript                    | return 1 + 1; |
        | Should Be Equal    | ${sum}                                | ${2}          |
        """
        js = self._get_javascript_to_execute(''.join(code))
        self._info("Executing JavaScript:\n%s" % js)
        return self._current_browser().execute_script(js)

    def execute_async_javascript(self, *code):
        """Executes asynchronous JavaScript code.

        Similar to `Execute Javascript` except that scripts executed with
        this keyword must explicitly signal they are finished by invoking the
        provided callback. This callback is always injected into the executed
        function as the last argument.

        Scripts must complete within the script timeout or this keyword will
        fail. See the `Timeouts` section for more information.

        Examples:
        | Execute Async JavaScript | var callback = arguments[arguments.length - 1]; | window.setTimeout(callback, 2000); |
        | Execute Async JavaScript | ${CURDIR}/async_js_to_execute.js                |                                    |
        | ${retval}=               | Execute Async JavaScript                        |                                    |
        | ...                      | var callback = arguments[arguments.length - 1]; |                                    |
        | ...                      | function answer(){callback("text");};           |                                    |
        | ...                      | window.setTimeout(answer, 2000);                |                                    |
        | Should Be Equal          | ${retval}                                       | text                               |
        """
        js = self._get_javascript_to_execute(''.join(code))
        self._info("Executing Asynchronous JavaScript:\n%s" % js)
        return self._current_browser().execute_async_script(js)

    def get_alert_message(self, dismiss=True):
        """Returns the text of current JavaScript alert.

        By default the current JavaScript alert will be dismissed.
        This keyword will fail if no alert is present. Note that
        following keywords will fail unless the alert is
        dismissed by this keyword or another like `Get Alert Message`.
        """
        if dismiss:
            return self._close_alert()
        else:
            return self._read_alert()

    def dismiss_alert(self, accept=True):
        """ Returns true if alert was confirmed, false if it was dismissed

        This keyword will fail if no alert is present. Note that
        following keywords will fail unless the alert is
        dismissed by this keyword or another like `Get Alert Message`.
        """
        return self._handle_alert(accept)

    # Private

    def _close_alert(self, confirm=True):
        try:
            text = self._read_alert()
            alert = self._handle_alert(confirm)
            return text
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _read_alert(self):
        alert = None
        try:
            alert = self._current_browser().switch_to_alert()
            text = ' '.join(alert.text.splitlines()) # collapse new lines chars
            return text
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _handle_alert(self, confirm=True):
        try:
            alert = self._current_browser().switch_to_alert()
            if not confirm:
                alert.dismiss()
                return False
            else:
                alert.accept()
                return True
        except WebDriverException:
            raise RuntimeError('There were no alerts')

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