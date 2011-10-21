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

        `code` may contain multiple lines of code but must contain a 
        return statement (with the value to be returned) at the end.

        `code` may be divided into multiple cells in the test data. In that
        case, the parts are catenated together without adding spaces.

        If `code` is an absolute path to an existing file, the JavaScript
        to execute will be read from that file. Forward slashes work as
        a path separator on all operating systems.

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
        return self._current_browser().execute_script(js)

    def get_alert_message(self):
        """Returns the text of current JavaScript alert.

        This keyword will fail if no alert is present. Note that
        following keywords will fail unless the alert is
        dismissed by this keyword or another like `Get Alert Message`.
        """
        return self._close_alert()

    # Private

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