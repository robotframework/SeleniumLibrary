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

    @keyword
    def execute_javascript_with_arguments(self, *code):
        """ Executes the given JavaScript code with the given arguments
        #TODO: Add docstring
        """
        code, args = self._get_javascript_to_execute(code)
        self._execute_javascript_code(code, *args)

    @keyword
    def execute_async_javascript_with_arguments(self, *code):
        """ Executes the given asynchronous JavaScript code with the given
        arguments
        #TODO: Add docstring
        """
        code, args = self._get_javascript_to_execute(code)
        self._execute_async_javascript_code(code, args)

    def _prepare_argument_list(self, args):
        self.args_list = []
        for idx, item in enumerate(args):
            self.args_list.append("arguments[" + str(idx) + "]: " +
                                  str(item))

    def _execute_javascript_code(self, code, *args):
        if len(args) > 0:
            self._prepare_argument_list(args)
            self.info("Executing JavaScript: ""\n%s\n"
                      "with arguments \n%s" % (
                          code, "\n".join(self.args_list)))
        else:
            self.info("Executing JavaScript:\n%s" % code)
        self.driver.execute_script(code, *args)

    def _execute_async_javascript_code(self, code, *args):
        if len(args) > 0:
            self._prepare_argument_list(*args)
            self.info("Executing Async JavaScript: ""\n%s\n"
                      "with arguments \n%s" % (
                          code, "\n".join(self.args_list)))
            return self.driver.execute_script(code, *args)

        else:
            self.info("Executing Async JavaScript: \n%s" % code)
            return self.driver.execute_script(code)

    def _get_javascript_to_execute(self, lines):
        if all(isinstance(n, str) for n in lines):
            code = ''.join(lines)
            path = code.replace('/', os.sep)
            if os.path.isabs(path) and os.path.isfile(path):
                code = self._read_javascript_from_file(path)
                return code, []

        code, args = self._parse_javascript_and_arguments(lines)
        return code, args

    def _parse_javascript_and_arguments(self, code):
        is_arg = False
        is_code = True
        self.codelines = ''
        self.args = []

        for exp in code:
            if str(exp).strip() == "JAVASCRIPT":
                is_code = True
                is_arg = False
            elif str(exp).strip() == "ARGUMENTS":
                is_arg = True
                is_code = False
            elif is_code:
                self.codelines = self.codelines.__add__(exp + '\n')
            elif is_arg:
                self.args.append(exp)

        return self.codelines, self.args

    def _read_javascript_from_file(self, path):
        self.info('Reading JavaScript from file <a href="file://%s">%s</a>.'
                  .format(path.replace(os.sep, '/'), path), html=True)
        with open(path) as file:
            return file.read().strip()
