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

from .events import dispatch


class LibraryListener(object):
    ROBOT_LISTENER_API_VERSION = 2

    def start_suite(self, name, attrs):
        dispatch('scope_start', attrs['longname'])

    def end_suite(self, name, attrs):
        dispatch('scope_end', attrs['longname'])

    def start_test(self, name, attrs):
        dispatch('scope_start', attrs['longname'])

    def end_test(self, name, attrs):
        dispatch('scope_end', attrs['longname'])
