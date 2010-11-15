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
        if self._selenium and not hasattr(err, '_selib_ran_on_failure'):
            self._run_on_failure()
            err._selib_ran_on_failure = True
        raise


class RunOnFailure(object):
    if decorator:
        __metaclass__ = runonfailuretype

    _run_on_failure = _do_nothing_on_failure = lambda self: None

    def run_on_failure(self, keyword_name):
        """Sets the keyword to execute when a SeleniumLibrary keyword fails.

        `keyword_name` is the name of a SeleniumLibrary keyword that
        will be executed if another SeleniumLibrary keyword fails.
        The name is case but not space sensitive.  If the name does
        not match any keyword, this functionality is disabled and
        nothing extra will be done in case of a failure.

        The initial keyword to use is set in `importing`, and the
        keyword that is used by default is `Capture
        Screenshot`. Taking a screenshot when something failed is a
        very useful feature, but notice that it can slow down the
        execution.

        This keyword returns the name of the previously registered
        failure keyword. It can be used to restore the original
        value later.

        Examples:
        | Run On Failure  | Log Source | # Run `Log Source` on failure. |
        | Run On Failure  | Nothing    | # Disables run-on-failure functionality. |

        The whole run-on-failure functionality is new in SeleniumLibrary 2.5.
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

