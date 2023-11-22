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
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class ExpectedConditionKeywords(LibraryComponent):
    @keyword
    def wait_for_expected_condition(self, condition: string, *args, timeout: Optional[float]=10):
        wait = WebDriverWait(self.driver, timeout, 0.1)
        # import sys,pdb;pdb.Pdb(stdout=sys.__stdout__).set_trace()
        c = getattr(EC, condition)
        result = wait.until(c(*args), message="Expected Condition not met within set timeout of " + str(timeout))
        return result
