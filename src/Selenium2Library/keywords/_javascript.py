import os
from selenium.common.exceptions import WebDriverException

class _JavaScriptKeywords(object):

    def __init__(self):
        self._cancel_on_next_confirmation = False

    # Public

    def alert_should_be_present(self, text=''):
        alert_text = self.get_alert_message()
        if text and alert_text != text:
            raise AssertionError("Alert text should have been '%s' but was '%s'"
                                  % (text, alert_text))

    def choose_cancel_on_next_confirmation(self):
        self._cancel_on_next_confirmation = True

    def choose_ok_on_next_confirmation(self):
        self._cancel_on_next_confirmation = False

    def confirm_action(self):
        text = self._close_alert(not self._cancel_on_next_confirmation)
        self._cancel_on_next_confirmation = False
        return text

    def execute_javascript(self, *code):
        js = self._get_javascript_to_execute(''.join(code))
        self._info("Executing JavaScript:\n%s" % js)
        return self._current_browser().execute_script(js)

    def get_alert_message(self):
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