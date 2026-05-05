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
from datetime import timedelta
from typing import Any, TypeAlias

from robot.utils import is_falsy, is_truthy, timestr_to_secs  # noqa
from selenium.webdriver.remote.webelement import WebElement

try:
    from robot.api.types import Secret
except ImportError:
    # Robot Framework < 7.4 does not have the Secret type.
    # This shim lets users on older RF versions still import it without
    # errors. It can be removed once RF 7.4+ is the minimum requirement.
    class Secret:  # type: ignore[no-redef]
        """Backport shim for ``robot.api.types.Secret`` (RF 7.4+).

        Mirrors the public interface of the real class so that ``isinstance``
        checks and ``.value`` access work uniformly across RF versions.
        """

        def __init__(self, value: str):
            self.value = value

        def __str__(self) -> str:
            return "<secret>"

        def __repr__(self) -> str:
            return f"{type(self).__name__}(value=<secret>)"

Locator: TypeAlias = WebElement | str | list["Locator"]


def is_noney(item):
    return item is None or (isinstance(item, str) and item.upper() == "NONE")


def _convert_delay(delay):
    if isinstance(delay, timedelta):
        return delay.microseconds // 1000
    x = timestr_to_secs(delay)
    return int(x * 1000)


def _convert_timeout(timeout):
    if isinstance(timeout, timedelta):
        return timeout.total_seconds()
    return timestr_to_secs(timeout)


def type_converter(argument: Any) -> str:
    return type(argument).__name__.lower()
