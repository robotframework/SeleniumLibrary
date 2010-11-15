#  Copyright 2008-2010 Nokia Siemens Networks Oyj
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import inspect

try:
    from decorator import decorator
except SyntaxError: # decorator module requires Python/Jython 2.4+
    decorator = None


class runonfailuretype(type):

    def __new__(cls, clsname, bases, dct):
        for name, method in dct.items():
            if _is_keyword(name, method):
                dct[name] = decorator(_run_on_failure_wrapper, method)
        return type.__new__(cls, clsname, bases, dct)


def _is_keyword(name, method):
    return (not name.startswith('_')) and inspect.isroutine(method)

def _run_on_failure_wrapper(method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except Exception, err:
        self = args[0]
        if self._selenium and not hasattr(err, 'ran_on_failure'):
            self._run_on_failure()
            err.ran_on_failure = True
        raise


class RunOnFailure(object):
    if decorator:
        __metaclass__ = runonfailuretype

    _run_on_failure = _no_run_on_failure = lambda self: None

    def run_on_failure(self, keyword_name):
        """Sets the keyword to be run when a SeleniumLibrary keyword fails.

        `keyword_name` is the name of the keyword to be executed and it must be
        a SeleniumLibrary keyword. The name is case and underscore insensitive.

        If `keyword_name` is not a valid keyword name, nothing will be executed
        in case of failure.

        Returns the previous keyword name.

        Examples:
        | Run On Failure  | Log Source |# Run `Log Source` in case of failure.
        | Run On Failure  | capture_screenshot |# The name is case and underscore insensitive; this runs `Capture Screenshot`.
        | Run On Failure  | Nothing    |# Do nothing in case of failure. Can be also used to override the default keyword set in `library importing`.
        """
        old = self._get_run_on_failure_name()
        self._set_run_on_failure(keyword_name)
        self._log_run_on_failure()
        return old

    def _set_run_on_failure(self, keyword_name):
        name = keyword_name.replace(' ', '_').lower()
        self._run_on_failure = getattr(self, name, self._no_run_on_failure)

    def _get_run_on_failure_name(self):
        if not self._run_on_failure_is_set():
            return 'No keyword'
        return self._run_on_failure.__name__.replace('_', ' ').title()

    def _run_on_failure_is_set(self):
        return self._run_on_failure != self._no_run_on_failure

    def _log_run_on_failure(self):
        self._info('%s will be run on failure.' % self._get_run_on_failure_name())

