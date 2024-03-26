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
import string
from typing import Optional

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.errors import UnkownExpectedCondition
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExpectedConditionKeywords(LibraryComponent):
    @keyword
    def wait_for_expected_condition(self, condition: string, *args, timeout: Optional[float]=10):
        """Waits until ``condition`` is true or ``timeout`` expires.

        The condition must be one of selenium's expected condition which
        can be found within the selenium
        [https://www.selenium.dev/selenium/docs/api/py/webdriver_support/selenium.webdriver.support.expected_conditions.html#module-selenium.webdriver.support.expected_conditions Python API]
        documentation. The expected condition can written as snake_case
        (ex title_is) or it can be space delimited (ex Title Is). Some
        conditions require additional arguments or ``args`` which should
        be passed along after the expected condition.

        Fails if the timeout expires before the condition becomes true.
        The default value is 10 seconds.

        Examples:
        | `Wait For Expected Condition` | alert_is_present |
        | `Wait For Expected Condition` |  Title Is  | New Title |

        If the expected condition expects a locator then one can pass
        as arguments a tuple containing the selenium locator strategies
        and the locator.

        Example of expected condition expecting locator:
        | ${byElem}= |  Evaluate  ("id","added_btn")
        | `Wait For Expected Condition` | Presence Of Element Located | ${byElem}
        """

        condition = self._parse_condition(condition)
        wait = WebDriverWait(self.driver, timeout, 0.1)
        try:
            c = getattr(EC, condition)
        except:
            # ToDo: provide hints as to what is avaialbel or find closet match
            raise UnkownExpectedCondition(f"{condition} is an unknown expected condition")
        result = wait.until(c(*args), message="Expected Condition not met within set timeout of " + str(timeout))
        return result

    def _parse_condition(self, condition: string):
        parsed = condition.replace(' ','_').lower()
        return parsed