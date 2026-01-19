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
from datetime import timedelta
from typing import Any

from robot.utils import timestr_to_secs
from robot.utils import is_truthy, is_falsy  # noqa

# Need only for unit tests and can be removed when Approval tests fixes:
# https://github.com/approvals/ApprovalTests.Python/issues/41
WINDOWS = os.name == "nt"


def is_noney(item):
    return item is None or isinstance(item, str) and item.upper() == "NONE"

def _convert_delay(delay):
    if isinstance(delay, timedelta):
        return delay.microseconds // 1000
    else:
        x =  timestr_to_secs(delay)
        return int( x * 1000)


def _convert_timeout(timeout):
    if isinstance(timeout, timedelta):
        return timeout.total_seconds()
    return timestr_to_secs(timeout)


def type_converter(argument: Any) -> str:
    return type(argument).__name__.lower()
