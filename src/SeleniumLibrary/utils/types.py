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

# Originally based on  Robot Framework 3.0.2 robot.utils.robottypes and
# Can be removed when library minimum required Robot Framework
# version is greater than 3.0.4. Then Robot Framework is_truthy should
# also support string NONE as Python False. Also string 0 is evaluated
# as False in RF 3.1 but not in 3.0.4.
from robot.utils import is_string
from robot.utils import PY3


def is_truthy(item):
    if is_string(item):
        return item.upper() not in ('FALSE', 'NO', '', 'NONE', '0', 'OFF')
    return bool(item)


def is_falsy(item):
    return not is_truthy(item)


def is_noney(item):
    return item is None or is_string(item) and item.upper() == 'NONE'
