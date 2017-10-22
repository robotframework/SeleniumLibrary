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

from collections import namedtuple


def parse_range(range_string):
    Range = namedtuple('Range', 'minimum maximum')
    try:
        integer = int(range_string)
        return Range(minimum=integer, maximum=integer)
    except ValueError:
        number1, number2 = _sprint_range(range_string)
        number1 = _convert_to_int(number1)
        number2 = _convert_to_int(number2)
        if number1 < 0 or number2 < 0:
            raise ValueError('Invalid range definition')
        if number1 < number2:
            return Range(minimum=number1, maximum=number2)
        return Range(minimum=number2, maximum=number1)


def _sprint_range(range_string):
    if '..' in range_string:
        return range_string.split('..')
    raise ValueError('Invalid range definition')


def _convert_to_int(number):
    try:
        return int(number)
    except ValueError:
        raise ValueError('Invalid range definition')
