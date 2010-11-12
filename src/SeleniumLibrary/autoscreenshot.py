#  Copyright 2008-2009 Nokia Siemens Networks Oyj
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


class autoscreenshot(type):

    def __new__(cls, clsname, bases, dct):
        for name, method in dct.items():
            if _is_keyword(name, method):
                dct[name] = _wrap_with_auto_screenshot(method)
        return type.__new__(cls, clsname, bases, dct)


def _is_keyword(name, method):
        return (not name.startswith('_')) and inspect.isroutine(method)

def _wrap_with_auto_screenshot(method):
    def auto_screenshot_wrapper(self, *args):
        try:
            return method(self, *args)
        except Exception:
            self.capture_screenshot()
            raise
    return auto_screenshot_wrapper
