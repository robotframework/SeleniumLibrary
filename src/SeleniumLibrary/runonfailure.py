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
    except Exception:
        self = args[0]
        self._run_on_failure()
        raise


class RunOnFailure(object):
    if decorator:
        __metaclass__ = runonfailuretype
