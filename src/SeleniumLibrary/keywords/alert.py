# Copyright 2008-2011 Nokia Networks
# Copyright 2011-2016 Ryan Tomac, Ed Manlove and contributors
# Copyright 2016-     Robot Framework Foundation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import timedelta
from typing import Optional

from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from SeleniumLibrary.base import keyword, LibraryComponent
from SeleniumLibrary.utils import secs_to_timestr


class AlertKeywords(LibraryComponent):
    ACCEPT = "ACCEPT"
    DISMISS = "DISMISS"
    LEAVE = "LEAVE"
    _next_alert_action = ACCEPT

    @keyword
    def input_text_into_alert(
        self, text: str, action: str = ACCEPT, timeout: Optional[timedelta] = None
    ):
        """Types the given ``text`` into an input field in an alert.

        The alert is accepted by default, but that behavior can be controlled
        by using the ``action`` argument same way as with `Handle Alert`.

        ``timeout`` specifies how long to wait for the alert to appear.
        If it is not given, the global default `timeout` is used instead.

        New in SeleniumLibrary 3.0.
        """
        alert = self._wait_alert(timeout)
        alert.send_keys(text)
        self._handle_alert(alert, action)

    @keyword
    def alert_should_be_present(
        self,
        text: str = "",
        action: str = ACCEPT,
        timeout: Optional[timedelta] = None,
    ):
        """Verifies that an alert is present and by default, accepts it.

        Fails if no alert is present. If ``text`` is a non-empty string,
        then it is used to verify alert's message. The alert is accepted
        by default, but that behavior can be controlled by using the
        ``action`` argument same way as with `Handle Alert`.

        ``timeout`` specifies how long to wait for the alert to appear.
        If it is not given, the global default `timeout` is used instead.

        ``action`` and ``timeout`` arguments are new in SeleniumLibrary 3.0.
        In earlier versions, the alert was always accepted and a timeout was
        hardcoded to one second.
        """
        message = self.handle_alert(action, timeout)
        if text and text != message:
            raise AssertionError(
                f"Alert message should have been '{text}' but it " f"was '{message}'."
            )

    @keyword
    def alert_should_not_be_present(
        self, action: str = ACCEPT, timeout: Optional[timedelta] = None
    ):
        """Verifies that no alert is present.

        If the alert actually exists, the ``action`` argument determines
        how it should be handled. By default, the alert is accepted, but
        it can be also dismissed or left open the same way as with the
        `Handle Alert` keyword.

        ``timeout`` specifies how long to wait for the alert to appear.
        By default, is not waited for the alert at all, but a custom time can
        be given if alert may be delayed. See the `time format` section
        for information about the syntax.

        New in SeleniumLibrary 3.0.
        """
        try:
            alert = self._wait_alert(timeout)
        except AssertionError:
            return
        text = self._handle_alert(alert, action)
        raise AssertionError(f"Alert with message '{text}' present.")

    @keyword
    def handle_alert(self, action: str = ACCEPT, timeout: Optional[timedelta] = None):
        """Handles the current alert and returns its message.

        By default, the alert is accepted, but this can be controlled
        with the ``action`` argument that supports the following
        case-insensitive values:

        - ``ACCEPT``: Accept the alert i.e. press ``Ok``. Default.
        - ``DISMISS``: Dismiss the alert i.e. press ``Cancel``.
        - ``LEAVE``: Leave the alert open.

        The ``timeout`` argument specifies how long to wait for the alert
        to appear. If it is not given, the global default `timeout` is used
        instead.

        Examples:
        | Handle Alert |                |       | # Accept alert.  |
        | Handle Alert | action=DISMISS |       | # Dismiss alert. |
        | Handle Alert | timeout=10 s   |       | # Use custom timeout and accept alert.  |
        | Handle Alert | DISMISS        | 1 min | # Use custom timeout and dismiss alert. |
        | ${message} = | Handle Alert   |       | # Accept alert and get its message.     |
        | ${message} = | Handle Alert   | LEAVE | # Leave alert open and get its message. |

        New in SeleniumLibrary 3.0.
        """
        self.info(f"HANDLE::{type(timeout)}::{timeout}")
        alert = self._wait_alert(timeout)
        return self._handle_alert(alert, action)

    def _handle_alert(self, alert, action):
        action = action.upper()
        text = " ".join(alert.text.splitlines())
        if action == self.ACCEPT:
            alert.accept()
        elif action == self.DISMISS:
            alert.dismiss()
        elif action != self.LEAVE:
            raise ValueError(f"Invalid alert action '{action}'.")
        return text

    def _wait_alert(self, timeout=None):
        timeout = self.get_timeout(timeout)
        wait = WebDriverWait(self.driver, timeout)
        try:
            return wait.until(EC.alert_is_present())
        except TimeoutException:
            raise AssertionError(f"Alert not found in {secs_to_timestr(timeout)}.")
        except WebDriverException as err:
            raise AssertionError(f"An exception occurred waiting for alert: {err}")
