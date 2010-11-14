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

from decorator import decorator


class autoscreenshot(type):

    def __new__(cls, clsname, bases, dct):
        for name, method in dct.items():
            if _is_keyword(name, method):
                dct[name] = decorator(_auto_screenshot_wrapper, method)
        return type.__new__(cls, clsname, bases, dct)


def _is_keyword(name, method):
    return (not name.startswith('_')) and inspect.isroutine(method)

def _auto_screenshot_wrapper(method, *args, **kwargs):
    try:
        return method(*args, **kwargs)
    except Exception:
        args[0].capture_screenshot()
        raise

