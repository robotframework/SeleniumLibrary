import os
from keywordgroup import KeywordGroup


class _JavaScriptKeywords(KeywordGroup):

    # Public

    def execute_javascript(self, *code):
        """Executes the given JavaScript code.

        `code` may contain multiple lines of code and may be divided into
        multiple cells in the test data. In that case, the parts are
        catenated together without adding spaces.

        If `code` is an absolute path to an existing file, the JavaScript
        to execute will be read from that file. Forward slashes work as
        a path separator on all operating systems.

        The JavaScript executes in the context of the currently selected
        frame or window as the body of an anonymous function. Use _window_ to
        refer to the window of your application and _document_ to refer to the
        document object of the current frame or window, e.g.
        _document.getElementById('foo')_.

        This keyword returns None unless there is a return statement in the
        JavaScript. Return values are converted to the appropriate type in
        Python, including WebElements.

        Examples:
        | Execute JavaScript | window.my_js_function('arg1', 'arg2') |               |
        | Execute JavaScript | ${CURDIR}/js_to_execute.js            |               |
        | ${sum}=            | Execute JavaScript                    | return 1 + 1; |
        | Should Be Equal    | ${sum}                                | ${2}          |
        """
        js = self._get_javascript_to_execute(''.join(code))
        self._info("Executing JavaScript:\n%s" % js)
        return self._current_browser().execute_script(js)

    def execute_async_javascript(self, *code):
        """Executes asynchronous JavaScript code.

        Similar to `Execute Javascript` except that scripts executed with
        this keyword must explicitly signal they are finished by invoking the
        provided callback. This callback is always injected into the executed
        function as the last argument.

        Scripts must complete within the script timeout or this keyword will
        fail. See the `Timeouts` section for more information.

        Examples:
        | Execute Async JavaScript | var callback = arguments[arguments.length - 1]; | window.setTimeout(callback, 2000); |
        | Execute Async JavaScript | ${CURDIR}/async_js_to_execute.js                |                                    |
        | ${retval}=               | Execute Async JavaScript                        |                                    |
        | ...                      | var callback = arguments[arguments.length - 1]; |                                    |
        | ...                      | function answer(){callback("text");};           |                                    |
        | ...                      | window.setTimeout(answer, 2000);                |                                    |
        | Should Be Equal          | ${retval}                                       | text                               |
        """
        js = self._get_javascript_to_execute(''.join(code))
        self._info("Executing Asynchronous JavaScript:\n%s" % js)
        return self._current_browser().execute_async_script(js)

    # Private

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
