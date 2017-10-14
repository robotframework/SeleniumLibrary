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

from robot.utils import ConnectionCache


class BrowserCache(ConnectionCache):

    def __init__(self):
        ConnectionCache.__init__(self, no_current_msg='No current browser')
        self._closed = set()

    @property
    def browsers(self):
        return self._connections

    def get_open_browsers(self):
        open_browsers = []
        for browser in self._connections:
            if browser not in self._closed:
                open_browsers.append(browser)
        return open_browsers

    def close(self):
        if self.current:
            browser = self.current
            browser.quit()
            self.current = self._no_current
            self._closed.add(browser)

    def close_all(self):
        for browser in self._connections:
            if browser not in self._closed:
                browser.quit()
        self.empty_cache()
        return self.current
