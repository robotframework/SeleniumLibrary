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

from robot.utils import get_link_path

from SeleniumLibrary.base import LibraryComponent, keyword
from SeleniumLibrary.utils import is_noney


class ScreenshotKeywords(LibraryComponent):

    @keyword
    def set_screenshot_directory(self, path):
        """Sets the directory for captured screenshots.

        ``path`` argument specifies the absolute path to a directory where
        the screenshots should be written to. If the directory does not
        exist, it will be created. The directory can also be set when
        `importing` the library. If it is not configured anywhere,
        screenshots are saved to the same directory where Robot Framework's
        log file is written.

        ``persist`` argument is deprecated and has no effect.

        The previous value is returned and can be used to restore
        the original value later if needed.

        Returning the previous value is new in SeleniumLibrary 3.0.
        The persist argument was removed in SeleniumLibrary 3.2.
        """
        if is_noney(path):
            path = None
        else:
            path = os.path.abspath(path)
            self._create_directory(path)
        previous = self.ctx.screenshot_root_directory
        self.ctx.screenshot_root_directory = path
        return previous

    @keyword
    def capture_page_screenshot(self,
                                filename='selenium-screenshot-{index}.png'):
        """Takes screenshot of the current page and embeds it into log file.

        ``filename`` argument specifies the name of the file to write the
        screenshot into. The directory where screenshots are saved can be
        set when `importing` the library or by using the `Set Screenshot
        Directory` keyword. If the directory is not configured, screenshots
        are saved to the same directory where Robot Framework's log file is
        written.

        Starting from SeleniumLibrary 1.8, if ``filename`` contains marker
        ``{index}``, it will be automatically replaced with unique running
        index preventing files to be overwritten. Indices start from 1,
        and how they are represented can be customized using Python's
        [https://docs.python.org/2/library/string.html#formatstrings|
        format string syntax].

        An absolute path to the created screenshot file is returned.

        Examples:
        | `Capture Page Screenshot` |                                        |
        | `File Should Exist`       | ${OUTPUTDIR}/selenium-screenshot-1.png |
        | ${path} =                 | `Capture Page Screenshot`              |
        | `File Should Exist`       | ${OUTPUTDIR}/selenium-screenshot-2.png |
        | `File Should Exist`       | ${path}                                |
        | `Capture Page Screenshot` | custom_name.png                        |
        | `File Should Exist`       | ${OUTPUTDIR}/custom_name.png           |
        | `Capture Page Screenshot` | custom_with_index_{index}.png          |
        | `File Should Exist`       | ${OUTPUTDIR}/custom_with_index_1.png   |
        | `Capture Page Screenshot` | formatted_index_{index:03}.png         |
        | `File Should Exist`       | ${OUTPUTDIR}/formatted_index_001.png   |
        """
        if not self.drivers.current:
            self.info('Cannot capture screenshot because no browser is open.')
            return
        path = self._get_screenshot_path(filename)
        self._create_directory(path)
        if not self.driver.save_screenshot(path):
            raise RuntimeError("Failed to save screenshot '{}'.".format(path))
        # Image is shown on its own row and thus previous row is closed on
        # purpose. Depending on Robot's log structure is a bit risky.
        self.info('</td></tr><tr><td colspan="3">'
                  '<a href="{src}"><img src="{src}" width="800px"></a>'
                  .format(src=get_link_path(path, self.log_dir)), html=True)
        return path

    def _get_screenshot_path(self, filename):
        directory = self.ctx.screenshot_root_directory or self.log_dir
        filename = filename.replace('/', os.sep)
        index = 0
        while True:
            index += 1
            formatted = filename.format(index=index)
            path = os.path.join(directory, formatted)
            # filename didn't contain {index} or unique path was found
            if formatted == filename or not os.path.exists(path):
                return path

    def _create_directory(self, path):
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
