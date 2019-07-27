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
from robot.libraries.BuiltIn import BuiltIn
from selenium.webdriver.remote.file_detector import FileDetector, LocalFileDetector

import SeleniumLibrary


class SelLibLocalFileDetector(FileDetector):

    def __init__(self):
        self.selenium_file_detector = LocalFileDetector()

    def is_local_file(self, *keys):
        if self.choose_file():
            return self.selenium_file_detector.is_local_file(*keys)
        return None

    def choose_file(self):
        try:
            sl = self._get_sl()
        except Exception:
            sl = None
        if sl and sl._running_keyword == 'choose_file':
            return True
        return False

    def _get_sl(self):
        libraries = BuiltIn().get_library_instance(all=True)
        for library in libraries:
            if isinstance(libraries[library], SeleniumLibrary.SeleniumLibrary):
                return libraries[library]
