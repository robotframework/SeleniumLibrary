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

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import is_falsy, is_string


class RunOnFailureKeywords(LibraryComponent):

    @keyword
    def register_keyword_to_run_on_failure(self, keyword):
        """Sets the keyword to execute when a SeleniumLibrary keyword fails.

        `keyword` is the name of a keyword that will be executed if a
        SeleniumLibrary keyword fails. It is possible to use any available
        keyword, including user keywords or keywords from other libraries,
        but the keyword must not take any arguments.

        The initial keyword to use is set in `importing`, and the
        keyword that is used by default is `Capture Page Screenshot`.
        Taking a screenshot when something failed is a very useful
        feature, but notice that it can slow down the execution.

        It is possible to use string "Nothing" or "None", case-insensitively,
        as well as any value considered false in Python to disable this
        feature altogether.

        This keyword returns the name of the previously registered
        failure keyword or Python ``None`` if this functionality was
        previously disabled. The return value can be always used to
        restore the original value later.

        Example:
        | Register Keyword To Run On Failure  | Log Source | # Run `Log Source` on failure. |
        | ${previous kw}= | Register Keyword To Run On Failure  | Nothing    | # Disables run-on-failure functionality and stores the previous kw name in a variable. |
        | Register Keyword To Run On Failure  | ${previous kw} | # Restore to the previous keyword. |

        Changes in version 3.0.0:
        - Possible to use string "NONE" or any falsy value to disable the
          feature.
        - Return Python ``None`` when the functionality was disabled earlier.
          In previous versions special value "No Keyword" was returned and
          it could not be used to restore the original state.
        """
        old_keyword = self.ctx.run_on_failure_keyword
        keyword = self.resolve_keyword(keyword)
        self.ctx.run_on_failure_keyword = keyword
        self.info('%s will be run on failure.' % (keyword or 'No keyword'))
        return old_keyword

    @staticmethod
    def resolve_keyword(name):
        if is_falsy(name) or is_string(name) and name.upper() == 'NOTHING':
            return None
        return name
