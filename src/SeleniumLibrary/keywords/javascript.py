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
from collections import namedtuple
from typing import Any, Union

from robot.utils import plural_or_not, seq2str

from selenium.webdriver.remote.webelement import WebElement
from SeleniumLibrary.base import LibraryComponent, keyword


class JavaScriptKeywords(LibraryComponent):

    js_marker = "JAVASCRIPT"
    arg_marker = "ARGUMENTS"

    @keyword
    def execute_javascript(self, *code: Any) -> Any:
        """Executes the given JavaScript code with possible arguments.

        ``code`` may be divided into multiple cells in the test data and
        ``code`` may contain multiple lines of code and arguments. In that case,
        the JavaScript code parts are concatenated together without adding
        spaces and optional arguments are separated from ``code``.

        If ``code`` is a path to an existing file, the JavaScript
        to execute will be read from that file. Forward slashes work as
        a path separator on all operating systems.

        The JavaScript executes in the context of the currently selected
        frame or window as the body of an anonymous function. Use ``window``
        to refer to the window of your application and ``document`` to refer
        to the document object of the current frame or window, e.g.
        ``document.getElementById('example')``.

        This keyword returns whatever the executed JavaScript code returns.
        Return values are converted to the appropriate Python types.

        Starting from SeleniumLibrary 3.2 it is possible to provide JavaScript
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.execute_script|
        arguments] as part of ``code`` argument. The JavaScript code and
        arguments must be separated with `JAVASCRIPT` and `ARGUMENTS` markers
        and must be used exactly with this format. If the Javascript code is
        first, then the `JAVASCRIPT` marker is optional. The order of
        `JAVASCRIPT` and `ARGUMENTS` markers can be swapped, but if `ARGUMENTS`
        is the first marker, then `JAVASCRIPT` marker is mandatory. It is only
        allowed to use `JAVASCRIPT` and `ARGUMENTS` markers only one time in the
        ``code`` argument.

        Examples:
        | `Execute JavaScript` | window.myFunc('arg1', 'arg2') |
        | `Execute JavaScript` | ${CURDIR}/js_to_execute.js    |
        | `Execute JavaScript` | alert(arguments[0]); | ARGUMENTS | 123 |
        | `Execute JavaScript` | ARGUMENTS | 123 | JAVASCRIPT | alert(arguments[0]); |
        """
        js_code, js_args = self._get_javascript_to_execute(code)
        self._js_logger("Executing JavaScript", js_code, js_args)
        return self.driver.execute_script(js_code, *js_args)

    @keyword
    def execute_async_javascript(self, *code: Any) -> Any:
        """Executes asynchronous JavaScript code with possible arguments.

        Similar to `Execute Javascript` except that scripts executed with
        this keyword must explicitly signal they are finished by invoking the
        provided callback. This callback is always injected into the executed
        function as the last argument.

        Scripts must complete within the script timeout or this keyword will
        fail. See the `Timeout` section for more information.

        Starting from SeleniumLibrary 3.2 it is possible to provide JavaScript
        [https://seleniumhq.github.io/selenium/docs/api/py/webdriver_remote/selenium.webdriver.remote.webdriver.html#selenium.webdriver.remote.webdriver.WebDriver.execute_async_script|
        arguments] as part of ``code`` argument. See `Execute Javascript` for
        more details.

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
        self._js_logger("Executing Asynchronous JavaScript", js_code, js_args)
        return self.driver.execute_async_script(js_code, *js_args)

    def _js_logger(self, base, code, args):
        message = f"{base}:\n{code}\n"
        if args:
            message = (
                f"{message}By using argument{plural_or_not(args)}:\n{seq2str(args)}"
            )
        else:
            message = f"{message}Without any arguments."
        self.info(message)

    def _get_javascript_to_execute(self, code):
        js_code, js_args = self._separate_code_and_args(code)
        if not js_code:
            raise ValueError("JavaScript code was not found from code argument.")
        js_code = "".join(js_code)
        path = js_code.replace("/", os.sep)
        if os.path.isabs(path) and os.path.isfile(path):
            js_code = self._read_javascript_from_file(path)
        return js_code, js_args

    def _separate_code_and_args(self, code):
        code = list(code)
        self._check_marker_error(code)
        index = self._get_marker_index(code)
        if self.arg_marker not in code:
            return code[index.js + 1 :], []
        if self.js_marker not in code:
            return code[0 : index.arg], code[index.arg + 1 :]
        else:
            if index.js == 0:
                return code[index.js + 1 : index.arg], code[index.arg + 1 :]
            else:
                return code[index.js + 1 :], code[index.arg + 1 : index.js]

    def _check_marker_error(self, code):
        if not code:
            raise ValueError("There must be at least one argument defined.")
        message = None
        template = " marker was found two times in the code."
        if code.count(self.js_marker) > 1:
            message = f"{self.js_marker}{template}"
        if code.count(self.arg_marker) > 1:
            message = f"{self.arg_marker}{template}"
        index = self._get_marker_index(code)
        if index.js > 0 and index.arg != 0:
            message = f"{self.js_marker}{template}"
        if message:
            raise ValueError(message)

    def _get_marker_index(self, code):
        Index = namedtuple("Index", "js arg")
        if self.js_marker in code:
            js = code.index(self.js_marker)
        else:
            js = -1
        if self.arg_marker in code:
            arg = code.index(self.arg_marker)
        else:
            arg = -1
        return Index(js=js, arg=arg)

    def _read_javascript_from_file(self, path):
        self.info(
            f'Reading JavaScript from file <a href="file://{path.replace(os.sep, "/")}">{path}</a>.',
            html=True,
        )
        with open(path) as file:
            return file.read().strip()
