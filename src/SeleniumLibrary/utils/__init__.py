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

from robot.utils import plural_or_not, secs_to_timestr, timestr_to_secs  # noqa

from .librarylistener import LibraryListener  # noqa
from .types import (
    is_falsy,
    is_noney,
    is_string,
    is_truthy,
    WINDOWS,
    _convert_timeout,
    _convert_delay,
)  # noqa


def escape_xpath_value(value: str):
    value = str(value)
    if '"' in value and "'" in value:
        parts_wo_apos = value.split("'")
        escaped = "', \"'\", '".join(parts_wo_apos)
        return f"concat('{escaped}')"
    if "'" in value:
        return f'"{value}"'
    return f"'{value}'"
