import time
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from keywordgroup import KeywordGroup


class _AlertKeywords(KeywordGroup):

    __ACCEPT_ALERT = 'accept'
    __DISMISS_ALERT = 'dismiss'

    def __init__(self):
        self._next_alert_dismiss_type = self.__ACCEPT_ALERT

    # Public

    def input_text_into_prompt(self, text):
        """Types the given `text` into alert box.  """
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
        alert_text = self._handle_alert(self.__ACCEPT_ALERT)
        if text and alert_text != text:
            raise AssertionError("Alert text should have been "
                                 "'%s' but was '%s'"
                                 % (text, alert_text))

    def choose_cancel_on_next_confirmation(self):
        """Cancel will be selected the next time `Confirm Action` is used."""
        self._next_alert_dismiss_type = self.__DISMISS_ALERT

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
        self._next_alert_dismiss_type = self.__ACCEPT_ALERT

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
        text = self._handle_alert(self._next_alert_dismiss_type)
        self._next_alert_dismiss_type = self.__DISMISS_ALERT
        return text

    def get_alert_message(self, dismiss=True):
        """Returns the text of current JavaScript alert.

        By default the current JavaScript alert will be dismissed.
        This keyword will fail if no alert is present. Note that
        following keywords will fail unless the alert is
        dismissed by this keyword or another like `Get Alert Message`.
        """
        if dismiss:
            return self._handle_alert(self.__DISMISS_ALERT)
        else:
            return self._handle_alert()

    def dismiss_alert(self, accept=True):
        """ Returns true if alert was confirmed, false if it was dismissed

        This keyword will fail if no alert is present. Note that
        following keywords will fail unless the alert is
        dismissed by this keyword or another like `Get Alert Message`.
        """
        if accept:
            return self._handle_alert(self.__ACCEPT_ALERT)
        else:
            return self._handle_alert()

    def _handle_alert(self, dismiss_type=None):
        """Alert re-try for Chrome

        Because Chrome has difficulties to handle alerts, like::

        alert.text
        alert.dismiss

        This function creates a re-try funtionality to better support
        alerts in Chrome.
        """
        retry = 0
        while retry < 4:
            try:
                return self._alert_worker(dismiss_type)
            except WebDriverException:
                time.sleep(0.2)
                retry += 1
        raise RuntimeError('There were no alerts')

    def _alert_worker(self, dismiss_type=None):
        alert = self._wait_alert()
        text = ' '.join(alert.text.splitlines())
        if dismiss_type == self.__DISMISS_ALERT:
            alert.dismiss()
        elif dismiss_type == self.__ACCEPT_ALERT:
            alert.accept()
        return text

    def _wait_alert(self):
        return WebDriverWait(self._current_browser(), 1).until(
            EC.alert_is_present())
