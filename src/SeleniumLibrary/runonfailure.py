#  Copyright 2008-2011 Nokia Siemens Networks Oyj
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
import sys

try:
    from decorator import decorator
except SyntaxError: # decorator module requires Python/Jython 2.4+
    decorator = None
if sys.platform == 'cli':
    decorator = None # decorator module doesn't work with IronPython 2.6


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
        if self._selenium and not hasattr(err, '_selib_ran_on_failure'):
            self._run_on_failure()
            err._selib_ran_on_failure = True
        raise


class RunOnFailure(object):
    if decorator:
        __metaclass__ = runonfailuretype

    _run_on_failure = _do_nothing_on_failure = lambda self: None

    def register_keyword_to_run_on_failure(self, keyword_name):
        """Sets the keyword to execute when a SeleniumLibrary keyword fails.

        `keyword_name` is the name of a SeleniumLibrary keyword that
        will be executed if another SeleniumLibrary keyword fails.
        It is not possible to use a keyword that requires arguments.
        The name is case but not space sensitive. If the name does
        not match any keyword, this functionality is disabled and
        nothing extra will be done in case of a failure.

        The initial keyword to use is set in `importing`, and the
        keyword that is used by default is `Capture Screenshot`.
        Taking a screenshot when something failed is a very useful
        feature, but notice that it can slow down the execution.

        This keyword returns the name of the previously registered
        failure keyword. It can be used to restore the original
        value later.

        Examples:
        | Register Keyword To Run On Failure  | Log Source | # Run `Log Source` on failure. |
        | ${previous kw}= | Register Keyword To Run On Failure  | Nothing    | # Disables run-on-failure functionality and stores the previous kw name in a variable. |
        | Register Keyword To Run On Failure  | ${previous kw} | # Restore to the previous keyword. |

        The whole run-on-failure functionality is new in SeleniumLibrary 2.5.
        It only works when running tests on Python/Jython 2.4 or newer and
        it does not work on IronPython at all.
        """
        old = self._get_run_on_failure_name()
        self._set_run_on_failure(keyword_name)
        self._log_run_on_failure()
        return old

    def _set_run_on_failure(self, keyword_name):
        name = keyword_name.replace(' ', '_').lower()
        self._run_on_failure = getattr(self, name, self._do_nothing_on_failure)

    def _get_run_on_failure_name(self):
        if not self._run_on_failure_is_set():
            return 'No keyword'
        return self._run_on_failure.__name__.replace('_', ' ').title()

    def _run_on_failure_is_set(self):
        return self._run_on_failure != self._do_nothing_on_failure

    def _log_run_on_failure(self):
        self._info('%s will be run on failure.'
                   % self._get_run_on_failure_name())

