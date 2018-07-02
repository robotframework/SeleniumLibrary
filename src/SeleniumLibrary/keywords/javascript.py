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

import os

from SeleniumLibrary.base import LibraryComponent, keyword


class JavaScriptKeywords(LibraryComponent):

    @keyword
    def execute_javascript(self, *code):
        """Executes the given JavaScript code.

        ``code`` may contain multiple lines of code and may be divided into
        multiple cells in the test data. In that case, the parts are
        concatenated together without adding spaces.

        If ``code`` is an absolute path to an existing file, the JavaScript
        to execute will be read from that file. Forward slashes work as
        a path separator on all operating systems.

        The JavaScript executes in the context of the currently selected
        frame or window as the body of an anonymous function. Use ``window``
        to refer to the window of your application and ``document`` to refer
        to the document object of the current frame or window, e.g.
        ``document.getElementById('example')``.

        This keyword returns whatever the executed JavaScript code returns.
        Return values are converted to the appropriate Python types.

        Examples:
        | `Execute JavaScript` | window.myFunc('arg1', 'arg2') |
        | `Execute JavaScript` | ${CURDIR}/js_to_execute.js    |
        | ${sum} =             | `Execute JavaScript` | return 1 + 1; |
        | `Should Be Equal`    | ${sum}               | ${2}          |
        """
        js = self._get_javascript_to_execute(code)
        self.info("Executing JavaScript:\n%s" % js)
        return self.driver.execute_script(js)

    @keyword
    def execute_async_javascript(self, *code):
        """Executes asynchronous JavaScript code.

        Similar to `Execute Javascript` except that scripts executed with
        this keyword must explicitly signal they are finished by invoking the
        provided callback. This callback is always injected into the executed
        function as the last argument.

        Scripts must complete within the script timeout or this keyword will
        fail. See the `Timeouts` section for more information.

        Examples:
        | `Execute Async JavaScript` | var callback = arguments[arguments.length - 1]; window.setTimeout(callback, 2000); |
        | `Execute Async JavaScript` | ${CURDIR}/async_js_to_execute.js |
        | ${result} = | `Execute Async JavaScript`                      |
        | ...         | var callback = arguments[arguments.length - 1]; |
        | ...         | function answer(){callback("text");};           |
        | ...         | window.setTimeout(answer, 2000);                |
        | `Should Be Equal` | ${result} | text |
        """
        js = self._get_javascript_to_execute(code)
        self.info("Executing Asynchronous JavaScript:\n%s" % js)
        return self.driver.execute_async_script(js)

    def _get_javascript_to_execute(self, lines):
        code = ''.join(lines)
        path = code.replace('/', os.sep)
        if os.path.isabs(path) and os.path.isfile(path):
            code = self._read_javascript_from_file(path)
        return code

    def _read_javascript_from_file(self, path):
        self.info('Reading JavaScript from file <a href="file://%s">%s</a>.'
                  .format(path.replace(os.sep, '/'), path), html=True)
        with open(path) as file:
            return file.read().strip()
