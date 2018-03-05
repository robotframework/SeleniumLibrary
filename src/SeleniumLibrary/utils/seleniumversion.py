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

import selenium

SeleniumVersion = namedtuple('SeleniumVersion', 'major minor micro')
major, minor, micro = (selenium.__version__.split('.') + ['0', '0'])[:3]
major, minor, micro = int(major), int(minor), int(micro)
SELENIUM_VERSION = SeleniumVersion(major=major, minor=minor, micro=micro)
