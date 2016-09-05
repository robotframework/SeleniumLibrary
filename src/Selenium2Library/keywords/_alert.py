from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from keywordgroup import KeywordGroup


class _AlertKeywords(KeywordGroup):

    def __init__(self):
        self._cancel_on_next_confirmation = False

    # Public

    def input_text_into_prompt(self, text):
        """Types the given `text` into alert box.  """
        alert = None
        try:
            alert = self._wait_alert()
            alert.send_keys(text)
        except WebDriverException:
            raise RuntimeError('There were no alerts')

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
            raise AssertionError("Alert text should have been "
                                 "'%s' but was '%s'"
                                 % (text, alert_text))

    def choose_cancel_on_next_confirmation(self):
        """Cancel will be selected the next time `Confirm Action` is used."""
        self._cancel_on_next_confirmation = True

    def choose_ok_on_next_confirmation(self):
        """Undo the effect of using keywords `Choose Cancel On Next Confirmation`. Note
        that Selenium's overridden window.confirm() function will normally
        automatically return true, as if the user had manually clicked OK, so
        you shouldn't need to use this command unless for some reason you need
        to change your mind prior to the next confirmation. After any
        confirmation, Selenium will resume using the default behavior for
        future confirmations, automatically returning true (OK) unless/until
        you explicitly use `Choose Cancel On Next Confirmation` for each
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
            self._handle_alert(confirm)
            return text
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _read_alert(self):
        alert = None
        try:
            alert = self._wait_alert()
            # collapse new lines chars
            return ' '.join(alert.text.splitlines())
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _handle_alert(self, confirm=True):
        try:
            alert = self._wait_alert()
            if not confirm:
                alert.dismiss()
                return False
            else:
                alert.accept()
                return True
        except WebDriverException:
            raise RuntimeError('There were no alerts')

    def _wait_alert(self):
        return WebDriverWait(self._current_browser(), 1).until(
            EC.alert_is_present())
