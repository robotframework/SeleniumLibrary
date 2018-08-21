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
        js_code, js_args = self._get_javascript_to_execute(code)
        self.info("Executing JavaScript:\n%s\nBy using arguments %s"
                  % (js_code, js_args))
        return self.driver.execute_script(js_code, *js_args)

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
        js_code, js_args = self._get_javascript_to_execute(code)
        self.info("Executing Asynchronous JavaScript:\n%s\nBy using arguments %s"
                  % (js_code, js_args))
        return self.driver.execute_async_script(js_code, *js_args)

    def _get_javascript_to_execute(self, code):
        js_code, js_args = self._separate_code_and_args(code)
        js_code = ''.join(js_code)
        path = js_code.replace('/', os.sep)
        if os.path.isfile(path):
            js_code = self._read_javascript_from_file(path)
        return js_code, js_args

    def _separate_code_and_args(self, code):
        if not code:
            raise ValueError('There must be at least one JavaScript line defined.')
        js_code, js_args = [], []
        get_code, get_args = False, False
        found_code, found_args = False, False
        for line in code:
            if line == 'JAVASCRIPT':
                if found_code:
                    raise ValueError('JAVASCRIPT marker was found two times in code.')
                get_code, found_code = True, True
                get_args = False
                continue
            if line == 'ARGUMENTS':
                if found_args:
                    raise ValueError('ARGUMENTS marker was found two times in code.')
                get_code = False
                get_args, found_args = True, True
                continue
            if not get_code and not get_args:
                get_code, found_code = True, True
            if get_code:
                js_code.append(line)
            if get_args:
                js_args.append(line)
        return js_code, js_args

    def _read_javascript_from_file(self, path):
        self.info('Reading JavaScript from file <a href="file://%s">%s</a>.'
                  .format(path.replace(os.sep, '/'), path), html=True)
        with open(path) as file:
            return file.read().strip()
